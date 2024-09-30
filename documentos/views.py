
from rest_framework import generics
from .models import Politica
from .serializers import *

class DocumentosView(generics.ListAPIView):
    queryset = Politica.objects.all()
    serializer_class = DocumentosSerializer

class PoliticasListView(generics.ListAPIView):
    queryset = Politica.objects.all()
    serializer_class = PoliticaListSerializer


class PoliticasCreateView(generics.CreateAPIView):
    queryset = Politica.objects.all()
    serializer_class = PoliticaCreateSerializer

