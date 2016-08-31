# encoding=utf8
"""
APP　推送
"""
import json
import logging
from .mipush import mipush_of_ios, mipush_of_android




logger = logging.getLogger('service')


class AppPush(object):

    def __init__(self):
        pass

    @classmethod
    def push(cls, customer_id, target_url, msg, pass_through=0):
        android_res = mipush_of_android.push_to_account(
            customer_id, {'target_url': target_url}, description=msg, pass_through=pass_through)
        ios_res = mipush_of_ios.push_to_account(
            customer_id, {'target_url': target_url}, description=msg, pass_through=pass_through)

        logger.info({
            'action': 'push.apppush',
            'customer': customer_id,
            'msg': msg,
            'target_url': target_url,
            'android_res': json.dumps(android_res),
            'ios_res': json.dumps(ios_res)
        })
        return {'android': android_res, 'ios': ios_res}

