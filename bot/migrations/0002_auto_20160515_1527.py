# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='horoscope',
            name='created_date',
            field=models.DateTimeField(verbose_name=b'date scraped'),
        ),
    ]
