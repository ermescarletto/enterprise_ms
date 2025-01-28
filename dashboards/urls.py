from django.urls import path, include
from .views import *
from .api import *

app_name = 'dashboards'
urlpatterns = [


    path('api/dashboards/', DashboardList.as_view(), name='dashboard_list'),
    path('api/meusdashboards/<int:id>', MyDashboards.as_view(), name='my_dashboards'),

]