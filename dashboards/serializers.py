from rest_framework import serializers
from .models import *


class DashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = DashboardPublico
        fields = '__all__'


class DashboardUnidade(serializers.ModelSerializer):
    class Meta:
        model = DashboardUnidade
        fields = '__all__'


class ImportacaoDadosSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImportacaoDados
        fields = '__all__'


class LinhaPlanilhaSerializer(serializers.ModelSerializer):
    class Meta:
        model = LinhaPlanilha
        fields = '__all__'


class PosicaoEstoqueDiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PosicaoEstoqueDia
        fields = '__all__'