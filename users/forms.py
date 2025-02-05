from django import forms
from django.contrib.auth import get_user_model
import re
from enterprise.forms.custom_fields import *
from bootstrap_datepicker_plus.widgets import DatePickerInput
from bootstrap_modal_forms.forms import BSModalModelForm
from django.contrib.auth.models import Group

User = get_user_model()

  # Retorna apenas os números do CPF para salvar no banco
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'cpf', 'telefone', 'data_nascimento', 'is_active', 'is_staff', 'is_admin']
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}),
        }


class GroupModalForm(BSModalModelForm):

    class Meta:
        model = Group
        fields = ['name']

class GroupEditForm(BSModalModelForm):

    class Meta:
        model = Group
        fields = ['name', 'permissions']

class UserModalForm(BSModalModelForm):

    cpf = CPFField()
    telefone = PhoneNumberField()
    data_nascimento = forms.DateField(widget=DatePickerInput(options={"format": "MM/DD/YYYY"}))

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


        }
        labels = {
            'email' : 'E-mail',
            'username' : 'Nome de Usuário',
        }

