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

from rest_framework import serializers
from django_celery_beat.models import PeriodicTask, IntervalSchedule, CrontabSchedule
from .models import Automacao, LogAutomacao

class IntervalScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntervalSchedule
        fields = '__all__'

class CrontabScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrontabSchedule
        fields = '__all__'

class PeriodicTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeriodicTask
        fields = '__all__'

class AutomacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Automacao
        fields = '__all__'

class LogAutomacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogAutomacao
        fields = '__all__'