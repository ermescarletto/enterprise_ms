from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'cpf', 'telefone', 'data_nascimento', 'is_active', 'is_staff', 'is_admin']
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}),
        }
