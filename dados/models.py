from django.db import models

# Create your models here.
class RegistroFinanceiro(models.Model):
    empresa_filial = models.CharField(max_length=255,null=True, blank=True)
    centro_custo = models.CharField(max_length=255,null=True, blank=True)
    conta = models.CharField(max_length=100,null=True, blank=True)
    competencia = models.DateField(null=True, blank=True)
    historico = models.TextField(null=True, blank=True)
    valor_contabil = models.DecimalField(max_digits=20, decimal_places=2,null=True, blank=True)

    def __str__(self):
        return f"{self.empresa_filial} - {self.competencia}"

    class Meta:
        verbose_name = "Registro Financeiro"
        verbose_name_plural = "Registros Financeiros"
        ordering = ['competencia', 'empresa_filial']    





