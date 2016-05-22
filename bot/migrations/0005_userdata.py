# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0004_auto_20160515_1710'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_id', models.CharField(max_length=100)),
                ('mid', models.CharField(max_length=200)),
                ('msg_txt', models.CharField(max_length=10000)),
                ('timestamp', models.CharField(max_length=100)),
                ('page_id', models.CharField(max_length=100)),
                ('recent_question', models.CharField(max_length=500)),
            ],
        ),
    ]
