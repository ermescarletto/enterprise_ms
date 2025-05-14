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
from collections import defaultdict
from datetime import datetime
from .models import *

from .models import *

url = "https://api-zmartbi.teknisa.com"


@shared_task(bind=True)
def processar_planilha(self, importacao_id):
    importacao = ImportacaoDados.objects.get(id=importacao_id)
    importacao.status = 'processando'
    importacao.save()

    try:
        ext = importacao.arquivo.name.split('.')[-1].lower()
        if ext in ['xls', 'xlsx', 'ods']:
            df = pd.read_excel(importacao.arquivo.path)
        elif ext == 'csv':
            df = pd.read_csv(importacao.arquivo.path)
        else:
            raise Exception("Formato não suportado")

        total = len(df)
        for index, row in df.iterrows():
            LinhaPlanilha.objects.create(
                importacao=importacao,
                codigo_unidade=row['CODIGO DA UNIDADE'],
                unidade=row['UNIDADE'],
                codigo_centro_custo=row['CODIGO DO CENTRO DE CUSTO'],
                centro_custo=row['CENTRO DE CUSTO'],
                codigo_reduzido=row['CODIGO REDUSIDO'],
                data=row['DATA'],
                numero=row['NUMERO'],
                conta=row['CONTA'],
                historico=row['HISTÓRICO'],
                debito=row['DÉBITO'],
                credito=row['CRÉDITO'],
                saldo=row['SALDO']
            )
            importacao.progresso = round((index + 1) / total * 100, 2)
            importacao.save()

        importacao.status = 'concluido'
    except Exception as e:
        importacao.status = 'erro'
        print(f"[ERRO] {e}")
    finally:
        importacao.save()

