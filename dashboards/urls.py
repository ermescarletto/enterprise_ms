from django.urls import path, include
from .views import *
from .api import *
from rest_framework.routers import DefaultRouter



router = DefaultRouter()

router.register(r'dados', ImportacaoViewSet, basename='importacao')

app_name = 'dashboards'
urlpatterns = [

]