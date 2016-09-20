from __future__ import unicode_literals

from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^(?P<pk>\d+)/(?P<slug>[\w-]+)/$', views.comments, name='detail'),
    url(r'^(?P<pk>\d+)/ban/(?P<comment_id>\d+)/$', views.ban_user,name='ban')
]
