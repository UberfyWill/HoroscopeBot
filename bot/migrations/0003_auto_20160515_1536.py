# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0002_auto_20160515_1527'),
    ]

    operations = [
        migrations.AlterField(
            model_name='horoscope',
            name='created_date',
            field=models.CharField(max_length=100),
        ),
    ]
