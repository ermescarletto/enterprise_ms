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