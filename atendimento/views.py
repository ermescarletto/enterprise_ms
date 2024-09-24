from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from .models import Equipe, TipoAtendimento, Chamado
from .serializers import EquipeSerializer, TipoAtendimentoSerializer, ChamadoSerializer






class EquipeListCreate(generics.ListCreateAPIView):
    queryset = Equipe.objects.all()
    serializer_class = EquipeSerializer
    permission_classes = [IsAuthenticated,DjangoModelPermissions]

class EquipeCRUD(generics.RetrieveUpdateDestroyAPIView):
    queryset = Equipe.objects.all()
    serializer_class = EquipeSerializer
    permission_classes = [IsAuthenticated,DjangoModelPermissions]


class EquipeViewSet(viewsets.ModelViewSet):
    queryset = Equipe.objects.all()
    serializer_class = EquipeSerializer
    permission_classes = [IsAuthenticated]



class TipoAtendimentoViewSet(viewsets.ModelViewSet):
    queryset = TipoAtendimento.objects.all()
    serializer_class = TipoAtendimentoSerializer
    permission_classes = [IsAuthenticated]

class ChamadoViewSet(viewsets.ModelViewSet):
    queryset = Chamado.objects.all()
    serializer_class = ChamadoSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'], url_path='direcionar')
    def direcionar_para_equipe(self, request, pk=None):
        chamado = self.get_object()
        equipe_id = request.data.get('equipe_id')
        equipe = Equipe.objects.get(id=equipe_id)
        try:
            chamado.direcionar_para_equipe(equipe)
            return Response({'status': 'Chamado direcionado'}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], url_path='atender')
    def atender_chamado(self, request, pk=None):
        chamado = self.get_object()
        usuario = request.user
        chamado.atender_chamado(usuario)
        return Response({'status': 'Chamado em atendimento'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='fechar')
    def fechar_chamado(self, request, pk=None):
        chamado = self.get_object()
        chamado.fechar_chamado()
        return Response({'status': 'Chamado fechado'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='reabrir')
    def reabrir_chamado(self, request, pk=None):
        chamado = self.get_object()
        usuario = request.user
        if usuario.is_superuser:
            chamado.reabrir_chamado(usuario)
            return Response({'status': 'Chamado reaberto'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Você não tem permissão para reabrir este chamado.'}, status=status.HTTP_403_FORBIDDEN)

    @action(detail=True, methods=['post'], url_path='cancelar')
    def cancelar_chamado(self, request, pk=None):
        chamado = self.get_object()
        chamado.cancelar_chamado()
        return Response({'status': 'Chamado cancelado'}, status=status.HTTP_200_OK)
