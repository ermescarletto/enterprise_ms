from rest_framework import serializers
from .models import *


class CidadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cidade
        fields = '__all__'


class BairroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bairro
        fields = ['nome', 'cidade']


class LogradouroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Logradouro
        fields = ['nome', 'bairro', 'cidade']


class PessoaFisicaSerializerCompleto(serializers.ModelSerializer):
    enderecos = serializers.StringRelatedField(many=True)
    contatos = serializers.StringRelatedField(many=True)

    class Meta:
        model = PessoaFisica
        fields = ['nome', 'data_nascimento', 'sexo', 'email', 'telefone', 'enderecos', 'contatos']


class PessoaFisicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PessoaFisica
        fields = ['__all__']


class EnderecoPessoaFisicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnderecoPessoaFisica
        fields = ['__all__']


class ContatoPessoaFisicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContatoPessoaFisica
        fields = ['__all__']



class PessoaJuridicaSerializerCompleto(serializers.ModelSerializer):
    class Meta:
        model = PessoaJuridica
        fields = '__all__'

class UnidadeSerializerCompleto(serializers.ModelSerializer):
    class Meta:
        model = Unidade
        fields = '__all__'




from users.serializers import UserSerializer
class GerenteSerializerCompleto(serializers.ModelSerializer):
    unidades = UnidadeSerializerCompleto(many=True, read_only=True)
    usuario = UserSerializer()
    class Meta:
        model = Gerente
        fields = '__all__'