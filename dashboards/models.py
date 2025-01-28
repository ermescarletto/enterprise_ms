from django.db import models

# Create your models here.



class DashboardPublico(models.Model):
    nome = models.CharField(max_length=255)
    url_dashboard = models.TextField()
    ativo = models.BooleanField(default=True)
    publico = models.BooleanField(default=False)


class DashboardUnidade(models.Model):
    nome = models.CharField(max_length=255)
    unidade = models.ForeignKey('cadastros.Unidade', on_delete=models.CASCADE)
    url_dashboard = models.TextField()
    ativo = models.BooleanField(default=True)


