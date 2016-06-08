# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-05-31 13:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tablero', '0023_escala'),
    ]

    operations = [
        migrations.AddField(
            model_name='escala',
            name='color',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='tablero.Color'),
            preserve_default=False,
        ),
    ]