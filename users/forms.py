from django import forms
from django.contrib.auth import get_user_model
import re


User = get_user_model()


class CPFField(forms.CharField):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("max_length", 14)  # Formato: 000.000.000-00
        kwargs.setdefault("widget", forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "000.000.000-00"
        }))
        super().__init__(*args, **kwargs)

    def clean(self, value):
        value = super().clean(value)
        if not value:
            return value

        # Remove pontos e traço
        cpf = re.sub(r"[^0-9]", "", value)

        if len(cpf) != 11 or not cpf.isdigit():
            raise forms.ValidationError("CPF inválido. Insira um CPF válido no formato 000.000.000-00.")

        return cpf  # Retorna apenas os números do CPF para salvar no banco
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'cpf', 'telefone', 'data_nascimento', 'is_active', 'is_staff', 'is_admin']
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}),
        }



from bootstrap_modal_forms.forms import BSModalModelForm


class UserModalForm(BSModalModelForm):

    cpf = CPFField()
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

