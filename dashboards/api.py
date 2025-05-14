import traceback
import uuid
from datetime import datetime
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django_celery_beat.models import PeriodicTask, IntervalSchedule, CrontabSchedule
from .models import Automacao, LogAutomacao
from .serializers import (
    IntervalScheduleSerializer,
    CrontabScheduleSerializer,
    PeriodicTaskSerializer,
    AutomacaoSerializer,
    LogAutomacaoSerializer,
)
from .tasks import executar_automacao

import requests
from celery.result import AsyncResult
from decouple import config
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *
from .tasks import *

# Substitua pelos seus dados reais
TENANT_ID = config('TENANT_ID')
CLIENT_ID = config('CLIENT_ID')
CLIENT_SECRET = config('CLIENT_SECRET')
WORKSPACE_ID = config('WORKSPACE_ID')
REPORT_ID = config('REPORT_ID')

class IniciarProcessoView(APIView):
    permission_classes = [IsAuthenticated]  # Requer autenticação

    def post(self, request):
        identificador = str(uuid.uuid4())  # Gera um ID único
        try:
            tarefa = envia_email_estoque.apply_async(args=[identificador])  # Dispara a tarefa
            tarefa = envia_email_estoque.apply_async(args=[identificador])  # Dispara a tarefa
        except Exception as e:
            print(f"Erro ao iniciar a tarefa: {e}")
            print(traceback.format_exc())
            return Response({"status": "erro", "mensagem": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({"task_id": tarefa.id, "status": "processando"}, status=status.HTTP_202_ACCEPTED)

class VerificarStatusView(APIView):
    permission_classes = [IsAuthenticated]  # Requer autenticação

    def get(self, request, task_id):
        resultado = AsyncResult(task_id)
        if resultado.ready():
            return Response({"status": "finalizado", "dados": resultado.result}, status=status.HTTP_200_OK)
        return Response({"status": "processando"}, status=status.HTTP_200_OK)

class ImportacaoViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]  # Requer admin user.
    queryset = ImportacaoDados.objects.all().order_by('-data_upload')
    serializer_class = ImportacaoDadosSerializer
    parser_classes = [MultiPartParser, FormParser]

    def create(self, request, *args, **kwargs):
        empresa = request.data.get("empresa")
        competencia = request.data.get("competencia")

        # Gera nova versão
        versao = ImportacaoDados.objects.filter(empresa=empresa, competencia=competencia).count() + 1
        request.data._mutable = True
        request.data["versao"] = versao
        request.data._mutable = False

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        importacao = serializer.save()

        # Dispara task assíncrona com Celery
        processar_planilha.delay(str(importacao.id))

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['get'])
    def listar_envios(self, request):
        """
        Lista todos os envios de planilhas, podendo filtrar por competência (YYYY-MM)
        """
        competencia = request.query_params.get('competencia', None)
        queryset = self.queryset

        if competencia:
            try:
                ano, mes = competencia.split('-')
                data_inicio = datetime(int(ano), int(mes), 1)
                data_fim = datetime(int(ano), int(mes) + 1, 1) if int(mes) < 12 else datetime(int(ano) + 1, 1, 1)
                queryset = queryset.filter(competencia__gte=data_inicio, competencia__lt=data_fim)
            except Exception:
                return Response({'erro': 'Formato de competência inválido. Use YYYY-MM.'}, status=400)

        serializer = self.get_serializer(queryset.order_by('-data_upload'), many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def dados_por_competencia(self, request):
        """
        Lista os dados da planilha por competência e empresa (opcionalmente versão)
        """
        competencia = request.query_params.get('competencia')
        empresa = request.query_params.get('empresa')
        versao = request.query_params.get('versao', None)

        if not competencia or not empresa:
            return Response({'erro': 'Informe os parâmetros: competencia=YYYY-MM e empresa=...' }, status=400)

        try:
            ano, mes = competencia.split('-')
            data_inicio = datetime(int(ano), int(mes), 1)
            data_fim = datetime(int(ano), int(mes) + 1, 1) if int(mes) < 12 else datetime(int(ano) + 1, 1, 1)

            qs = ImportacaoDados.objects.filter(
                empresa=empresa,
                competencia__gte=data_inicio,
                competencia__lt=data_fim,
            )

            if versao:
                qs = qs.filter(versao=int(versao))
            else:
                qs = qs.filter(ativo=True)

            importacao = qs.order_by('-versao').first()
            if not importacao:
                return Response({'erro': 'Nenhuma planilha encontrada.'}, status=404)

            linhas = LinhaPlanilha.objects.filter(importacao=importacao)
            serializer = LinhaPlanilhaSerializer(linhas, many=True)
            return Response({
                "importacao": ImportacaoDados(importacao).data,
                "linhas": serializer.data
            })

        except Exception as e:
            return Response({'erro': str(e)}, status=400)
        
class PowerBIEmbedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # 1. Obter token de acesso (client credentials flow)
        token_url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"
        token_data = {
            'grant_type': 'client_credentials',
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'scope': 'https://analysis.windows.net/powerbi/api/.default'
        }
        token_response = requests.post(token_url, data=token_data)
        
        if token_response.status_code != 200:
            return Response({'error': 'Falha ao obter token de acesso'}, status=status.HTTP_400_BAD_REQUEST)

        access_token = token_response.json().get('access_token')

        # 2. Gerar token de incorporação
        embed_url = f"https://api.powerbi.com/v1.0/myorg/groups/{WORKSPACE_ID}/reports/{REPORT_ID}/GenerateToken"
        embed_headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        embed_body = {
            'accessLevel': 'View'
        }

        embed_response = requests.post(embed_url, headers=embed_headers, json=embed_body)
        if embed_response.status_code != 200:
            return Response({'error': 'Falha ao gerar embed token'}, status=status.HTTP_400_BAD_REQUEST)

        embed_data = embed_response.json()

        return Response({
            'embedToken': embed_data.get('token'),
            'embedUrl': f"https://app.powerbi.com/reportEmbed?reportId={REPORT_ID}&groupId={WORKSPACE_ID}",
            'reportId': REPORT_ID
        })
    
class IntervalScheduleViewSet(viewsets.ModelViewSet):
    queryset = IntervalSchedule.objects.all()
    serializer_class = IntervalScheduleSerializer

class CrontabScheduleViewSet(viewsets.ModelViewSet):
    queryset = CrontabSchedule.objects.all()
    serializer_class = CrontabScheduleSerializer

class PeriodicTaskViewSet(viewsets.ModelViewSet):
    queryset = PeriodicTask.objects.all()
    serializer_class = PeriodicTaskSerializer

class AutomacaoViewSet(viewsets.ModelViewSet):
    queryset = Automacao.objects.all()
    serializer_class = AutomacaoSerializer

    @action(detail=True, methods=['post'])
    def executar(self, request, pk=None):
        """
        Executa uma automação manualmente.
        """
        automacao = self.get_object()
        executar_automacao.delay(automacao.id)
        return Response({"status": "Automação iniciada"}, status=status.HTTP_202_ACCEPTED)

class LogAutomacaoViewSet(viewsets.ModelViewSet):
    queryset = LogAutomacao.objects.all()
    serializer_class = LogAutomacaoSerializer