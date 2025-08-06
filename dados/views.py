from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from .models import RegistroFinanceiro
from .serializers import RegistroFinanceiroSerializer
import csv
from io import TextIOWrapper
import datetime

def parse_competencia(value):
    # Tenta converter formatos como '1/1/2025' para '2025-01-01'
    try:
        return datetime.datetime.strptime(value, '%d/%m/%Y').date().isoformat()
    except Exception:
        try:
            return datetime.datetime.strptime(value, '%Y-%m-%d').date().isoformat()
        except Exception:
            return value  # retorna como está se não conseguir converter

def parse_valor_contabil(value):
    # Remove pontos de milhar e troca vírgula por ponto
    try:
        return value.replace('.', '').replace(',', '.')
    except Exception:
        return value

class RegistroFinanceiroViewSet(viewsets.ModelViewSet):
    queryset = RegistroFinanceiro.objects.all()
    serializer_class = RegistroFinanceiroSerializer
    parser_classes = [MultiPartParser]

    def create(self, request, *args, **kwargs):
        print("Iniciando importação CSV")
        RegistroFinanceiro.objects.all().delete()
        print("Tabela limpa")

        csv_file = request.FILES.get('file')
        if not csv_file:
            print("Arquivo não enviado")
            return Response({'error': 'Arquivo CSV não enviado.'}, status=status.HTTP_400_BAD_REQUEST)

        field_map = {
            'Empresa / Filial': 'empresa_filial',
            'Centro de Custo': 'centro_custo',
            'Conta': 'conta',
            'Competência': 'competencia',
            'Histórico': 'historico',
            'Valor Contábil': 'valor_contabil',
        }

        data_list = []
        try:
            print("Tentando ler como UTF-8")
            csv_reader = csv.DictReader(TextIOWrapper(csv_file, encoding='utf-8'), delimiter=';')
            for row in csv_reader:
                print("Linha lida:", row)
                mapped_row = {field_map.get(k.strip(), k.strip()): v.strip() for k, v in row.items()}
                # Ajusta os campos problemáticos
                if 'competencia' in mapped_row:
                    mapped_row['competencia'] = parse_competencia(mapped_row['competencia'])
                if 'valor_contabil' in mapped_row:
                    mapped_row['valor_contabil'] = parse_valor_contabil(mapped_row['valor_contabil'])
                serializer = self.get_serializer(data=mapped_row)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                data_list.append(serializer.data)
        except UnicodeDecodeError:
            print("UnicodeDecodeError, tentando latin1")
            csv_file.seek(0)
            csv_reader = csv.DictReader(TextIOWrapper(csv_file, encoding='latin1'), delimiter=';')
            for row in csv_reader:
                print("Linha lida:", row)
                mapped_row = {field_map.get(k.strip(), k.strip()): v.strip() for k, v in row.items()}
                if 'competencia' in mapped_row:
                    mapped_row['competencia'] = parse_competencia(mapped_row['competencia'])
                if 'valor_contabil' in mapped_row:
                    mapped_row['valor_contabil'] = parse_valor_contabil(mapped_row['valor_contabil'])
                serializer = self.get_serializer(data=mapped_row)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                data_list.append(serializer.data)
        except Exception as e:
            print("Erro inesperado:", e)
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        if not data_list:
            print("Nenhum registro importado")
            return Response({'warning': 'Nenhum registro foi importado.'}, status=status.HTTP_200_OK)

        print("Importação concluída")
        return Response(data_list, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
