
from django import forms
import re

class PhoneNumberField(forms.CharField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("max_length", 14)  # Formato (##) ####-####
        kwargs.setdefault("widget", forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "(00) 0000-0000"
        }))
        super().__init__(*args, **kwargs)

    def clean(self, value):
        value = super().clean(value)
        if value:
            # Remove tudo que não for número
            phone_number = re.sub(r'\D', '', value)

            # Verifica se tem 10 dígitos (excluindo DDD)
            if len(phone_number) != 10:
                raise forms.ValidationError("O número de telefone deve ter 10 dígitos.")

            return f"({phone_number[:2]}) {phone_number[2:6]}-{phone_number[6:]}"
        return value


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

        return cpf