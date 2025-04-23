from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from .tasks import *
import uuid
from celery.result import AsyncResult
import traceback
from rest_framework import viewsets
from .serializers import *
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser


class IniciarProcessoView(APIView):
    permission_classes = [IsAuthenticated]  # Requer autenticação

    def post(self, request):
        identificador = str(uuid.uuid4())  # Gera um ID único
        try:
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
        






class ImportacaoViewSet(viewsets.ModelViewSet):
    # ... código existente ...

    @action(detail=False, methods=['get'])
    def posicoes_estoque(self, request):
        """
        Retorna as posições do estoque filtrando por data de referência (DTREF).
        """
        data_referencia = request.query_params.get('data_referencia', None)

        if not data_referencia:
            return Response({'erro': 'O parâmetro data_referencia é obrigatório no formato YYYY-MM-DD.'}, status=400)

        try:
            # Converte a data de referência para o formato datetime
            data_referencia = datetime.strptime(data_referencia, "%Y-%m-%d").date()

            # Filtra as posições do estoque pela data de referência
            posicoes = PosicaoEstoqueDia.objects.filter(dtref=data_referencia)

            if not posicoes.exists():
                return Response({'erro': 'Nenhuma posição de estoque encontrada para a data de referência fornecida.'}, status=404)

            # Serializa os dados
            serializer = PosicaoEstoqueDiaSerializer(posicoes, many=True)
            return Response(serializer.data, status=200)

        except ValueError:
            return Response({'erro': 'O formato da data de referência é inválido. Use YYYY-MM-DD.'}, status=400)