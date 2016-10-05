# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponsePermanentRedirect,HttpResponse

from djconfig import config

from spirit.core.utils.paginator import paginate, yt_paginate
from spirit.core.utils.ratelimit.decorators import ratelimit
from spirit.category.models import Category
from spirit.comment.models import MOVED
from spirit.comment.forms import CommentForm
from spirit.comment.utils import comment_posted
from spirit.comment.models import Comment
from spirit.topic.models import Topic
from django.db.models import Sum
from spirit.topic.forms import TopicForm
from spirit.topic import utils
from project.user.models import BanUser
import datetime

from .extra import *


def detail(request, pk, slug):
    bu = BanUser.objects.filter(username=request.user).first()
    topic = Topic.objects.get_public_or_404(pk, request.user)
    
    if topic.slug != slug:
        return HttpResponsePermanentRedirect(topic.get_absolute_url())

    utils.topic_viewed(request=request, topic=topic)

    comments = Comment.objects\
        .for_topic(topic=topic)\
        .with_likes(user=request.user)\
        .with_polls(user=request.user)\
        .order_by('date')
    comments = paginate(
        comments,
        per_page=config.comments_per_page,
        page_number=request.GET.get('page', 1)
    )

    for c in comments:
        if bu and bu.is_baned and c.user == request.user:
            c.is_removed = 0
        c.date = c.date+datetime.timedelta(hours=8)
	#strdatetime = now.strftime("%Y-%m-%d %H:%M:%S")
        c.date = c.date.strftime("%m-%d")

    context = {
        'topic': topic,
        'comments': comments
    }

    return render(request, 'spirit/topic/detail.html', context)


def index_active(request):
    categories = Category.objects\
        .visible()\
        .parents()
    cat = get_topic_by_mysort(*categories)

    topics = Topic.objects\
        .visible()\
        .global_()\
        .with_bookmarks(user=request.user)\
        .order_by('-is_globally_pinned', '-date')\
        .select_related('category')

    for topic in topics:
        topic.like_counts = get_likes_count_by_topic(topic)
        topic.first_comment = get_first_comment_by_topic(topic)

    topics = yt_paginate(
        topics,
        per_page=config.topics_per_page,
        page_number=request.GET.get('page', 1)
    )

    for t in topics:
        t.last_active = t.last_active+datetime.timedelta(hours=8)
	#strdatetime = now.strftime("%Y-%m-%d %H:%M:%S")
        t.last_active = t.last_active.strftime("%Y-%m-%d")
        t.date = t.date + datetime.timedelta(hours=8)
        t.date = t.date.strftime("%Y-%m-%d")
        print t.date
    context = {
        'categories': cat,
        'topics': topics
    }
    for c in categories:
        if c.title == "活动通知":
            return redirect(c.get_absolute_url())
    return render(request, 'spirit/topic/active.html', context)

def index(request):
    categories = Category.objects\
        .visible()\
        .parents()
    cat = get_topic_by_mysort(*categories)

    topics = Topic.objects\
        .visible()\
        .global_()\
        .with_bookmarks(user=request.user)\
        .order_by('-is_globally_pinned', '-date')\
        .select_related('category')

    for topic in topics:
        topic.like_counts = get_likes_count_by_topic(topic)
        topic.first_comment = get_first_comment_by_topic(topic)

    topics = yt_paginate(
        topics,
        per_page=config.topics_per_page,
        page_number=request.GET.get('page', 1)
    )

    for t in topics:
        t.last_active = t.last_active+datetime.timedelta(hours=8)
	#strdatetime = now.strftime("%Y-%m-%d %H:%M:%S")
        t.last_active = t.last_active.strftime("%Y-%m-%d")
        t.date = t.date + datetime.timedelta(hours=8)
        t.date = t.date.strftime("%Y-%m-%d")
        print t.date
    context = {
        'categories': cat,
        'topics': topics
    }
    return render(request, 'spirit/topic/active.html', context)