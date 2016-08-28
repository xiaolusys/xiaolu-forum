from __future__ import unicode_literals

from django.conf.urls import url
from django.conf.urls import url, include
import project.comment.history.urls
from . import views

urlpatterns = [
    url(r'^history/', include(project.comment.history.urls, namespace='history')),
    url(r'^(?P<topic_id>\d+)/publish/(?P<pk>\d+)/quote/$', views.publish, name='publish'),
]
