from __future__ import unicode_literals

from django.conf.urls import url
from django.conf.urls import url, include
import project.comment.history.urls


urlpatterns = [
    url(r'^history/', include(project.comment.history.urls, namespace='history')),
]
