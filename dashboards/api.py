from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .tasks import *
import uuid
from celery.result import AsyncResult
import traceback

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
