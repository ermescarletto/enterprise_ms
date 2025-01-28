from django.urls import path, include
from .api import *
from django.contrib.auth.views import logout_then_login
from .views import *

app_name = 'users'

urlpatterns = [
#api_desativada    path("login/", obtain_auth_token, name='login'),
    path("login/", CustomLoginView.as_view(), name='login'),
    path("list/", user_list, name='user_list'),
    path("create/", user_create, name='user_create'),
    path("manage/<int:pk>/",user_crud,name="user_crud"),
    path("perms/",manage_perms, name='manage_perms'),
]

