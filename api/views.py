from django.http import Http404
from django.db.models import F
from rest_framework.views import APIView
from rest_framework.response import Response

from moeda.models import Moeda, Cotacao
from moeda.get_cotacoes import get_cotacoes

from .serializers import MoedaSerializer, CotacaoSerializer

from datetime import datetime, timedelta

# Create your views here.
class MoedaList(APIView):
    """
    Listar todas as moedas.
    """
    def get(self, request, format=None):
        moedas = Moeda.objects.all()
        serializer = MoedaSerializer(moedas, many=True)
        return Response(serializer.data)

class MoedaDetail(APIView):
    """
    Detalhes da Moeda.
    """
    def get_object(self, pk):
        try:
            return Moeda.objects.get(pk=pk)
        except Moeda.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        moeda = self.get_object(pk)
        serializer = MoedaSerializer(moeda)
        return Response(serializer.data)

class CotacaoList(APIView):
    """
    Cotações das moedas por data.

    Para filtrar por data também: ?dataInicial=2022-03-01&dataFinal=2022-03-18
    """
    def get(self, request, base, moeda, format=None):
        cotacoes = Cotacao.objects.filter(base=base, moeda=moeda).order_by('-data')
        if request.GET.get('dataInicial', None):
            cotacoes = cotacoes.filter(data__gte=request.GET.get('dataInicial'))
        if request.GET.get('dataFinal', None):
            cotacoes = cotacoes.filter(data__lte=request.GET.get('dataFinal'))
        
        serializer = CotacaoSerializer(cotacoes, many=True)
        return Response(serializer.data)

class CotacaoHighchartList(APIView):
    """
    Cotações das moedas selecionadas por data. Resposta formatada para Highcharts.

    Para filtrar por data também: ?dataInicial=2022-03-01&dataFinal=2022-03-18
    """
    def get(self, request, base, moeda, format=None):
        cotacoes = Cotacao.objects.all().order_by('-data')
        if request.GET.get('dataInicial', None):
            # Se a data inicial for menor que a data mais antiga registrada no sistema, buscar os dados que faltam na API
            if Cotacao.objects.all().order_by('data').first().data - datetime.strptime(request.GET.get('dataInicial'), '%Y-%m-%d').date() >= timedelta(days=1):
                get_cotacoes(datetime.strptime(request.GET.get('dataInicial'), '%Y-%m-%d').date(), request.GET.get('dataFinal', Cotacao.objects.all().order_by('data').first().data))
            cotacoes = cotacoes.filter(data__gte=request.GET.get('dataInicial'))
        if request.GET.get('dataFinal', None):
            cotacoes = cotacoes.filter(data__lte=request.GET.get('dataFinal'))
        
        # Formatar a resposta de acordo com o esperado pelo Highcharts,
        # e calcular a cotação de acordo com as moedas selecionadas.
        moeda1 = cotacoes.filter(moeda=base) # Primeira moeda ex.: [USD]/BRL
        moeda2 = cotacoes.filter(moeda=moeda) # Segunda moeda ex.: USD/[BRL]
        base = cotacoes.filter(moeda__codigo='USD') # Moeda base da cotação, nesse caso é (dólar) fixo
        data = [[datetime(year=b.data.year, month=b.data.month, day=b.data.day).timestamp()*1000, (b.cotacao/m1.cotacao)*m2.cotacao] for (m1, m2, b) in zip(moeda1, moeda2, base)]
        return Response(data)