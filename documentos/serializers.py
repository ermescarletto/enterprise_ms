
from rest_framework import serializers
from .models import Politica, ProcedimentoPadrao, Fluxogramas, AnexosPolitica
from cadastros.models import Empresa, Departamento

class FluxogramaSerializer(serializers.ModelSerializer):
    key = serializers.SerializerMethodField()
    data = serializers.SerializerMethodField()

    class Meta:
        model = Fluxogramas
        fields = ['key', 'data']

    def get_key(self, obj):
        return f"{obj.procedimento_padrao.id}-{obj.id}"

    def get_data(self, obj):
        return {
            "codigo": obj.procedimento_padrao.politica.codigo_politica,
            "nome": obj.titulo_fluxograma,
            "departamento": obj.procedimento_padrao.politica.departamento.nome,
            "anexo": obj.anexo.url if obj.anexo else None
        }

class ProcedimentoPadraoSerializer(serializers.ModelSerializer):
    children = FluxogramaSerializer(many=True, source='fluxogramas_set')
    key = serializers.SerializerMethodField()
    data = serializers.SerializerMethodField()

    class Meta:
        model = ProcedimentoPadrao
        fields = ['key', 'data', 'children']

    def get_key(self, obj):
        return f"{obj.politica.id}-{obj.id}"

    def get_data(self, obj):
        return {
            "codigo": obj.politica.codigo_politica,
            "nome": obj.titulo_procedimento,
            "departamento": obj.politica.departamento.nome,
            "anexo": obj.anexo.url if obj.anexo else None
        }

class DocumentosSerializer(serializers.ModelSerializer):
    children = ProcedimentoPadraoSerializer(many=True, source='procedimentopadrao_set')
    key = serializers.SerializerMethodField()
    data = serializers.SerializerMethodField()

    class Meta:
        model = Politica
        fields = ['key', 'data', 'children']

    def get_key(self, obj):
        return str(obj.id)

    def get_data(self, obj):
        anexo = AnexosPolitica.objects.filter(politica=obj).first()
        return {
            "codigo": obj.codigo_politica,
            "nome": obj.titulo_politica,
            "departamento": obj.departamento.nome,
            "anexo": anexo.anexo.url if anexo else None
        }


class EmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        fields = ['id', 'nome', 'pessoa_juridica']


# Serializer for Departamento
class DepartamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departamento
        fields = ['id', 'nome']


# Serializer for Politica
class PoliticaListSerializer(serializers.ModelSerializer):
    empresa = EmpresaSerializer()  # Nested Empresa serializer
    departamento = DepartamentoSerializer()  # Nested Departamento serializer

    class Meta:
        model = Politica
        fields = '__all__'

class PoliticaCreateSerializer(serializers.ModelSerializer):


    class Meta:
        model = Politica
        fields = '__all__'