# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-05-18 20:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tablero', '0019_totaldimension'),
    ]

    operations = [
        migrations.AlterField(
            model_name='totaldimension',
            name='indicador',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tablero.Perspectiva'),
        ),
    ]
