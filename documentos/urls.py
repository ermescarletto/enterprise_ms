from django.urls import path, include
from .views import *

app_name = 'documentos'
urlpatterns = [
    path('api/documentos/', DocumentosView.as_view(), name='documentos-node'),
    path('api/politicas/', PoliticasListView.as_view(), name='documentos-politica'),
    path('api/politicas/create/', PoliticasCreateView.as_view(), name='create-politica'),

]