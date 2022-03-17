from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns

from .views import MoedaList, MoedaDetail, CotacaoList, CotacaoHighchartList

urlpatterns = [
    path('moedas/', MoedaList.as_view()),
    path('moedas/<str:pk>/', MoedaDetail.as_view()),
    path('cotacoes/<str:base>/<str:moeda>/', CotacaoList.as_view()),
    path('grafico/<str:base>/<str:moeda>/', CotacaoHighchartList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)