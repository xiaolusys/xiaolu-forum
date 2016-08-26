# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

import spirit.urls
import project.comment.urls
import project.topic.urls
import project.user.urls
import project.category.urls
import project.topic.views

# Override admin login for security purposes
from django.contrib.auth.decorators import login_required
admin.site.login = login_required(admin.site.login)


urlpatterns = [
    # Examples:
    # url(r'^$', 'example.views.home', name='home'),
    # url(r'^example/', include('example.foo.urls')),
    url(r'^topic/notification/',include('project.remind.urls')),
    url(r'^comment/', include(project.comment.urls, namespace='comment')),
    url(r'^topic/', include(project.topic.urls, namespace='topic')),
    url(r'^user/', include(project.user.urls, namespace='user')),
    url(r'^category/', include(project.category.urls, namespace='category')),
    url(r'^$', project.topic.views.index_active, name='index'),
    url(r'^', include(spirit.urls)),
    url(r'^accounts/', include('allauth.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
