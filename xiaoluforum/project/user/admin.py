# -*- coding: utf-8 -*-

from django.contrib import admin
from project.user.models import BanUser

class BanUserAdmin(admin.ModelAdmin):
    list_display = (
        'id','user','username','first_name','days','is_baned'
    )

admin.site.register(BanUser,BanUserAdmin)