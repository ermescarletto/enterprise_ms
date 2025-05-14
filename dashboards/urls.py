from django.urls import path, include
from .views import *
from .api import *
from rest_framework.routers import DefaultRouter


router = DefaultRouter()

router.register(r'interval-schedules', IntervalScheduleViewSet, basename='interval-schedule')
router.register(r'crontab-schedules', CrontabScheduleViewSet, basename='crontab-schedule')
router.register(r'periodic-tasks', PeriodicTaskViewSet, basename='periodic-task')
router.register(r'automacoes', AutomacaoViewSet, basename='automacao')
router.register(r'logs', LogAutomacaoViewSet, basename='logautomacao')
router.register(r'dados', ImportacaoViewSet, basename='importacao')

app_name = 'dashboards'
urlpatterns = [
    path("task/iniciar/", IniciarProcessoView.as_view(), name="iniciar_processo"),
    path("task/status/<str:task_id>/", VerificarStatusView.as_view(), name="verificar_status"),
    path('',include(router.urls)),
    path('api/powerbi-embed/', PowerBIEmbedView.as_view(), name='powerbi-embed'),
]