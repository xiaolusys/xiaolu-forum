# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from ..push.app_push import AppPush
from allauth.socialaccount.models import SocialAccount

def at_push(comment_user,back_user):
    customer_id = SocialAccount.objects.filter(user_id=comment_user.id).first().extra_data['id']
    msg = back_user.first_name + "给" + comment_user.first_name + "回复一条评论"
    app_push = AppPush()
    app_push.push(customer_id, "com.jimei.xlmm://app/v1/vip_forum", msg)
