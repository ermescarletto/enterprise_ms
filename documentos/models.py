from django.db import models

class Politica(models.Model):
    empresa = models.ForeignKey('cadastros.Empresa', on_delete=models.PROTECT)
    departamento = models.ForeignKey( 'cadastros.Departamento', on_delete=models.PROTECT)
    codigo_politica = models.CharField(max_length=15,unique=True)
    titulo_politica = models.CharField(max_length=255)
    texto_politica = models.TextField()
    criado_em = models.DateTimeField(auto_now=True, auto_created=True)

class AnexosPolitica(models.Model):
    politica = models.ForeignKey(Politica, on_delete=models.CASCADE)
    anexo = models.FileField(upload_to='politicas/anexos/{}/'.format(politica))
    comentario = models.CharField(max_length=255, null=True, blank=True)
    criado_em = models.DateTimeField(auto_now=True, auto_created=True)

class ProcedimentoPadrao(models.Model):
    politica = models.ForeignKey(Politica, on_delete=models.CASCADE)
    titulo_procedimento = models.CharField(max_length=255)
    texto_procedimento = models.TextField()
    anexo = models.FileField(upload_to='politicas/anexos/{}/pops/'.format(politica))

class Fluxogramas(models.Model):
    procedimento_padrao = models.ForeignKey(ProcedimentoPadrao, on_delete=models.CASCADE)
    titulo_fluxograma = models.CharField(max_length=255)
    anexo = models.FileField(upload_to='politicas/anexo/{}/pops/fluxogramas/'.format(procedimento_padrao))


