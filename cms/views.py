from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.shortcuts import redirect
import json
from django.core.mail import EmailMessage
from django.shortcuts import render
from .forms import UploadJSONForm



class Index(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'
    login_url = 'auth/login/'  # Defina a URL para onde os usuários não autenticados serão redirecionados



def process_json(request):
    if request.method == "POST":
        form = UploadJSONForm(request.POST, request.FILES)
        if form.is_valid():
            json_file = request.FILES["json_file"]
            email = form.cleaned_data["email"]

            # Ler o arquivo JSON
            data = json.load(json_file)

            # Converter para HTML
            html_table = generate_html_table(data)

            # Enviar e-mail
            send_email_with_table(email, html_table)

            return render(request, "cms/sucesso.html", {"email": email})

    else:
        form = UploadJSONForm()

    return render(request, "cms/json.html", {"form": form})

def generate_html_table(data):
    """Gera uma tabela HTML a partir dos dados JSON"""
    headers = [
        "NRORG", "NMORGANIZACAO", "CDEMPRESA", "NMEMPRESA", "CDFILIAL",
        "NMFILIAL", "NMPRODUTO", "SGUNIDADE", "QTESTOQDIA", "VRMEDIOBRUT",
        "VRESTOQBRUT", "VRCUSTOPROD", "NUMDIAS"
    ]

    table = "<table border='1' style='border-collapse: collapse; width: 100%; text-align: left;'>"
    table += "<tr style='background-color: #f2f2f2;'>" + "".join(f"<th>{header}</th>" for header in headers) + "</tr>"

    for item in data:
        table += "<tr>" + "".join(f"<td>{item.get(header, '')}</td>" for header in headers) + "</tr>"

    table += "</table>"
    return table

def send_email_with_table(to_email, table_html):
    """Envia um e-mail com a tabela HTML"""
    subject = "Relatório de Estoque"
    message = "Segue o relatório de estoque gerado automaticamente."
    email = EmailMessage(subject, message,'no-reply@msservice.ind.br', [to_email])
    email.content_subtype = "html"
    email.body = f"<html><body><p>{message}</p>{table_html}</body></html>"
    email.send()