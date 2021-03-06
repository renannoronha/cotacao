# Generated by Django 3.1.7 on 2022-03-17 11:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Moeda',
            fields=[
                ('codigo', models.CharField(max_length=3, primary_key=True, serialize=False, verbose_name='Código')),
                ('moeda', models.CharField(max_length=255, verbose_name='Nome da Moeda')),
                ('simbolo', models.CharField(max_length=5, verbose_name='Símbolo')),
            ],
            options={
                'verbose_name': 'Moeda',
                'verbose_name_plural': 'Moedas',
            },
        ),
        migrations.CreateModel(
            name='Cotacao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Data')),
                ('cotacao', models.DecimalField(decimal_places=20, max_digits=25, verbose_name='Cotação')),
                ('base', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='cotacao_base', to='moeda.moeda')),
                ('moeda', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='cotacao_moeda', to='moeda.moeda')),
            ],
            options={
                'verbose_name': 'Cotação',
                'verbose_name_plural': 'Cotações',
            },
        ),
    ]