@shared_task(bind=True)
def processar_planilha(self, importacao_id):
    importacao = ImportacaoDados.objects.get(id=importacao_id)
    importacao.status = 'processando'
    importacao.save()

    try:
        ext = importacao.arquivo.name.split('.')[-1].lower()
        if ext in ['xls', 'xlsx', 'ods']:
            df = pd.read_excel(importacao.arquivo.path)
        elif ext == 'csv':
            df = pd.read_csv(importacao.arquivo.path)
        else:
            raise Exception("Formato não suportado")

        total = len(df)
        for index, row in df.iterrows():
            LinhaPlanilha.objects.create(
                importacao=importacao,
                codigo_unidade=row['CODIGO DA UNIDADE'],
                unidade=row['UNIDADE'],
                codigo_centro_custo=row['CODIGO DO CENTRO DE CUSTO'],
                centro_custo=row['CENTRO DE CUSTO'],
                codigo_reduzido=row['CODIGO REDUSIDO'],
                data=row['DATA'],
                numero=row['NUMERO'],
                conta=row['CONTA'],
                historico=row['HISTÓRICO'],
                debito=row['DÉBITO'],
                credito=row['CRÉDITO'],
                saldo=row['SALDO']
            )
            importacao.progresso = round((index + 1) / total * 100, 2)
            importacao.save()

        importacao.status = 'concluido'
    except Exception as e:
        importacao.status = 'erro'
        print(f"[ERRO] {e}")
    finally:
        importacao.save()

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
def envia_fluxo_caixa(identificador,filiais=None):
    headers = {
        'Webtoken': 'NjdlYmQ0YWIyYjhjNGE3ZGM2NTBkNWQ4XzQ4MjQ=',
        'Cookie': 'PHPSESSID=1eodhb8grn23us5tq9jkfegg8f'
    }
    response = requests.get(url, headers=headers)
    data = response.json() if response.status_code == 200 else []

    # Empresas permitidas
    empresas_permitidas = {"02", "05"}

    # Estrutura de dados {empresa -> {dia -> valores}}
    fluxo_agrupado = defaultdict(lambda: defaultdict(lambda: {"VRENTRADA": 0, "VRSAIDA": 0, "LANCAMENTOS": []}))

    for item in data:
        dt_mov = item["DTMOVFLUXO"]
        cd_empresa = item["CDEMPRESA"]
        nm_empresa = item["NMEMPRESA"]

        # Filtrar apenas empresas desejadas
        if cd_empresa not in empresas_permitidas:
            continue

        # Converter a data para o formato correto
        data_mov = datetime.strptime(dt_mov, "%d/%m/%Y")

        # Filtrar apenas o mês de março
        if data_mov.month != 3:
            continue

        # Armazenar os dados agrupados por empresa e dia
        dia = data_mov.strftime("%Y-%m-%d")
        fluxo_agrupado[nm_empresa][dia]["VRENTRADA"] += item["VRENTRADA"]
        fluxo_agrupado[nm_empresa][dia]["VRSAIDA"] += item["VRSAIDA"]
        fluxo_agrupado[nm_empresa][dia]["LANCAMENTOS"].append(item)

    # Ordenar empresas
    empresas_ordenadas = sorted(fluxo_agrupado.keys())

    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Fluxo de Caixa - Março</title>
        <style>
            table { border-collapse: collapse; width: 100%; margin-bottom: 20px; }
            th, td { border: 1px solid black; padding: 8px; text-align: left; }
            th { background-color: #f2f2f2; }
            h2 { margin-top: 20px; }
            .toggle { cursor: pointer; color: blue; text-decoration: underline; }
            .hidden { display: none; }
        </style>
        <script>
            function toggleDetails(id) {
                var element = document.getElementById(id);
                if (element.style.display === "none") {
                    element.style.display = "table-row-group";
                } else {
                    element.style.display = "none";
                }
            }
        </script>
    </head>
    <body>
        <h1>Relatório de Fluxo de Caixa - Março</h1>
    """

    for empresa in empresas_ordenadas:
        html_content += f"<h2>{empresa}</h2>"
        html_content += """
        <table>
            <tr>
                <th>Data</th>
                <th>Entrada (R$)</th>
                <th>Saída (R$)</th>
                <th>Detalhes</th>
            </tr>
        """

        # Ordenar dias dentro de cada empresa
        for dia in sorted(fluxo_agrupado[empresa].keys(), key=lambda x: datetime.strptime(x, "%Y-%m-%d")):
            valores = fluxo_agrupado[empresa][dia]
            id_lancamento = f"detalhes_{empresa}_{dia.replace('-', '')}"

            # Linha principal com botão de expandir/recolher
            html_content += f"""
            <tr>
                <td>{dia}</td>
                <td>{valores['VRENTRADA']:.2f}</td>
                <td>{valores['VRSAIDA']:.2f}</td>
                <td><span class="toggle" onclick="toggleDetails('{id_lancamento}')">Ver detalhes</span></td>
            </tr>
            """

            # Linhas ocultas com os lançamentos detalhados
            html_content += f"""
            <tbody id="{id_lancamento}" class="hidden">
                <tr>
                    <th colspan="4">Lançamentos no dia {dia}</th>
                </tr>
            """
            for lancamento in valores["LANCAMENTOS"]:
                html_content += f"""
                <tr>
                    <td colspan="2">{lancamento['DSCLASSFINA']}</td>
                    <td>{lancamento['VRENTRADA']:.2f}</td>
                    <td>{lancamento['VRSAIDA']:.2f}</td>
                </tr>
                """
            html_content += "</tbody>"

        html_content += "</table>"

    html_content += """
    </body>
    </html>
    """

    with open("fluxo_caixa.html", "w", encoding="utf-8") as f:
        f.write(html_content)

    print("Arquivo 'fluxo_caixa.html' gerado com sucesso!")

@shared_task
def envia_email_estoque(identificador, filiais=None):
    headers = {
        'Webtoken': 'Njc5N2NmZThlYTJmMzg3ZDljN2RlNmRkXzQ4MjQ=',
        'Cookie': 'PHPSESSID=1eodhb8grn23us5tq9jkfegg8f'
    }

    response = requests.get(url, headers=headers)
    data = json.loads(response.text)
    df = pd.DataFrame(data)

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
                # Criar uma cópia para evitar o aviso de "SettingWithCopyWarning"
                filial_data = group[["NMFILIAL", "NMSUBPRODNIVEL", "VRESTOQDIA"]].copy()

                # Renomear colunas
                filial_data.columns = ["FILIAL", "GRUPO", "VALOR NO DIA"]

                # Arredondar os valores e adicionar o símbolo R$
                filial_data["VALOR NO DIA"] = filial_data["VALOR NO DIA"].round(2).apply(lambda x: f"R$ {x:.2f}")

                # Calcular o total corretamente
                total_estoque = group["VRESTOQDIA"].sum()

                # Criar um DataFrame com a linha de total e concatenar com o original
                total_row = pd.DataFrame([["", "TOTAL", f"R$ {total_estoque:.2f}"]], columns=filial_data.columns)
                filial_data = pd.concat([filial_data, total_row], ignore_index=True)

                # Criar a tabela HTML
                tabela_html = filial_data.to_html(index=False, classes="table table-striped table-bordered")
                nome_filial = group["NMFILIAL"].iloc[0]
                # Renderizar template com os dados
                html_content = render_to_string("email/email.html", {
                    "email_title": 'Posição do Estoque',
                    "email_text": "Você está recebendo um e-mail automático com os dados da posição do estoque da sua unidade.",
                    "nm_filial": group["NMFILIAL"].iloc[0],  # Nome da filial
                    "html_table": tabela_html
                })
                print('enviando e-mail {}'.format(nome_filial))

                # Enviar e-mail
                email = EmailMessage(
                    subject=f"Resumo de Estoque para a Filial {nome_filial}",
                    body=html_content,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[user_email,'charles@maissabor.ind.br']
                )
                email.content_subtype = "html"
                try:
                    email.send()
                except Exception as e:
                        print(f"❌ Erro ao enviar e-mail para {user_email}: {str(e)}")


        except Gerente.DoesNotExist:
            print(f"Nenhum gerente encontrado para a filial {filial_codigo}")

    return {"status": "finalizado", "dados": 'Executado com sucesso'}

@shared_task
def gera_relatorio_pagamentos(identificador):
    headers = {'Webtoken': 'NjdkODE4MDc2NDg2YzczNzI5M2Y2M2RiXzQ4MjQ='}
    response = requests.get(url, headers=headers)
    data = json.loads(response.text)

    empresas_filtradas = {"02", "05"}
    meses_filtrados = {"03", "04"}  # Março e Abril
    fluxo_agrupado = defaultdict(lambda: defaultdict(lambda: {"VRPAGAR": 0, "VRRECEBER": 0, "LANCAMENTOS": []}))

    for item in data:
        cde_empresa = item["CDEMPRESA"]
        tipo_operacao = item["TIPO_OPERACAO"]
        nm_empresa = item["NMEMPRESA"]

        if cde_empresa not in empresas_filtradas:
            continue

        if tipo_operacao == "01 - NF Compra":
            data_venc = item["DTATUAVENPAG"]
            valor_pagar = item["VRRATPAG"]
            valor_receber = 0
        elif tipo_operacao == "01 - NF Venda":
            data_venc = item["DTATUAVENREC"]
            valor_pagar = 0
            valor_receber = item["VRATUAREC"]
        else:
            continue

        data_venc = datetime.strptime(data_venc, "%d/%m/%Y")
        mes_venc = data_venc.strftime("%m")
        if mes_venc not in meses_filtrados:
            continue

        dia_venc = data_venc.strftime("%d/%m/%Y")
        fluxo_agrupado[nm_empresa][dia_venc]["VRPAGAR"] += valor_pagar
        fluxo_agrupado[nm_empresa][dia_venc]["VRRECEBER"] += valor_receber
        fluxo_agrupado[nm_empresa][dia_venc]["LANCAMENTOS"].append(item)

    html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Relatório de Pagamentos</title>
            <style>
                table { border-collapse: collapse; width: 100%; margin-bottom: 20px; }
                th, td { border: 1px solid black; padding: 8px; text-align: left; }
                th { background-color: #f2f2f2; }
                h2 { margin-top: 20px; }
                .toggle { cursor: pointer; color: blue; text-decoration: underline; }
                .hidden { display: none; }
            </style>
            <script>
                function toggleDetails(id) {
                    var element = document.getElementById(id);
                    element.style.display = (element.style.display === "none" ? "table-row-group" : "none");
                }
            </script>
        </head>
        <body>
            <h1>Relatório de Pagamentos - Março e Abril</h1>
        """

    for empresa, dias in fluxo_agrupado.items():
        html_content += f"<h2>{empresa}</h2><table>"
        html_content += """
            <tr>
                <th>Dia</th>
                <th>Valor a Pagar (R$)</th>
                <th>Valor a Receber (R$)</th>
                <th>Detalhes</th>
            </tr>
            """
        for dia, valores in sorted(dias.items(), key=lambda x: datetime.strptime(x[0], "%d/%m/%Y")):
            id_lancamento = f"detalhes_{dia.replace('/', '')}_{empresa.replace(' ', '_')}"
            html_content += f"""
                <tr>
                    <td>{dia}</td>
                    <td>{valores['VRPAGAR']:.2f}</td>
                    <td>{valores['VRRECEBER']:.2f}</td>
                    <td><span class='toggle' onclick="toggleDetails('{id_lancamento}')">Ver detalhes</span></td>
                </tr>
                <tbody id="{id_lancamento}" class="hidden">
                    <tr>
                        <th colspan="4">Lançamentos do dia {dia}</th>
                    </tr>
                """
            for lancamento in valores["LANCAMENTOS"]:
                html_content += f"""
                    <tr>
                        <td colspan="2">{lancamento['DSCLASSFINA']}</td>
                        <td colspan="2">{lancamento['TIPO_OPERACAO']}</td>
                    </tr>
                    """
            html_content += "</tbody>"
        html_content += "</table>"

    html_content += "</body></html>"

    with open("relatorio_pagamentos.html", "w", encoding="utf-8") as f:
        f.write(html_content)

    print("Arquivo 'relatorio_pagamentos.html' gerado com sucesso!")

@shared_task
def carrega_posicao_estoque(identificador, filiais=None):

    headers = {
        'Webtoken': 'Njc5N2NmZThlYTJmMzg3ZDljN2RlNmRkXzQ4MjQ=',
        'Cookie': 'PHPSESSID=1eodhb8grn23us5tq9jkfegg8f'
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return {"status_code": response.status_code, "status": "erro", "dados": f"Erro na requisição: {response.status_code}"}

    data = json.loads(response.text)

    # Iterar sobre os dados do JSON e salvar no model PosicaoEstoqueDia
    for item in data:
        # Filtrar apenas as filiais desejadas, se especificadas
        if filiais and int(item["CDFILIAL"]) not in filiais:
            continue

        # Converter campos de data para o formato datetime.date
        dtposiestq = datetime.strptime(item["DTPOSIESTQ"], "%d/%m/%Y").date()
        dtref = datetime.strptime(item["DTREF"], "%d/%m/%Y").date()
        dtimport = datetime.strptime(item["DTIMPORT"], "%d/%m/%Y").date()
        # Salvar ou atualizar os dados no model
        PosicaoEstoqueDia.objects.update_or_create(
            id_teknisa=item["_id"],
            nmorg=item["NRORG"],
            nmorganizacao=item["NMORGANIZACAO"],
            cdempresa=int(item["CDEMPRESA"]),
            nmfilial=item["NMFILIAL"],
            dtposiestq=dtposiestq,
            dtref=dtref,
            dtimport=dtimport,
            nmgrupprodnivel=item["NMGRUPPRODNIVEL"],
            nmsubprodnivel=item["NMSUBPRODNIVEL"],
            nrloteesto=item["NRLOTEESTQ"].strip() or None,
            cdlocalestoq=item["CDLOCALESTOQ"].strip() or None,
            dslocalestoq=item["DSLOCALESTOQ"].strip() or None,
            cdalmoxarife=item["CDALMOXARIFE"].strip() or None,
            dsalmoxarife=item["DSALMOXARIFE"].strip() or None,
            cdarvprod=item.get("CDARVPROD") or None,
            nmprodnivel=item["NMPRODNIVEL"],
            cdprodesto=item["CDPRODESTO"],
            sgunidade=item["SGUNIDADE"],
            qtestoquedia=item["QTESTOQDIA"],
            vrmediobrut=item["VRMEDIOBRUT"],
            vrestoqbrut=item["VRESTOQBRUT"],
            vrmedio=item["VRMEDIO"],
            vrestoqdia=item["VRESTOQDIA"],
            vrcustoprod=item["VRCUSTOPROD"],
            numdias=item["NUMDIAS"],
            defaults={
                "data_criacao": datetime.now().date()  # Campo gerado automaticamente
            }
        )

    return {"status_code": 201, "status": "finalizado", "dados": "Dados inseridos no model PosicaoEstoqueDia com sucesso"}



import requests
from celery import shared_task
from .models import Automacao, LogAutomacao
import uuid

@shared_task
def executar_automacao(automacao_id):
    try:
        automacao = Automacao.objects.get(id=automacao_id)
        if not automacao.ativo:
            return {"status": "Automação desativada"}
        headers = {"Authorization": f"{automacao.token_param} {automacao.token}"} if automacao.token else {}
        response = requests.request(
            method=automacao.metodo,
            url=automacao.url,
            headers=headers,
            json=automacao.parametros
        )

        log = LogAutomacao.objects.create(
            hash=str(uuid.uuid4()),
            automacao=automacao,
            data_hora=datetime.now(),
            tipo_execucao='AUTOMÁTICA',
            resposta=response.json(),
            status=response.status_code
        )
        return {"status": "Sucesso", "log_id": log.id}

    except Exception as e:
        LogAutomacao.objects.create(
            hash=str(uuid.uuid4()),
            automacao=automacao,
            data_hora=datetime.now(),
            tipo_execucao='AUTOMÁTICA',
            resposta={},
            status=500,
            erro=str(e)
        )
        return {"status": "Erro", "mensagem": str(e)}



@shared_task
def executar_automacoes_ativas():
    """
    Executa todas as automações ativas.
    """
    automacoes = Automacao.objects.filter(ativo=True)
    for automacao in automacoes:
        executar_automacao.delay(automacao.id)