# serializers.py

from rest_framework import serializers
from .models import RegistroFinanceiro

class RegistroFinanceiroSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistroFinanceiro
        fields = '__all__'
