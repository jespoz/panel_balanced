# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-05-06 13:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tablero', '0005_administradorunidad'),
    ]

    operations = [
        migrations.AlterField(
            model_name='administradorunidad',
            name='unidad',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='tablero.Unidad'),
        ),
    ]