# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from datetime import timedelta

from django.db import models
from django.utils import timezone
from django.conf import settings

class BanUser(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="用户id", related_name='bu')
    username = models.CharField(verbose_name="用户名",blank=True,max_length=64)
    first_name = models.CharField(verbose_name="用户昵称",blank=True,max_length=64)
    days = models.IntegerField(verbose_name="禁言天数",blank=True)
    create_time = models.DateTimeField(verbose_name="创建时间",auto_now=True)
    update_time = models.DateTimeField(verbose_name="更新时间",blank=True,null=True)
    release_time = models.DateTimeField(verbose_name="解封时间",blank=True,null=True)
    reason = models.TextField(verbose_name="禁言理由",blank=True,max_length=640)
    is_baned = models.BooleanField(verbose_name="是否被禁",default=False)

    class Meta:
        verbose_name = "禁言用户"
        verbose_name_plural = "_禁言用户"

