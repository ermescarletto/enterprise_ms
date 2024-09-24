from django.db import models
from users.models import User
from django.utils import timezone



class Equipe(models.Model):
    nome = models.CharField(max_length=100)
    usuarios = models.ManyToManyField(User, related_name='equipes')
    codigo = models.CharField(max_length=5)
    def __str__(self):
        return self.nome

class TipoAtendimento(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    slo = models.DurationField(help_text="Objetivo de nível de serviço, por exemplo, 2 horas.")
    sla = models.DurationField(help_text="Acordo de nível de serviço, por exemplo, 4 horas.")
    equipe = models.ForeignKey(Equipe, on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return self.nome

    def calcular_sla_vencido(self, chamado):
        """Verifica se o SLA foi violado para um chamado específico."""
        tempo_passado = timezone.now() - chamado.criado_em
        return tempo_passado > self.sla

    def calcular_slo_alcancado(self, chamado):
        """Verifica se o SLO foi atingido para um chamado específico."""
        tempo_passado = timezone.now() - chamado.criado_em
        return tempo_passado <= self.slo


class Chamado(models.Model):
    STATUS = (
        ('NO', 'NOVO'),
        ('AB', 'AGUARDANDO ATENDIMENTO'),
        ('AT', 'EM ATENDIMENTO'),
        ('FE', 'FECHADO'),
        ('CA', 'CANCELADO'),
    )
    codigo = models.CharField(max_length=255)
    tipo_atendimento = models.ForeignKey(TipoAtendimento, on_delete=models.CASCADE)
    resumo = models.CharField(max_length=255)
    descricao = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices=STATUS, default='NO')
    usuario_criador = models.ForeignKey(User, related_name='chamados_criados', on_delete=models.CASCADE)
    usuario_atendente = models.ForeignKey(User, related_name='chamados_atendidos', on_delete=models.SET_NULL, null=True, blank=True)
    equipe_atendente = models.ForeignKey(Equipe, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.resumo

    def direcionar_para_equipe(self, equipe):
        """Direciona o chamado para uma equipe e muda o status para 'AGUARDANDO ATENDIMENTO'."""
        if equipe.tipos_atendimento.filter(id=self.tipo_atendimento.id).exists():
            self.equipe_atendente = equipe
            self.status = 'AB'
            self.save()
        else:
            raise ValueError(f"A equipe '{equipe.nome}' não está autorizada a atender o tipo de atendimento '{self.tipo_atendimento.nome}'.")

    def atender_chamado(self, usuario):
        """Método para atender o chamado, mudando o status para EM ATENDIMENTO e atribuindo o atendente."""
        if self.status == 'AB' and usuario in self.equipe_atendente.usuarios.all():
            self.status = 'AT'
            self.usuario_atendente = usuario
            self.save()

    def fechar_chamado(self):
        """Método para fechar o chamado, mudando o status para FECHADO."""
        if self.status == 'AT':
            self.status = 'FE'
            self.save()

    def reabrir_chamado(self, usuario):
        """Método para reabrir o chamado, que só pode ser executado por administradores."""
        if self.status == 'FE' and usuario.is_superuser:
            self.status = 'NO'
            self.save()

    def cancelar_chamado(self):
        """Método para cancelar o chamado."""
        if self.status in ['NO', 'AB', 'AT']:
            self.status = 'CA'
            self.save()

    @property
    def is_aberto(self):
        return self.status == 'AB'

    @property
    def is_fechado(self):
        return self.status == 'FE'

class AnexoChamado(models.Model):
    CHAMADO_ANEXOS_LIMIT = 10 * 1024 * 1024  # Limite de 10MB por arquivo

    chamado = models.ForeignKey(Chamado, related_name='anexos', on_delete=models.CASCADE)
    arquivo = models.FileField(upload_to='')  # Definido abaixo no método estático
    tipo_arquivo = models.CharField(max_length=50)
    criado_em = models.DateTimeField(auto_now_add=True)
    enviado_por = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Anexo do chamado {self.chamado.id} por {self.enviado_por.username}"

    def tamanho_valido(self):
        """Verifica se o tamanho do arquivo é permitido."""
        return self.arquivo.size <= self.CHAMADO_ANEXOS_LIMIT

    @staticmethod
    def chamado_directory_path(instance, filename):
        """Gera o caminho de upload baseado no ID do chamado."""
        return f'chamados/{instance.chamado.id}/anexos/{filename}'

    def save(self, *args, **kwargs):
        """Sobrescreve o método save para adicionar o caminho dinâmico de upload."""
        self.arquivo.upload_to = self.chamado_directory_path(self, self.arquivo.name)
        super(AnexoChamado, self).save(*args, **kwargs)


class ComentarioChamado(models.Model):
    chamado = models.ForeignKey(Chamado, related_name='comentarios', on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    comentario = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentário por {self.usuario.username} no chamado {self.chamado.id}"


class AnexoComentario(models.Model):
    COMENTARIO_ANEXOS_LIMIT = 10 * 1024 * 1024  # Limite de 10MB por arquivo

    comentario = models.ForeignKey(ComentarioChamado, related_name='anexos', on_delete=models.CASCADE)
    arquivo = models.FileField(upload_to='')  # Definido abaixo no método estático
    tipo_arquivo = models.CharField(max_length=50)
    criado_em = models.DateTimeField(auto_now_add=True)
    enviado_por = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Anexo do comentário {self.comentario.id} por {self.enviado_por.username}"

    def tamanho_valido(self):
        """Verifica se o tamanho do arquivo é permitido."""
        return self.arquivo.size <= self.COMENTARIO_ANEXOS_LIMIT

    @staticmethod
    def comentario_directory_path(instance, filename):
        """Gera o caminho de upload baseado no ID do comentário."""
        return f'comentarios/{instance.comentario.id}/anexos/{filename}'

    def save(self, *args, **kwargs):
        """Sobrescreve o método save para adicionar o caminho dinâmico de upload."""
        self.arquivo.upload_to = self.comentario_directory_path(self, self.arquivo.name)
        super(AnexoComentario, self).save(*args, **kwargs)
