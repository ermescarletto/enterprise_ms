import pandas as pd
import json

# Nome do arquivo Excel
file_path = "data/Empresa.xlsx"

# Ler a planilha
xls = pd.ExcelFile(file_path)
df = xls.parse(xls.sheet_names[0])  # Considera a primeira aba

# Renomear colunas para corresponder ao modelo Django
df.columns = ["codigo", "cnpj", "inscricao_estadual", "razao_social"]

def format_cnpj(cnpj):
    """Remove caracteres não numéricos do CNPJ"""
    return "".join(filter(str.isdigit, str(cnpj)))

# Tratamento dos dados
df["cnpj"] = df["cnpj"].apply(format_cnpj)
df["inscricao_estadual"].fillna("", inplace=True)
df["inscricao_municipal"] = ""
df["email"] = ""
df["telefone"] = ""
df["nome_fantasia"] = ""

data = []

# Criar a estrutura JSON da fixture para Django
for index, row in df.iterrows():
    data.append({
        "model": "app.PessoaJuridica",  # Substitua "app" pelo nome real do seu app Django
        "pk": index + 1,
        "fields": {
            "cnpj": row["cnpj"],
            "inscricao_estadual": row["inscricao_estadual"],
            "inscricao_municipal": row["inscricao_municipal"],
            "razao_social": row["razao_social"],
            "nome_fantasia": row["nome_fantasia"],
            "email": row["email"],
            "telefone": row["telefone"],
        }
    })

# Salvar como JSON
fixture_path = "data/empresa_fixture.json"
with open(fixture_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print(f"Fixture gerada com sucesso: {fixture_path}")