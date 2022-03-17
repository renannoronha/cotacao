from django.shortcuts import render

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
        
        serializer = CotacaoSerializer(cotacoes, many=True)
        return Response(serializer.data)

class CotacaoHighchartList(APIView):
    """
    Cotações das moedas por data para o gráfico.
    """
    def get(self, request, base, moeda, format=None):
        cotacoes = Cotacao.objects.filter(base=base, moeda=moeda).order_by('-data')
        if request.GET.get('dataInicial', None):
            cotacoes.filter(data__gte=request.get('dataInicial'))
        if request.GET.get('dataFinal', None):
            cotacoes.filter(data__lte=request.get('dataFinal'))
        
        data = [[datetime(year=c[0].year, month=c[0].month, day=c[0].day).timestamp()*1000, c[1]] for c in cotacoes.values_list('data', 'cotacao')]
        return Response(data)