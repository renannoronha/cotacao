from django.db import models

# Create your models here.
class Moeda(models.Model):
    codigo = models.CharField('Código', max_length=3, primary_key=True)
    moeda = models.CharField('Nome da Moeda', max_length=255)
    simbolo = models.CharField('Símbolo', max_length=5)

    def __str__(self):
        return self.codigo

    class Meta:
        verbose_name = 'Moeda'
        verbose_name_plural = 'Moedas'

class Cotacao(models.Model):
    moeda = models.ForeignKey(Moeda, on_delete=models.PROTECT, related_name='cotacao_moeda')
    base = models.ForeignKey(Moeda, on_delete=models.PROTECT, related_name='cotacao_base')
    data = models.DateField('Data')
    cotacao = models.DecimalField('Cotação', decimal_places=20, max_digits=25)

    def __str__(self):
        return '%s - %s %s' % (self.data, self.moeda, self.cotacao)

    class Meta:
        verbose_name = 'Cotação'
        verbose_name_plural = 'Cotações'