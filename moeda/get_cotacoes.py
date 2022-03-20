import requests
import json
from datetime import datetime, timedelta

from .models import Moeda, Cotacao

def get_cotacoes(dataInicial, dataFinal):
    """
    Importa e salva as dados da API Vatcomply de acordo com as datas fornecidas.
    """

    # Setar valor inicial e final das datas para quando a função for chamada pelo cronjob
    if not dataInicial:
        try:
            dataInicial = Cotacao.objects.all().order_by('-data').first().data
        except:
            dataInicial = datetime.now().date() - timedelta(days=5)
    if not dataFinal:
        dataFinal = datetime.now().date()
    
    while dataInicial <= dataFinal:
        r = requests.get('https://api.vatcomply.com/rates?base=USD&date=' + dataInicial.strftime('%Y-%m-%d'))
        if r.status_code == 200:
            rates = r.json()
            data = rates['date']
            base = Moeda.objects.get(codigo=rates['base'])
            for moeda in Moeda.objects.all():
                default = {
                    'moeda': moeda,
                    'base': base,
                    'data': data,
                    'cotacao': rates['rates'][moeda.codigo],
                }
                print(default)
                (obj, created) = Cotacao.objects.update_or_create(
                    moeda = moeda,
                    base = base,
                    data = data,
                    cotacao = rates['rates'][moeda.codigo],
                    defaults = default
                )
        else:
            return r.raise_for_status()
        dataInicial = dataInicial + timedelta(days=1)
