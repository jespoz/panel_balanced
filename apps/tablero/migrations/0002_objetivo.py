# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-05-05 20:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tablero', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Objetivo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.TextField()),
                ('perspectiva', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tablero.Perspectiva')),
            ],
        ),
    ]