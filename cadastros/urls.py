from django.urls import path, include

from .views import *
from .api import *


app_name = 'cadastros'
urlpatterns = [
    ### UNIDADE E GERENTE, TESTANDO O TIPO DE INCLUSÃO DA ROTA

    path('api/cidades/', CidadeList.as_view(), name='api-cidade-list'),
    path('api/cidades/<int:pk>/', CidadeCRUD.as_view(), name='api-cidade-crud'),
    path('api/pessoasfisicas/', PessoaFisicaList.as_view(), name='pessoas_fisicas'),
    path('api/pessoasfisicas/<int:pk>', PessoaFisicaList.as_view(), name='pessoas-fisicas-crud'),

#API PARA PJ
    path('api/pessoajuridica/', PessoaJuridicaListCreate.as_view(), name='pessoas-juridicas'),
    path('api/pessoajuridica/<int:pk>', PessoaJuridicaCRUD.as_view(), name='pessoas-fisicas-crud'),

#API PARA UNIDADE0
    path('api/unidade/', UnidadeListCreate.as_view(), name='pessoas-juridicas'),
    path('api/unidade/<int:pk>', UnidadesCRUD.as_view(), name='pessoas-fisicas-crud'),

#API PARA GERENTES
    path('api/gerente/', GerenteListCreate.as_view(), name='gerentes'),
    path('api/gerente/<int:pk>',GerenteCRUD.as_view(), name='gerentes-crud'),

    #cidades
    path('cidades/list/',GetCidadesListView.as_view(),name='cidades-list'),
    path('cidades/',CidadeListView.as_view(), name='cidades'),
    path('cidades/create/', CidadeListView.as_view(), name='cidades-create'),

    #################### PESSOA JURIDICA ##################

    path('pessoajuridica/list/', GetPessoaJuridicaListView.as_view(), name='pessoa-juridica-list'),
    path('pessoajuridica/', PessoaJuridicaListView.as_view(), name='pessoa-juridica'),
    path('pessoajuridica/create/', CidadeListView.as_view(), name='pessoa-juridica-create'),

    #################### UNIDADE ##################

    path('unidade/list/', GetUnidadesListView.as_view(), name='unidade-list'),
    path('unidade/', UnidadeListView.as_view(), name='unidade'),
    path('unidade/create/', CidadeListView.as_view(), name='unidade-create'),

    #################### UNIDADE ##################

    path('gerente/list/', GetGerentesListView.as_view(), name='gerente-list'),

    path('gerente/', GerenteListView.as_view(), name='gerente'),

    path('gerente/create/', CidadeListView.as_view(), name='gerente-create'),

    path('gerente/<int:id>/edit/', CidadeListView.as_view(), name='unidade-create'),

    path('gerente/<int:id>/delete/', CidadeListView.as_view(), name='unidade-create'),

]