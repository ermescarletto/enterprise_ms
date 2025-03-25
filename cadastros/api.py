from django.urls import reverse_lazy
from django.shortcuts import render
from rest_framework import generics
from .models import *
from .serializers import *
# Create your views here.


class CidadeList(generics.ListCreateAPIView):
    queryset = Cidade.objects.all()
    serializer_class = CidadeSerializer

class CidadeCRUD(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cidade.objects.all()
    serializer_class = CidadeSerializer

class BairroList(generics.ListCreateAPIView):
    queryset = Bairro.objects.all()
    serializer_class = BairroSerializer

class BairroCRUD(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bairro.objects.all()
    serializer_class = BairroSerializer

class LogradouroList(generics.ListCreateAPIView):
    queryset = Logradouro.objects.all()
    serializer_class = LogradouroSerializer

class LogradouroCRUD(generics.RetrieveUpdateDestroyAPIView):
    queryset = Logradouro.objects.all()
    serializer_class = LogradouroSerializer

class PessoaFisicaList(generics.ListCreateAPIView):
    queryset = PessoaFisica.objects.all()
    serializer_class = PessoaFisicaSerializerCompleto

class PessoasCRUD(generics.RetrieveUpdateDestroyAPIView):
    queryset = PessoaFisica.objects.all()
    serializer_class = PessoaFisicaSerializer

class EnderecoPessoaFisicaList(generics.ListCreateAPIView):
    queryset = EnderecoPessoaFisica.objects.all()
    serializer_class = EnderecoPessoaFisicaSerializer



#### API PESSOA JURIDICA PARA VUE ######


class PessoaJuridicaListCreate(generics.ListCreateAPIView):
    queryset = PessoaJuridica.objects.all()
    serializer_class = PessoaJuridicaSerializerCompleto

class PessoaJuridicaCRUD(generics.RetrieveUpdateDestroyAPIView):
    queryset = PessoaFisica.objects.all()
    serializer_class = PessoaJuridicaSerializerCompleto


###### UNIDADE #######

class UnidadeListCreate(generics.ListCreateAPIView):
    queryset = Unidade.objects.all()
    serializer_class = UnidadeSerializerCompleto

class UnidadesCRUD(generics.RetrieveUpdateDestroyAPIView):
    queryset = Unidade.objects.all()
    serializer_class = UnidadeSerializerCompleto


##### GERENTE ####### DIA 1
#### PERSEVERANÇA E FÉ ######

class GerenteListCreate(generics.ListCreateAPIView):
    queryset = Gerente.objects.all()
    serializer_class = GerenteSerializerCompleto

class GerenteCRUD(generics.RetrieveUpdateDestroyAPIView):
    queryset = Gerente.objects.all()
    serializer_class = GerenteSerializerCompleto