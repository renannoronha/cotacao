# Generated by Django 3.1.7 on 2022-03-17 11:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('moeda', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cotacao',
            old_name='date',
            new_name='data',
        ),
    ]
