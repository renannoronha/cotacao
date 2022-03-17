import requests
import json
from datetime import datetime, timedelta

from .models import Moeda, Cotacao

def get_cotacoes(dataInicial, dataFinal):
    while dataInicial <= dataFinal:
        r = requests.get('https://api.vatcomply.com/rates?base=USD&date=' + dataInicial.strftime('%Y-%m-%d'))
        if r.status_code == 200:
            rates = r.json()
            data = rates['date']
            base = rates['base']
            for moeda in Moeda.objects.all():
                default = {
                    'moeda': moeda,
                    'base': moeda,
                    'data': data,
                    'cotacao': rates['rates'][moeda.codigo],
                }
                print(default)
                (obj, created) = Cotacao.objects.update_or_create(
                    moeda = moeda,
                    base = moeda,
                    data = data,
                    cotacao = rates['rates'][moeda.codigo],
                    defaults = default
                )
        else:
            return r.raise_for_status()
        dataInicial = dataInicial + timedelta(days=1)
