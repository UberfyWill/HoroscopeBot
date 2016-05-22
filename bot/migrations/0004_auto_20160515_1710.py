# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0003_auto_20160515_1536'),
    ]

    operations = [
        migrations.RenameField(
            model_name='horoscope',
            old_name='date',
            new_name='horoscope_date',
        ),
    ]
