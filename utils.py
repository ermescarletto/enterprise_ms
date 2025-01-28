import csv
import json


def csv_to_city(csv_file, json_file):
    fixtures = []

    with open(csv_file, newline='', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=',')
        for i, row in enumerate(reader):
            estado, nome, cep_de, cep_ate = row
            if nome != "":

                fixture = {
                    "model": "cadastros.cidade",
                    "pk": i + 1,  # Cada objeto precisa de uma chave primária única
                    "fields": {
                        "nome": nome,
                        "estado": estado,
                        "cep_de": int(cep_de),
                        "cep_ate": int(cep_ate)
                    }
                }
                fixtures.append(fixture)

    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(fixtures, f, ensure_ascii=False, indent=4)


# Substitua 'cidades.csv' e 'fixture.json' pelos nomes corretos
csv_to_city('ceps.csv', 'cidades.json')
