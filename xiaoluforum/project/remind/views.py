from __future__ import unicode_literals
import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import Http404, HttpResponse
from django.conf import settings
from django.contrib import messages
from django.utils.html import escape

from djconfig import config

from spirit.core import utils
from spirit.core.utils.paginator import yt_paginate
from spirit.core.utils.paginator.infinite_paginator import paginate
from spirit.topic.models import Topic
from spirit.topic.notification.models import TopicNotification
from spirit.topic.notification.forms import NotificationForm, NotificationCreationForm

@login_required
def index_ajax(request):
    print "daole "
    if not request.is_ajax():
        return Http404()

    notifications = TopicNotification.objects\
        .for_access(request.user)\
        .order_by("is_read", "-date")\
        .select_related('comment__user__st', 'comment__topic')

    notifications = notifications[:settings.ST_NOTIFICATIONS_PER_PAGE]

    notifications = [
        {
            'user': escape(n.comment.user.first_name),
            'action': n.action,
            'title': escape(n.comment.topic.title),
            'url': n.get_absolute_url(),
            'is_read': n.is_read
        }
        for n in notifications
    ]

    return HttpResponse(json.dumps({'n': notifications, }), content_type="application/json")
