from django.http import Http404
from django.db.models import F
from rest_framework.views import APIView
from rest_framework.response import Response

from moeda.models import Moeda, Cotacao

from .serializers import MoedaSerializer, CotacaoSerializer

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
            cotacoes.filter(data__gte=request.get('dataInicial'))
        if request.GET.get('dataFinal', None):
            cotacoes.filter(data__lte=request.get('dataFinal'))
        
        # cotacoes = cotacoes.annotate(codigo=F('moeda__codigo'), simbolo=F('moeda__simbolo'))
        serializer = CotacaoSerializer(cotacoes, many=True)
        return Response(serializer.data)