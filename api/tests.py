from django.test import TestCase, Client
from django.urls import reverse, resolve

from .views import MoedaList, MoedaDetail, CotacaoList, CotacaoHighchartList
from .serializers import MoedaSerializer, CotacaoSerializer
from moeda.models import Moeda, Cotacao

# Create your tests here.
class TestUrls(TestCase):

    def test_list_moedas_url_resolves(self):
        self.assertEquals(resolve(reverse('list_moedas')).func.view_class, MoedaList)

    def test_detail_moedas_url_resolves(self):
        self.assertEquals(resolve(reverse('detail_moedas', args=['codigo_moeda'])).func.view_class, MoedaDetail)

    def test_list_cotacao_url_resolves(self):
        self.assertEquals(resolve(reverse('list_cotacao', args=['codigo_moeda1', 'codigo_moeda2'])).func.view_class, CotacaoList)

    def test_list_highchart_url_resolves(self):
        self.assertEquals(resolve(reverse('list_highchart', args=['codigo_moeda1', 'codigo_moeda2'])).func.view_class, CotacaoHighchartList)

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.list_moedas_url = reverse('list_moedas')
        self.detail_moedas_url = reverse('detail_moedas', args=['USD'])
        self.list_cotacao_url = reverse('list_cotacao', args=['USD', 'BRL'])
        self.list_highchart_url = reverse('list_highchart', args=['USD', 'BRL'])
        self.dolar = Moeda.objects.create(codigo='USD', moeda='Dólar', simbolo='$')
        self.real = Moeda.objects.create(codigo='BRL', moeda='Real', simbolo='R$')
        Cotacao.objects.create(moeda=self.real, base=self.dolar, data='2022-01-01', cotacao=11)
        Cotacao.objects.create(moeda=self.real, base=self.dolar, data='2022-01-02', cotacao=12)
        Cotacao.objects.create(moeda=self.real, base=self.dolar, data='2022-01-03', cotacao=13)

    def test_list_moedas_get(self):
        response = self.client.get(self.list_moedas_url)
        self.assertEquals(response.status_code, 200)
      
        moedas = Moeda.objects.all()
        serializer = MoedaSerializer(moedas, many=True)
        self.assertEqual(response.data, serializer.data)

    def test_detail_moedas_get(self):
        response = self.client.get(self.detail_moedas_url)
        self.assertEquals(response.status_code, 200)
      
        serializer = MoedaSerializer(self.dolar)
        self.assertEqual(response.data, serializer.data)

    def test_list_cotacao_get(self):
        response = self.client.get(self.list_cotacao_url)
        self.assertEquals(response.status_code, 200)
       
        cotacoes = Cotacao.objects.filter(base=self.dolar, moeda=self.real).order_by('-data')
        serializer = CotacaoSerializer(cotacoes, many=True)
        self.assertEqual(response.data, serializer.data)

    def test_list_highchart_get(self):
        response = self.client.get(self.list_highchart_url)
        self.assertEquals(response.status_code, 200)

        cotacoes = Cotacao.objects.all().order_by('-data')
        # Formatar a resposta de acordo com o esperado pelo Highcharts,
        # e calcular a cotação de acordo com as moedas selecionadas.
        moeda1 = cotacoes.filter(moeda=self.dolar) # Primeira moeda ex.: [USD]/BRL
        moeda2 = cotacoes.filter(moeda=self.real) # Segunda moeda ex.: USD/[BRL]
        base = cotacoes.filter(moeda__codigo='USD') # Moeda base da cotação, nesse caso é (dólar) fixo
        data = [[datetime(year=b.data.year, month=b.data.month, day=b.data.day).timestamp()*1000, (b.cotacao/m1.cotacao)*m2.cotacao] for (m1, m2, b) in zip(moeda1, moeda2, base)]
        self.assertEqual(response.data, data)
