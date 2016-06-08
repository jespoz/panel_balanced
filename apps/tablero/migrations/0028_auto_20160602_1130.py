# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tablero', '0027_ciclo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ciclo',
            name='fecha',
            field=models.DateField(null=True, blank=True),
        ),
    ]
