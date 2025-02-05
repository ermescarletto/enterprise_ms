from django.urls import path, include
from .views import *
from .api import *

app_name = 'dashboards'
urlpatterns = [

    path('', Dashboards.as_view(), name='dashboards'),
    #path('api/meusdashboards/<int:id>', MyDashboards.as_view(), name='my_dashboards'),

]