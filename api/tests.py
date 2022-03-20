from django.test import TestCase
from django.urls import reverse, resolve

from .views import MoedaList, MoedaDetail, CotacaoList, CotacaoHighchartList

# Create your tests here.
class TestUrls(TestCase):

    def test_list_moedas_url_resolves(self):
        self.assertEquals(resolve(reverse('list_moedas')).func.view_class, MoedaList)

    def test_detail_moedas_url_resolves(self):
        self.assertEquals(resolve(reverse('detail_moedas', args=['some-arg'])).func.view_class, MoedaDetail)

    def test_list_cotacao_url_resolves(self):
        self.assertEquals(resolve(reverse('list_cotacao', args=['some-arg1', 'some-arg2'])).func.view_class, CotacaoList)

    def test_list_highchart_url_resolves(self):
        self.assertEquals(resolve(reverse('list_highchart', args=['some-arg', 'some-arg2'])).func.view_class, CotacaoHighchartList)