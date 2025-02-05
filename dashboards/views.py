from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.


class Dashboards(LoginRequiredMixin,TemplateView):
    template_name = "dashboards/dashboards.html"
    login_url = 'auth/login/'  # Defina a URL para onde os usuários não autenticados serão redirecionados
