from django.urls import path, include
from .api import *

app_name = 'cadastros'
urlpatterns = [
    path('api/cidades/', CidadeList.as_view(), name='cidade_list_create'),
    path('api/bairros/', BairroList.as_view(), name='bairro_list_create'),
    path('api/logradouros/', LogradouroList.as_view(), name='logradouro_list_create'),
    path('api/pessoas/', PessoaFisicaList.as_view(), name='pessoa_fisica_list_create'),
]