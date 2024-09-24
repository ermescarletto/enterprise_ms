from django.urls import path, include
from .views import *

app_name = 'atendimento'
urlpatterns = [
    path('api/equipe/', EquipeListCreate.as_view(), name='cidade_list_create'),

]