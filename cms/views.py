from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.shortcuts import redirect

class Index(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'
    login_url = 'auth/login/'  # Defina a URL para onde os usuários não autenticados serão redirecionados
