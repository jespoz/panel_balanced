# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tablero', '0026_auto_20160531_1157'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ciclo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ciclo', models.CharField(max_length=50)),
                ('fecha', models.DateField()),
            ],
        ),
    ]
