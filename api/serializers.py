from rest_framework import serializers

from moeda.models import Moeda, Cotacao


class MoedaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Moeda
        fields = ['codigo', 'moeda', 'simbolo']


class CotacaoSerializer(serializers.Serializer):
    data = serializers.CharField()
    moeda = serializers.CharField(source='moeda.moeda')
    base = serializers.CharField()
    cotacao = serializers.CharField()
    codigo = serializers.CharField(source='moeda.codigo')
    simbolo = serializers.CharField(source='moeda.simbolo')

    class Meta:
        model = Cotacao
        fields = ['moeda', 'base', 'data', 'cotacao', 'codigo', 'simbolo']
