# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tablero', '0009_proyecto_unidad'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='perspectiva',
            options={'verbose_name': 'Dimension', 'verbose_name_plural': 'Dimensiones'},
        ),
        migrations.AddField(
            model_name='perspectiva',
            name='color',
            field=models.CharField(max_length=7, null=True, blank=True),
        ),
    ]
