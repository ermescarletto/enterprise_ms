from .models import *
from bootstrap_modal_forms.forms import BSModalModelForm
from django import forms

class FormEmpresa(BSModalModelForm):
    page_title = Empresa.get_model_name(Empresa)
    class Meta:
        model = Empresa
        fields = '__all__'
