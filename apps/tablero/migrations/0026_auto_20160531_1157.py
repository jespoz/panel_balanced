# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tablero', '0025_auto_20160531_1007'),
    ]

    operations = [
        migrations.AddField(
            model_name='totalindicador',
            name='cumplimiento',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='totalindicador',
            name='meta',
            field=models.FloatField(default=0),
        ),
    ]
