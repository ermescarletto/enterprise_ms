from django.urls import path, include
from .views import *
from .api import *

app_name = 'cadastros'
urlpatterns = [

    #path('api/cidades/', CidadeList.as_view(), name='cidade_list_create'),
    path('api/pessoasfisicas/', PessoaFisicaList.as_view(), name='pessoas_fisicas'),
    path('api/pessoasfisicas/<int:id>', PessoaFisicaList.as_view(), name='pessoas_fisicas')

]