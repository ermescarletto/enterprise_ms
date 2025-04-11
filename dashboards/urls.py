from django.urls import path, include
from .views import *
from .api import *
from rest_framework.routers import DefaultRouter


app_name = 'dashboards'
urlpatterns = [
    path("task/iniciar/", IniciarProcessoView.as_view(), name="iniciar_processo"),
    path("task/status/<str:task_id>/", VerificarStatusView.as_view(), name="verificar_status"),
    path('', Dashboards.as_view(), name='dashboards'),
    path('dados/', ImportacaoViewSet.as_view(), name='importa_dados'),
    #path('api/meusdashboards/<int:id>', MyDashboards.as_view(), name='my_dashboards'),

]