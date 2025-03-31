from celery import shared_task
import requests
import json
import pandas as pd
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.conf import settings
from cadastros.models import Gerente
from users.models import User


@shared_task
def processar_dados(identificador):
    """Simula um processamento de dados"""
    time.sleep(5)  # Simula tempo de espera
    resultado = {"status": "finalizado", "dados": random.randint(100, 999)}
    return resultado



@shared_task
def envia_email_estoque(identificador):
    url = "https://api-zmartbi.teknisa.com"
    print('requisicao')

    payload = {}
    headers = {
        'Webtoken': 'Njc5N2NmZThlYTJmMzg3ZDljN2RlNmRkXzQ4MjQ=',
        'Cookie': 'PHPSESSID=1eodhb8grn23us5tq9jkfegg8f'
    }
    print('vai requisitar')
    response = requests.request("GET", url, headers=headers, data=payload)
    print(response)
    print(response.text)
    data = json.loads(response.text)
    df = pd.DataFrame(data)

    # Agrupar por CDFILIAL e NMSUBPRODNIVEL, somando VRESTOQDIA
    df_grouped = df.groupby(["CDFILIAL", "NMFILIAL", "NMSUBPRODNIVEL"], as_index=False)["VRESTOQDIA"].sum()
    print(df_grouped)

    # Separar por filial e enviar o email para cada gerente
    for filial_codigo, group in df_grouped.groupby("CDFILIAL"):
        # Obter o gerente responsável pela filial
        try:
            gerente = Gerente.objects.get(unidades__codigo=filial_codigo, ativo=True)
            user_email = gerente.usuario.email
            subject = f"Resumo de Estoque para a Filial {filial_codigo}"
            message = "Prezado Gerente, segue o resumo de estoque da filial."

            # Filtrar a tabela apenas para os dados da filial específica
            filial_data = group[["NMFILIAL", "NMSUBPRODNIVEL", "VRESTOQDIA"]]
            table_html = filial_data.to_html(index=False)

            # Garantir que o HTML seja limpo e não tenha dados sobrepostos
            table_html_cleaned = table_html.replace('<table border="1" class="dataframe">', '<table class="table">')

            # Enviar e-mail com o HTML no corpo
            email = EmailMessage(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,  # Assumindo que você tem um e-mail configurado no Django settings
                [user_email],
            )
            email.content_subtype = "html"  # Definir conteúdo como HTML
            email.body = f"<html><head><title>Resumo de Estoque</title></head><body><h2>Resumo de Estoque</h2>{table_html_cleaned}</body></html>"
            email.send()
            print(f"E-mail enviado para {user_email}")
        except Gerente.DoesNotExist:
            print(f"Nenhum gerente encontrado para a filial {filial_codigo}")

    # Simula um processamento de dados
    resultado = {"status": "finalizado", "dados": response.text}
    return resultado
