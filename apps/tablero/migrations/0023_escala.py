# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-05-31 13:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tablero', '0022_kpi'),
    ]

    operations = [
        migrations.CreateModel(
            name='Escala',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('desde', models.FloatField(default=0)),
                ('hasta', models.FloatField(default=0)),
            ],
        ),
    ]
