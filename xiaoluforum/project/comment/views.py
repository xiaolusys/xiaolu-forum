# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.http import Http404

from djconfig import config

from spirit.core.utils.ratelimit.decorators import ratelimit
from spirit.core.utils.decorators import moderator_required
from spirit.core.utils import markdown, paginator, render_form_errors, json_response
from spirit.topic.models import Topic
from spirit.comment.models import Comment
from spirit.comment.forms import CommentForm, CommentMoveForm #取消从spirit.comment下载入CommentImageForm,从当前中导入CommentImageForm
from .forms import CommentImageForm
from spirit.comment.utils import comment_posted, post_comment_update, pre_comment_update

from ..push.app_push import AppPush
from allauth.socialaccount.models import SocialAccount
from .utils import at_push

@login_required
@ratelimit(rate='1/10s')
def publish(request, topic_id, pk=None):
    topic = get_object_or_404(
        Topic.objects.opened().for_access(request.user),
        pk=topic_id
    )

    if request.method == 'POST':
        form = CommentForm(user=request.user, topic=topic, data=request.POST)

        if not request.is_limited and form.is_valid():
            comment = form.save()
            comment_posted(comment=comment, mentions=form.mentions)
            Comment.objects.for_access(user=request.user)
            if pk:
                comment = get_object_or_404(Comment.objects.for_access(user=request.user), pk=pk)
                at_push(comment.user,request.user)
                # print request.user.first_name+"给"+comment.user.first_name+"发了一条消息"
                # msg = request.user.first_name + "给" + comment.user.first_name + "回复一条评论"
                # customer_id = SocialAccount.objects.filter(user_id=comment.user.id).first().extra_data['id']
                # print customer_id
                # app_push = AppPush()
                # app_push.push(customer_id,"com.jimei.xlmm://app/v1/vip_forum",msg)
            return redirect(request.POST.get('next', comment.get_absolute_url()))
    else:
        initial = None

        if pk:
            comment = get_object_or_404(Comment.objects.for_access(user=request.user), pk=pk)
            quote = markdown.quotify(comment.comment, comment.user.first_name)
            initial = {'comment': quote, }
        form = CommentForm(initial=initial)

    context = {
        'form': form,
        'topic': topic
    }

    return render(request, 'spirit/comment/publish.html', context)


@login_required
def update(request, pk):
    comment = Comment.objects.for_update_or_404(pk, request.user)

    if request.method == 'POST':
        form = CommentForm(data=request.POST, instance=comment)

        if form.is_valid():
            pre_comment_update(comment=Comment.objects.get(pk=comment.pk))
            comment = form.save()
            post_comment_update(comment=comment)
            return redirect(request.POST.get('next', comment.get_absolute_url()))
    else:
        form = CommentForm(instance=comment)

    context = {'form': form, }

    return render(request, 'spirit/comment/update.html', context)


@moderator_required
def delete(request, pk, remove=True):
    comment = get_object_or_404(Comment, pk=pk)

    if request.method == 'POST':
        Comment.objects\
            .filter(pk=pk)\
            .update(is_removed=remove)

        return redirect(comment.get_absolute_url())

    context = {'comment': comment, }

    return render(request, 'spirit/comment/moderate.html', context)


@require_POST
@moderator_required
def move(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id)
    form = CommentMoveForm(topic=topic, data=request.POST)

    if form.is_valid():
        comments = form.save()

        for comment in comments:
            comment_posted(comment=comment, mentions=None)
            topic.decrease_comment_count()
    else:
        messages.error(request, render_form_errors(form))

    return redirect(request.POST.get('next', topic.get_absolute_url()))


def find(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment_number = Comment.objects.filter(topic=comment.topic, date__lte=comment.date).count()
    url = paginator.get_url(comment.topic.get_absolute_url(),
                            comment_number,
                            config.comments_per_page,
                            'page')
    return redirect(url)



@require_POST
@login_required
def image_upload_ajax(request):
    if not request.is_ajax():
        return Http404()

    form = CommentImageForm(user=request.user, data=request.POST, files=request.FILES)

    if form.is_valid():
        image = form.save()
        return json_response({'url': image.url, })

    return json_response({'error': dict(form.errors.items()), })
