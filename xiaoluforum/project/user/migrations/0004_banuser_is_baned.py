# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_banuser_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='banuser',
            name='is_baned',
            field=models.BooleanField(default=False, verbose_name='\u662f\u5426\u88ab\u7981'),
        ),
    ]
