# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-06-06 20:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tablero', '0029_revision'),
    ]

    operations = [
        migrations.CreateModel(
            name='TotalCicloUnidad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avance', models.FloatField(default=0)),
                ('ciclo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tablero.Ciclo')),
                ('unidad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tablero.Unidad')),
            ],
        ),
    ]
