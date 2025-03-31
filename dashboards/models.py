from django.db import models

# Create your models here.

TIPO_AUTOMACAO = [
    ('E', 'E-MAIL'),
    ('D', 'DASHBOARD')
]

METODO = [
    ('GET', 'GET'),
    ('POST', 'POST'),
    ('OPTIONS', 'OPTIONS')
]

TIPO_EXECUCAO = [
    ('MANUAL', 'M'),
    ('AUTOMÁTICA', 'A')
]

class Automacao(models.Model):
    nome = models.CharField(max_length=255)
    tipo = models.CharField(choices=TIPO_AUTOMACAO, max_length=2)
    url = models.URLField()
    token = models.CharField(max_length=255)
    ativo = models.BooleanField(default=True)
    recorrencia = models.CharField()
    dt_criacao = models.DateField()

class LogAutomacao(models.Model):
    hash = models.CharField(max_length=255)
    automacao = models.ForeignKey(Automacao, on_delete=models.CASCADE)
    data_hora = models.DateTimeField()
    tipo_execucao = models.CharField(choices=TIPO_EXECUCAO)
    resposta = models.JSONField()
    status = models.IntegerField()


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


