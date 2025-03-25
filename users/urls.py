from django.urls import path, include
from .api import *
from django.contrib.auth.views import logout_then_login
from .views import *

app_name = 'users'

urlpatterns = [

    ## AQUI SAO AS API PARA O VUE... FOCAR NISSO
    path("auth-login/", obtain_auth_token, name='auth-login'),
    path("api/list/", user_list, name='user_list'),
    path("api/users/", UserListAPIGeneric.as_view(), name='users_list'),

    #path("create/", user_create, name='user_create'),
    #path("manage/<int:pk>/",user_crud,name="user_crud"),
    #path("perms/",manage_perms, name='manage_perms'),



### DAQUI PRA BAIXO SAO AS DO DJANGO
    path("login/", CustomLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('users/', UserListView.as_view(), name='list'),
    path('users/list/', GetUsersView.as_view(), name='user-list'),
    path('users/create/', UserCreateView.as_view(), name='create'),
    path('users/<int:pk>/edit/', UserUpdateView.as_view(), name='edit'),
    path('users/<int:pk>/delete/', UserDeleteView.as_view(), name='delete'),
    path('users/<int:user_id>/toggle_active/', ToggleActiveStatusView.as_view(), name='toggle_active'),
    path('groups/', GroupListView.as_view(), name='groups'),
    path('groups/create/' , GroupCreateView.as_view(), name='create_group'),
    path('groups/<int:pk>/edit/', GroupEditView.as_view(), name='edit_groups'),
    path('groups/<int:pk>/delete/', GroupDeleteView.as_view(), name='edit_groups'),
]

