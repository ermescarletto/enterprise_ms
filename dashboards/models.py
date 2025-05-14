from django.db import models
import uuid
# Create your models here.

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
    url = models.URLField(blank=True, null=True)
    metodo = models.CharField(max_length=10, choices=METODO, default='GET')  # Novo campo para o método HTTP
    parametros = models.JSONField(blank=True, null=True)  # Novo campo para parâmetros da requisição
    token_param = models.CharField(max_length=255, blank=True, null=True)  # Novo campo para o token de autenticação
    token = models.CharField(max_length=255, blank=True, null=True)
    ativo = models.BooleanField(default=True)
    recorrencia = models.CharField(max_length=255, blank=True, null=True)
    dt_criacao = models.DateField(auto_created=True, auto_now=True)

class LogAutomacao(models.Model):
    hash = models.CharField(max_length=255)
    automacao = models.ForeignKey(Automacao, on_delete=models.CASCADE)
    data_hora = models.DateTimeField(auto_now_add=True)  # Alterado para auto_now_add
    tipo_execucao = models.CharField(max_length=10, choices=TIPO_EXECUCAO)
    resposta = models.JSONField()
    status = models.IntegerField()
    erro = models.TextField(blank=True, null=True)  # Novo campo para armazenar erros

class DashboardPublico(models.Model):
    nome = models.CharField(max_length=255)
    workspace_id = models.CharField(max_length=255)
    report_id = models.CharField(max_length=255)
    url_dashboard = models.TextField(blank=True, null=True)    
    ativo = models.BooleanField(default=True)
    publico = models.BooleanField(default=False)


class DashboardUnidade(models.Model):
    nome = models.CharField(max_length=255)
    unidade = models.ForeignKey('cadastros.Unidade', on_delete=models.CASCADE)
    workspace_id = models.CharField(max_length=255)
    report_id = models.CharField(max_length=255)
    url_dashboard = models.TextField(blank=True, null=True)    
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
        unique_together = ( 'competencia', 'versao')

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





class PosicaoEstoqueDia(models.Model):
    data_criacao = models.DateField(auto_created=True, auto_now=True)
    id_teknisa = models.CharField(max_length=255)
    nmorg = models.IntegerField()
    nmorganizacao = models.CharField(max_length=255)
    cdempresa = models.IntegerField()
    nmfilial = models.CharField(max_length=255)
    dtposiestq = models.DateField()
    dtref = models.DateField()
    dtimport = models.DateField()
    nmgrupprodnivel = models.CharField(max_length=255)
    nmsubprodnivel = models.CharField(max_length=255)
    nrloteesto = models.CharField(max_length=255, null=True, blank=True)
    cdlocalestoq = models.CharField(max_length=255, null=True, blank=True)
    dslocalestoq = models.CharField(max_length=255, null=True, blank=True)
    cdalmoxarife = models.CharField(max_length=255, null=True, blank=True)
    dsalmoxarife = models.CharField(max_length=255, null=True, blank=True)
    cdarvprod = models.CharField(max_length=255, null=True, blank=True)
    nmprodnivel = models.CharField(max_length=255)
    cdprodesto = models.CharField(max_length=255)
    sgunidade = models.CharField(max_length=255)
    qtestoquedia = models.DecimalField(max_digits=15, decimal_places=2)
    vrmediobrut = models.DecimalField(max_digits=15, decimal_places=2)
    vrestoqbrut = models.DecimalField(max_digits=15, decimal_places=2)
    vrmedio = models.DecimalField(max_digits=15, decimal_places=2)
    vrestoqdia = models.DecimalField(max_digits=15, decimal_places=2)
    vrcustoprod = models.DecimalField(max_digits=15, decimal_places=2)
    numdias = models.IntegerField()


