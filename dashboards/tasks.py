from celery import shared_task
import requests
import json
import pandas as pd
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from cadastros.models import Gerente
import time
import random


@shared_task
def processar_dados(identificador):
    """Simula um processamento de dados"""
    time.sleep(5)  # Simula tempo de espera
    resultado = {"status": "finalizado", "dados": random.randint(100, 999)}


@shared_task

def envia_dados_caixa(identificador, filiais=None):
    print('INICIO')
    return {"status": "finalizado", "dados": 'Executado com sucesso'}

@shared_task
def envia_email_estoque(identificador, filiais=None):
    print('INICIO')
    url = "https://api-zmartbi.teknisa.com"
    headers = {
        'Webtoken': 'Njc5N2NmZThlYTJmMzg3ZDljN2RlNmRkXzQ4MjQ=',
        'Cookie': 'PHPSESSID=1eodhb8grn23us5tq9jkfegg8f'
    }

    response = requests.get(url, headers=headers)
    data = json.loads(response.text)
    df = pd.DataFrame(data)
    print(filiais)
    print(identificador)

    # Converter CDFILIAL para inteiro para evitar problemas de tipo na filtragem
    df["CDFILIAL"] = df["CDFILIAL"].astype(int)

    # Agrupar por filial e nível de produto
    df_grouped = df.groupby(["CDFILIAL", "NMFILIAL", "NMSUBPRODNIVEL"], as_index=False)["VRESTOQDIA"].sum()
    print(df_grouped)

    # Filtrar apenas as filiais desejadas, se especificadas
    if filiais:
        if isinstance(filiais, int):
            filiais = [filiais]  # Converter para lista se for um único valor
        else:
            filiais = [int(f) for f in filiais]  # Garantir que todos os valores são inteiros

        df_grouped = df_grouped[df_grouped["CDFILIAL"].isin(filiais)]
    # Separar por filial e enviar e-mail
    for filial_codigo, group in df_grouped.groupby("CDFILIAL"):
        try:
            # Obter todos os gerentes para a filial
            gerentes = Gerente.objects.filter(unidades__codigo=filial_codigo, ativo=True)

            # Enviar o e-mail para cada gerente encontrado
            for gerente in gerentes:
                user_email = gerente.usuario.email
                # Criar a tabela HTML com os cabeçalhos desejados
                filial_data = group[["NMFILIAL", "NMSUBPRODNIVEL", "VRESTOQDIA"]]
                filial_data.columns = ["FILIAL", "GRUPO", "VALOR NO DIA"]  # Renomeando os cabeçalhos
                tabela_html = filial_data.to_html(index=False, classes="table table-striped table-bordered")

                nome_filial = group["NMFILIAL"].iloc[0]
                # Renderizar template com os dados
                html_content = render_to_string("email/email.html", {
                    "email_title": 'Posição do Estoque',
                    "email_text": "Você está recebendo um e-mail automático com os dados da posição do estoque da sua unidade.",
                    "nm_filial": group["NMFILIAL"].iloc[0],  # Nome da filial
                    "html_table": tabela_html
                })

                # Enviar e-mail
                email = EmailMessage(
                    subject=f"Resumo de Estoque para a Filial {nome_filial}",
                    body=html_content,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[user_email]
                )
                email.content_subtype = "html"
                try:
                    print('vai manda o email')
                    email.send()
                except:
                    print('mamamama')
                    return {"status": "finalizado", "mensagem": 'Executado com sucesso'}
                print(f"E-mail enviado para {user_email}")


        except Gerente.DoesNotExist:
            print(f"Nenhum gerente encontrado para a filial {filial_codigo}")

    return {"status": "finalizado", "dados": 'Executado com sucesso'}
