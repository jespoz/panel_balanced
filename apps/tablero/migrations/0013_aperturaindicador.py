# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-05-13 19:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tablero', '0012_auto_20160512_1554'),
    ]

    operations = [
        migrations.CreateModel(
            name='AperturaIndicador',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo_apertura', models.CharField(max_length=50)),
                ('apertura', models.CharField(max_length=140)),
                ('indicador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tablero.IndicadorObjetivo')),
            ],
            options={
                'verbose_name': 'Apertura por Indicador',
                'verbose_name_plural': 'Aperturas por Indicador',
            },
        ),
    ]