from __future__ import unicode_literals

from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^ajax/$', views.index_ajax, name='index-ajax'),
]
