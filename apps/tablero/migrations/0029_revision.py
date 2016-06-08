# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tablero', '0028_auto_20160602_1130'),
    ]

    operations = [
        migrations.CreateModel(
            name='Revision',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('observacion', models.TextField(null=True, blank=True)),
                ('avance', models.FloatField(default=0)),
                ('ciclo', models.ForeignKey(to='tablero.Ciclo')),
                ('proyecto', models.ForeignKey(to='tablero.Proyecto')),
            ],
            options={
                'verbose_name_plural': 'Revisiones',
            },
        ),
    ]
