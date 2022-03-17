from django.http import Http404
from django.db.models import F
from rest_framework.views import APIView
from rest_framework.response import Response

from moeda.models import Moeda, Cotacao

from .serializers import MoedaSerializer, CotacaoSerializer

from datetime import datetime, timedelta

# Create your views here.
class MoedaList(APIView):
    """
    List all Moedas.
    """
    def get(self, request, format=None):
        moedas = Moeda.objects.all()
        serializer = MoedaSerializer(moedas, many=True)
        return Response(serializer.data)

class MoedaDetail(APIView):
    """
    Retrieve Moeda
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
    Cotações das moedas por data para o gráfico.
    """
    def get(self, request, base, moeda, format=None):
        cotacoes = Cotacao.objects.all().order_by('-data')
        if request.GET.get('dataInicial', None):
            cotacoes = cotacoes.filter(data__gte=request.GET.get('dataInicial'))
        if request.GET.get('dataFinal', None):
            cotacoes = cotacoes.filter(data__lte=request.GET.get('dataFinal'))
        
        base = cotacoes.filter(moeda=base)
        moeda = cotacoes.filter(moeda=moeda)
        dolar = cotacoes.filter(moeda__codigo='USD')
        data = [[datetime(year=b.data.year, month=b.data.month, day=b.data.day).timestamp()*1000, (d.cotacao/b.cotacao)*m.cotacao] for (b, m, d) in zip(base, moeda, dolar)]
        return Response(data)