from django.contrib import admin
from django.contrib import messages
from django_object_actions import DjangoObjectActions

from .models import *

# Register your models here.
@admin.register(Moeda)
class MoedaAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'moeda', 'simbolo']

@admin.register(Cotacao)
class CotacaoAdmin(DjangoObjectActions, admin.ModelAdmin):
    list_display = ['moeda', 'base', 'data', 'cotacao']
    list_filter = ['moeda']
    ordering = ['-data']
    
    def importar_cotacoes(modeladmin, request, queryset):
        try:
            # getNewVideos()
            messages.success(request, "Cotacões atualizadas com sucesso!")
        except Exception as e:
            messages.error(request, "Erro ao buscar Cotações." + str(e))

    importar_cotacoes.label = "Impotar Cotações"
    importar_cotacoes.short_description = "Importar cotações a partir da última data registrada no sistema."

    changelist_actions = ('importar_cotacoes', )
