from django.db import models
import uuid
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


class ImportacaoDados(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    competencia = models.DateField(help_text="Use o primeiro dia do mês")
    versao = models.PositiveIntegerField()
    arquivo = models.FileField(upload_to="planilhas/")
    data_upload = models.DateTimeField(auto_now_add=True)
    ativo = models.BooleanField(default=False)
    status = models.CharField(
        max_length=20,
        choices=[('pendente', 'Pendente'), ('processando', 'Processando'), ('concluido', 'Concluído'), ('erro', 'Erro')],
        default='pendente'
    )

    class Meta:
        unique_together = ('empresa', 'competencia', 'versao')

    def save(self, *args, **kwargs):
        if self.ativo:
            ImportacaoDados.objects.filter(
                empresa=self.empresa,
                competencia=self.competencia,
                ativo=True
            ).update(ativo=False)
        super().save(*args, **kwargs)

class LinhaPlanilha(models.Model):
    """Cada linha da planilha importada"""
    importacao = models.ForeignKey(ImportacaoDados, on_delete=models.CASCADE, related_name='linhas')
    codigo_unidade = models.ForeignKey('cadastros.Unidade', on_delete=models.CASCADE)
    nome_unidade = models.CharField(max_length=255)
    codigo_centro_custo = models.ForeignKey('cadastros.CentroDeCusto', on_delete=models.CASCADE)
    centro_custo = models.CharField(max_length=255)
    codigo_reduzido = models.CharField(max_length=50)
    data = models.DateField()
    numero = models.CharField(max_length=50)
    conta = models.CharField(max_length=50)
    historico = models.TextField()
    debito = models.DecimalField(max_digits=15, decimal_places=2)
    credito = models.DecimalField(max_digits=15, decimal_places=2)
    saldo = models.DecimalField(max_digits=15, decimal_places=2)

