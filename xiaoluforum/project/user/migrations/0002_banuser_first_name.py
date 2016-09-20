# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='banuser',
            name='first_name',
            field=models.CharField(max_length=64, verbose_name='\u7528\u6237\u6635\u79f0', blank=True),
        ),
    ]
