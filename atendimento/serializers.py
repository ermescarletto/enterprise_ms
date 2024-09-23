from rest_framework import serializers
from .models import Equipe, TipoAtendimento, Chamado, AnexoChamado, ComentarioChamado, AnexoComentario

class EquipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipe
        fields = ['id', 'nome', 'usuarios']

class TipoAtendimentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoAtendimento
        fields = ['id', 'nome', 'descricao', 'slo', 'sla', 'equipe']

class ChamadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chamado
        fields = ['id', 'tipo_atendimento', 'resumo', 'descricao', 'criado_em', 'atualizado_em', 'status', 'usuario_criador', 'usuario_atendente', 'equipe_atendente']

class AnexoChamadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnexoChamado
        fields = ['id', 'chamado', 'arquivo', 'tipo_arquivo', 'criado_em', 'enviado_por']

class ComentarioChamadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComentarioChamado
        fields = ['id', 'chamado', 'usuario', 'comentario', 'criado_em']

class AnexoComentarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnexoComentario
        fields = ['id', 'comentario', 'arquivo', 'tipo_arquivo', 'criado_em', 'enviado_por']
