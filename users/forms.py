from django import forms
from django.contrib.auth import get_user_model
import re
from enterprise.forms.custom_fields import *
from bootstrap_modal_forms.forms import BSModalModelForm
from django.contrib.auth.models import Group
from .widgets import DualListWidget
User = get_user_model()

  # Retorna apenas os números do CPF para salvar no banco
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'username', 'email', 'cpf', 'telefone',
            'data_nascimento', 'groups', 'user_permissions', 'is_admin', 'is_staff'
        ]
        # Exclude 'password_set' if it’s not meant to be edited directly by users

    # Custom widgets with attributes
    widgets = {
        'first_name': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite seu nome',
        }),
        'last_name': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite seu sobrenome',
        }),
        'username': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Escolha um nome de usuário',
        }),
        'email': forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite seu e-mail',
        }),
        'cpf': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite seu CPF (somente números)',
            'maxlength': '11',
        }),
        'telefone': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite seu telefone (somente números)',
            'maxlength': '11',
        }),
        'data_nascimento': forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',  # HTML5 date picker
        }),
        'groups': forms.SelectMultiple(attrs={
            'class': 'form-control',
        }),
        'user_permissions': forms.SelectMultiple(attrs={
            'class': 'form-control',
        }),
        'is_admin': forms.CheckboxInput(attrs={
            'class': 'form-check-input',
        }),
        'is_staff': forms.CheckboxInput(attrs={
            'class': 'form-check-input',
        }),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Optional: Add custom validation or tweak widget attributes dynamically
        self.fields['cpf'].help_text = "Digite apenas os 11 dígitos do CPF."
        self.fields['telefone'].help_text = "Digite apenas os 11 dígitos do telefone."



class GroupModalForm(BSModalModelForm):

    class Meta:
        model = Group
        fields = ['name']
        labels =    {
            'name' : 'Nome do grupo'
        }
        widgets = {
            'name' : forms.TextInput(attrs={
                'class': 'form-control text-sm',
                'placeholder' : 'Grupo',
                'label' : 'Nome'
            }),
        }
from django.contrib.auth.models import Permission
from .widgets import DualListWidget
class GroupEditForm(BSModalModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=DualListWidget(),
        required=False,
    )
    class Meta:
        model = Group
        fields = ['name', 'permissions']
        labels = {
            'name' : 'Nome do grupo',
            'permissions' : 'Permissões'
        }
        widgets = {
            'name' : forms.TextInput(
                attrs={
                    'class': 'form-control text-sm',

                }
            )
        }


class UserModalForm(BSModalModelForm):

    cpf = CPFField()
    telefone = PhoneNumberField()

    class Meta:
        model = User
        fields = [
            'email',
            'username',
            'first_name',
            'last_name',
            'cpf',
            'telefone',
            'data_nascimento',
            'groups',
            'user_permissions',
            'is_admin',
            'is_staff'
        ]
        widgets = {
            'email' : forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder' : 'email@maissabor.ind.br',
            }),
            'username' : forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder' : 'Usuário',
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Sobrenome',
            }),
            'data_nascimento': forms.DateInput(attrs={
                'class': 'form-control',
                'placeholder' : 'Data Nascimento',
                'type' : 'date'
            }),
            'groups': DualListWidget(attrs={
                'class': 'form-control',
            }),
            'user_permissions': DualListWidget(attrs={
                'class': 'form-control',
            }),
            'is_admin': forms.CheckboxInput(attrs={
                'class': 'form-check-input form-control',
            }),
            'is_staff': forms.CheckboxInput(attrs={
                'class': 'form-check-input form-control',
            }),


        }
        labels = {
            'email' : 'E-mail',
            'username' : 'Nome',
            'groups' : 'Grupos do Usuário',
            'user_permissions' : 'Permissões do Usuário'
        }

from django.contrib.auth.models import Permission
from .widgets import DualListWidget
