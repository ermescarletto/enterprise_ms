
from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.


class BaseModelCadastro(models.Model):

    def get_fields(self):
        fields = []

        for field in self._meta.get_fields():
            if isinstance(field, (models.ManyToOneRel, models.ManyToManyRel)):
                continue

            field_name = field.verbose_name if hasattr(field, 'verbose_name') else field.name
            field_value = getattr(self, field.name, None)

            if isinstance(field_value, bool):
                field_value = "Sim" if field_value else "Não"
            elif isinstance(field, models.ManyToManyField):
                field_value = ', '.join([str(obj) for obj in field_value.all()])
            else:
                field_value = str(field_value) if field_value else '-'

            fields.append((field_name, field_value))

        return fields

    def get_model_name(self):
        return self._meta.verbose_name.title()

    class Meta:
        abstract = True



STATE_CHOICES = (
    ('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'),
    ('AM', 'Amazonas'), ('BA', 'Bahia'), ('CE', 'Ceará'),
    ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'),
    ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'),
    ('MS', 'Mato Grosso do Sul'), ('MG', 'Minas Gerais'),
    ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'),
    ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'),
    ('RN', 'Rio Grande do Norte'), ('RS', 'Rio Grande do Sul'),
    ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'),
    ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins')
)

class Cidade(models.Model):
    nome = models.CharField(max_length=60)
    estado = models.CharField(max_length=2, choices=STATE_CHOICES)
    cep_de = models.IntegerField()
    cep_ate = models.IntegerField()
    def __unicode__(self):
        return self.nome

    def __str__(self):
        return f'{self.nome} - {self.estado}'

    class Meta:
        verbose_name = 'Cadastro de Cidades'
        verbose_name_plural = 'Cidades'

class Bairro(models.Model):
    nome = models.CharField(max_length=60)
    cidade = models.ForeignKey(Cidade, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.nome} - {self.cidade}'

    class Meta:
        unique_together = ['nome', 'cidade']
        ordering = ['cidade', 'nome']


class Logradouro(models.Model):
    nome = models.CharField(max_length=60)
    bairro = models.ForeignKey(Bairro, on_delete=models.CASCADE)
    cidade = models.ForeignKey(Cidade, on_delete=models.CASCADE)
    cep = models.IntegerField()
    class Meta:
        unique_together = ['nome', 'bairro', 'cidade']
        ordering = ['cidade']

    def __str__(self):
        return '%d: %s' % (self.nome, self.cidade)


class PessoaFisica(models.Model):
    SEXO = (
        ('M', 'MASCULINO'), ('F', 'FEMININO')
    )
    nome = models.CharField(max_length=255)
    data_nascimento = models.DateField(null=True)
    cpf = models.CharField(max_length=11, null=True, blank=True)
    sexo = models.CharField(choices=SEXO)
    email = models.EmailField(blank=True, null=True)
    telefone = models.CharField(max_length=255, null=True, blank=True)


class EnderecoPessoaFisica(models.Model):
    TIPOENDERECO = (
        ('R', 'RESIDENCIAL'),
        ('C', 'COMERCIAL'),
        ('O', 'OUTROS')
    )
    principal = models.BooleanField()
    pessoa = models.ForeignKey(PessoaFisica, related_name='enderecos', on_delete=models.CASCADE)
    cidade = models.ForeignKey(Cidade, on_delete=models.CASCADE)
    bairro = models.ForeignKey(Bairro, on_delete=models.CASCADE)
    logradouro = models.ForeignKey(Logradouro, on_delete=models.CASCADE)
    tipo_endereco = models.CharField(choices=TIPOENDERECO, max_length=1)
    numero = models.IntegerField(blank=True, null=True)
    cep = models.CharField(max_length=8)

    class Meta:
        unique_together = ['pessoa', 'principal']
        ordering = ['-id']


class ContatoPessoaFisica(models.Model):
    TIPOCONTATO = (
        ('T', 'TELEFONE'),
        ('C', 'CELULAR'),
        ('E', 'EMAIL'),
        ('O', 'OUTROS')
    )
    principal = models.BooleanField()
    pessoa = models.ForeignKey(PessoaFisica, related_name='contatos', on_delete=models.CASCADE)
    tipo_contato = models.CharField(choices=TIPOCONTATO, max_length=1)
    contato = models.CharField(max_length=60)
    principal = models.BooleanField(default=False)

    class Meta:
        unique_together = ['pessoa', 'principal']

class PessoaJuridica(models.Model):
    nome_fantasia = models.CharField(max_length=255)
    razao_social = models.CharField(max_length=255)
    cnpj = models.CharField(max_length=14, null=False, blank=False)
    inscricao_estadual = models.CharField(max_length=12, null=True, blank=True)
    inscricao_municipal = models.CharField(max_length=12, null=True, blank=True)
    email = models.EmailField(blank=True, null=True)
    telefone = models.CharField(max_length=255, null=True, blank=True)


class EnderecoPessoaJuridica(models.Model):
    TIPOENDERECO = (
        ('R', 'RESIDENCIAL'),
        ('C', 'COMERCIAL'),
        ('O', 'OUTROS')
    )
    principal = models.BooleanField()
    pessoa_juridica = models.ForeignKey(PessoaJuridica, related_name='enderecos', on_delete=models.CASCADE)
    cidade = models.ForeignKey(Cidade, on_delete=models.CASCADE)
    bairro = models.ForeignKey(Bairro, on_delete=models.CASCADE)
    logradouro = models.ForeignKey(Logradouro, on_delete=models.CASCADE)
    tipo_endereco = models.CharField(choices=TIPOENDERECO, max_length=1)
    numero = models.IntegerField(blank=True, null=True)
    cep = models.CharField(max_length=8)

    class Meta:
        unique_together = ['pessoa_juridica', 'principal']
        ordering = ['-id']


class ContatoPessoaJuridica(models.Model):
    TIPOCONTATO = (
        ('T', 'TELEFONE'),
        ('C', 'CELULAR'),
        ('E', 'EMAIL'),
        ('O', 'OUTROS')
    )
    principal = models.BooleanField()
    pessoa_juridica = models.ForeignKey(PessoaJuridica, related_name='contatos', on_delete=models.CASCADE)
    tipo_contato = models.CharField(choices=TIPOCONTATO, max_length=1)
    contato = models.CharField(max_length=60)
    principal = models.BooleanField(default=False)

    class Meta:
        unique_together = ['pessoa_juridica', 'principal']


class Departamento(models.Model):
    nome = models.CharField(max_length=255)

    def __str__(self):
        return self.nome

class Unidade(BaseModelCadastro):
    codigo = models.IntegerField() #codigo sistema teknisa
    nome = models.CharField(max_length=255)
    cnpj = models.CharField(max_length=14)
    empresa = models.ForeignKey(PessoaJuridica, on_delete=models.CASCADE)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome


class Gerente(BaseModelCadastro):
    usuario = models.ForeignKey('users.User', on_delete=models.CASCADE, unique=True)
    unidades = models.ManyToManyField(Unidade)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.usuario.email}"


class Cargo(models.Model):
    descricao = models.CharField(max_length=255)
    dia_festivo = models.DateField(null=True)

    def __str__(self):
        return self.descricao
