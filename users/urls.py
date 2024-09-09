from django.urls import path, include
from .api import *
from django.contrib.auth.views import logout_then_login


app_name = 'users'

urlpatterns = [
    path("login/", obtain_auth_token, name='login'),
    path("list/", user_list, name='user_list'),
    path("create/", user_create, name='user_create'),
    path("manage/<int:pk>/",user_crud,name="user_crud"),
    path("perms/",manage_perms, name='manage_perms'),
]

