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

