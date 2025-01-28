from django.shortcuts import render
from django.views.generic import TemplateView

from django.shortcuts import redirect


class Index(TemplateView):

    template_name = 'index.html'


