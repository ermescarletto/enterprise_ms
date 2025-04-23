from rest_framework.generics import *
from .models import *
from .serializers import *



class EquipeListView(ListAPIView):
    queryset = Equipe.objects.all()
    serializer_class = EquipeSerializer