# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_banuser_is_baned'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banuser',
            name='release_time',
            field=models.DateTimeField(null=True, verbose_name='\u89e3\u5c01\u65f6\u95f4', blank=True),
        ),
        migrations.AlterField(
            model_name='banuser',
            name='update_time',
            field=models.DateTimeField(null=True, verbose_name='\u66f4\u65b0\u65f6\u95f4', blank=True),
        ),
    ]
