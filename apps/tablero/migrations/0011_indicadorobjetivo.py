# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tablero', '0010_auto_20160512_1130'),
    ]

    operations = [
        migrations.CreateModel(
            name='IndicadorObjetivo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('descripcion', models.CharField(max_length=100)),
                ('activo', models.BooleanField(default=False)),
                ('objetivo', models.ForeignKey(to='tablero.Objetivo')),
                ('responsable', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Indicador por Objetivo',
                'verbose_name_plural': 'Indicadores por Objetivo',
            },
        ),
    ]
