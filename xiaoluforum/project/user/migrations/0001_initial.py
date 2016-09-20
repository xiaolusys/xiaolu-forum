# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BanUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('days', models.IntegerField(verbose_name='\u7981\u8a00\u5929\u6570', blank=True)),
                ('create_time', models.DateTimeField(auto_now=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('update_time', models.DateTimeField(verbose_name='\u66f4\u65b0\u65f6\u95f4', blank=True)),
                ('release_time', models.DateTimeField(verbose_name='\u89e3\u5c01\u65f6\u95f4', blank=True)),
                ('reason', models.TextField(max_length=640, verbose_name='\u7981\u8a00\u7406\u7531', blank=True)),
                ('user', models.ForeignKey(related_name='bu', verbose_name='\u7528\u6237id', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '\u7981\u8a00\u7528\u6237',
                'verbose_name_plural': '_\u7981\u8a00\u7528\u6237',
            },
        ),
    ]
