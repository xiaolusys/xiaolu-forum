# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.utils.translation import ugettext as _
from django.http import HttpResponsePermanentRedirect

from djconfig import config

from spirit.core.utils.paginator import yt_paginate
from spirit.user.utils.email import send_email_change_email
from spirit.user.utils.tokens import UserEmailChangeTokenGenerator
from spirit.topic.models import Topic
from spirit.comment.models import Comment
from spirit.user.forms import UserProfileForm, EmailChangeForm, UserForm, EmailCheckForm
import datetime
User = get_user_model()

@login_required
def _activity(request, pk, slug, queryset, template, reverse_to, context_name, per_page):
    p_user = get_object_or_404(User, pk=pk)

    if p_user.st.slug != slug:
        url = reverse(reverse_to, kwargs={'pk': p_user.pk, 'slug': p_user.st.slug})
        return HttpResponsePermanentRedirect(url)

    items = yt_paginate(
        queryset,
        per_page=per_page,
        page_number=request.GET.get('page', 1)
    )

    context = {
        'p_user': p_user,
        context_name: items
    }

    return render(request, template, context)


def comments(request, pk, slug):
    # todo: test with_polls!
    user_comments = Comment.objects\
        .filter(user_id=pk)\
        .visible()\
        .with_polls(user=request.user)
    for u in user_comments:
        u.date = u.date + datetime.timedelta(hours=8)
	#strdatetime = now.strftime("%Y-%m-%d %H:%M:%S")
        u.date = u.date.strftime("%m-%d")
    return _activity(
        request, pk, slug,
        queryset=user_comments,
        template='spirit/user/profile_comments.html',
        reverse_to='spirit:user:detail',
        context_name='comments',
        per_page=config.comments_per_page,
    )
