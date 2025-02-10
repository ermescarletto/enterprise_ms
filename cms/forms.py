from django import forms

class UploadJSONForm(forms.Form):
    json_file = forms.FileField(label="Selecione um arquivo JSON")
    email = forms.EmailField(label="E-mail para envio")
