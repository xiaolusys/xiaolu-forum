# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.utils.translation import ugettext as _
from django.utils.html import mark_safe

from spirit.core.tags.registry import register
from spirit.comment.poll.utils.render import render_polls
from spirit.comment.forms import CommentForm
from spirit.comment.models import MOVED, CLOSED, UNCLOSED, PINNED, UNPINNED

#tag传入的参数带user,这样子页面也能读取当前的user
@register.inclusion_tag('spirit/comment/_form.html')
def render_comments_form_user(topic, user, next=None):
    form = CommentForm()
    return {'form': form, 'topic_id': topic.pk, 'user': user, 'next': next}