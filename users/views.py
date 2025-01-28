from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
# Create your views here.

class CustomLoginView(LoginView):
    template_name = "users/login.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('cms:index')  # Replace 'home' with your app's home view name