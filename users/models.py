from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

# Create your models here.


class User(AbstractUser):
    first_name = models.CharField(max_length=255,verbose_name="Nome",null=True, blank=True)
    last_name = models.CharField(max_length=255,verbose_name="Sobrenome",null=True, blank=True)
    username = models.CharField(max_length=30, unique=True, blank=True, null=True, )
    email = models.EmailField(unique=True, verbose_name="E-mail")
    cpf = models.CharField(max_length=11,verbose_name="CPF", blank=True, null=True)
    telefone = models.CharField(max_length=11,verbose_name="Telefone", blank=True, null=True)
    data_nascimento = models.DateField(blank=True, null=True,verbose_name="Data de Nascimento")
    password_set = models.BooleanField(default=False,blank=True)
    groups = models.ManyToManyField(Group, related_name='custom_user_set',blank=True, null=True)
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_permissions_set',blank=True, null=True)
    

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["cpf","data_nascimento","username"]
    EMAIL_FIELD = 'email'

    def to_dict_verbose(self,fields):
        data = {}
        for field in self._meta.fields:
                if field.name in fields:
                    verbose_name = field.verbose_name
                    value = getattr(self, field.attname)
                    data[verbose_name] = value
        return data
