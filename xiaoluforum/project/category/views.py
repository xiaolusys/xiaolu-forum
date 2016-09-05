# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.views.generic import ListView
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponsePermanentRedirect

from djconfig import config

from spirit.core.utils.paginator import yt_paginate
from spirit.topic.models import Topic
from spirit.category.models import Category
import datetime

from ..topic.extra import *

def detail(request, pk, slug):
    categories = Category.objects\
        .visible()\
        .parents()
    category = get_object_or_404(Category.objects.visible(),
                                 pk=pk)

    if category.slug != slug:
        return HttpResponsePermanentRedirect(category.get_absolute_url())

    subcategories = Category.objects\
        .visible()\
        .children(parent=category)

    topics = Topic.objects\
        .unremoved()\
        .with_bookmarks(user=request.user)\
        .for_category(category=category)\
        .order_by('-is_globally_pinned', '-is_pinned', '-last_active')\
        .select_related('category')

    for i in topics:
        i.last_active = i.last_active + datetime.timedelta(hours=8)
        # strdatetime = now.strftime("%Y-%m-%d %H:%M:%S")
        i.last_active = i.last_active.strftime("%Y-%m-%d")

    for topic in topics:
        topic.like_counts = get_likes_count_by_topic(topic)
        topic.first_comment = get_first_comment_by_topic(topic)


    topics = yt_paginate(
        topics,
        per_page=config.topics_per_page,
        page_number=request.GET.get('page', 1)
    )

    context = {
        'topcategories':categories,       #在渲染一个帖子分类的时候,显示所有的帖子分类,原来的情况是如果选了一个帖子分类,其他的帖子分类不会显示
        'category': category,
        'subcategories': subcategories,
        'topics': topics
    }

    return render(request, 'spirit/category/detail.html', context)


class IndexView(ListView):

    template_name = 'spirit/category/index.html'
    context_object_name = "categories"
    queryset = Category.objects.visible().parents()
