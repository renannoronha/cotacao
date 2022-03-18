from django.contrib import admin
from django.contrib import messages
from rangefilter.filters import DateRangeFilter
from django_object_actions import DjangoObjectActions

from .models import *
from .get_cotacoes import get_cotacoes

from datetime import datetime

# Register your models here.
@admin.register(Moeda)
class MoedaAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'moeda', 'simbolo']

@admin.register(Cotacao)
class CotacaoAdmin(DjangoObjectActions, admin.ModelAdmin):
    list_display = ['moeda', 'base', 'data', 'cotacao']
    list_filter = (
        'moeda',
        ('data', DateRangeFilter)
    )
    ordering = ['-data']
    
    # Configuração do botão para buscar novas cotações.
    def importar_cotacoes(modeladmin, request, queryset):
        try:
            get_cotacoes(datetime.strptime(str(Cotacao.objects.all().order_by('-data').first().data), '%Y-%m-%d'), datetime.today())
            messages.success(request, "Cotacões atualizadas com sucesso!")
        except Exception as e:
            messages.error(request, "Erro ao buscar Cotações. " + str(e))

    importar_cotacoes.label = "Impotar Últimas Cotações"
    importar_cotacoes.short_description = "Importar cotações a partir da última data registrada no sistema."

    changelist_actions = ('importar_cotacoes', )
