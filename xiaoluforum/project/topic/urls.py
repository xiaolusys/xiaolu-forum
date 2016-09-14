from __future__ import unicode_literals

from django.conf.urls import url

from . import views


urlpatterns = [
        url(r'^(?P<pk>\d+)/(?P<slug>[\w-]+)/$', views.detail, name='detail'),
        url(r'^active/$', views.index_active, name='index-active'),
        url(r'^index/$', views.index, name='index'),
]
