# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_banuser_first_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='banuser',
            name='username',
            field=models.CharField(max_length=64, verbose_name='\u7528\u6237\u540d', blank=True),
        ),
    ]
