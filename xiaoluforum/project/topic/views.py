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
import logging

logger = logging.getLogger(__name__)

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

def index(request):
    categories = Category.objects\
        .visible()\
        .parents()
    cat = get_topic_by_mysort(*categories)

    topics = Topic.objects \
        .visible() \
        .global_() \
        .with_bookmarks(user=request.user) \
        .order_by('-is_globally_pinned', '-date') \
        .select_related('category')

    topics = yt_paginate(
        topics,
        per_page=config.topics_per_page,
        page_number=request.GET.get('page', 1)
    )

    topics = fill_likes_count_and_first_comment_by_topics(topics)

    for t in topics:
        t.last_active = t.last_active + datetime.timedelta(hours=8)
        # strdatetime = now.strftime("%Y-%m-%d %H:%M:%S")
        t.last_active = t.last_active.strftime("%Y-%m-%d")
        t.date = t.date + datetime.timedelta(hours=8)
        t.date = t.date.strftime("%Y-%m-%d")

    context = {
        'categories': cat,
        'topics': topics
    }
    return render(request, 'spirit/topic/active.html', context)


def index_active(request):
    categories = Category.objects\
        .visible()\
        .parents()
    for c in categories:
        if c.title == "活动通知":
            # return HttpResponse('<html><head><title>test</title></head><body>success</body></html>')
            return redirect(c.get_absolute_url())

    return index(request)

@login_required
@ratelimit(rate='1/10s')
def publish(request, category_id=None):
    title = request.POST.get("title",'')
    comment = request.POST.get("comment",'')
    title = not title.isspace()          #如果里面全是空格,不允许通过
    comment = not comment.isspace()

    # logger.warn({"action":"publish_topic", "title_comment_info":title+comment})
    # topic = Topic()
    # if not all([title,comment]):
    #     return HttpResponse(123)

    if category_id:
        get_object_or_404(Category.objects.visible(),
                          pk=category_id)

    if request.method == 'POST':
        form = TopicForm(user=request.user, data=request.POST)
        cform = CommentForm(user=request.user, data=request.POST)

        if not request.is_limited and all([form.is_valid(), cform.is_valid()]) and all([title,comment]):  # TODO: test!
            # wrap in transaction.atomic?

            topic = form.save()
            cform.topic = topic
            comment = cform.save()
            comment_posted(comment=comment, mentions=cform.mentions)
            return redirect(topic.get_absolute_url())
    else:
        category_id = 2  #七嘴八舌为默认选择分类
        form = TopicForm(user=request.user, initial={'category': category_id, })
        cform = CommentForm()

    context = {
        'form': form,
        'cform': cform
    }

    return render(request, 'spirit/topic/publish.html', context)