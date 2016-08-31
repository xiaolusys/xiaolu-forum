# -*- coding: utf-8 -*-
"""
Django settings for running the example of spirit app
"""

from __future__ import unicode_literals

import os
import sys

from spirit.settings import *
# You may override or extend spirit settings below...

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
ST_COMMENT_MAX_LEN = 3000
# Quick-start development settings - unsuitable for production

# Application definition

# This will be the default in next version
ST_RATELIMIT_CACHE = 'st_rate_limit'

# Extend the Spirit installed apps.
# Check out the spirit.settings.py so you do not end up with duplicated apps.
INSTALLED_APPS.extend([
    'django.contrib.sites',
    'raven.contrib.django.raven_compat',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'project.login_provider',
    'project.remind',
    'project.comment',
    'project.topic',
    'project.user',
    'project.category',
    'project.mm',
    'project.push',
])

# same here, check out the spirit.settings.py
MIDDLEWARE_CLASSES.extend([
    # 'my_middleware1',
    # 'my_middleware2',
])

# same here
TEMPLATES[0]['OPTIONS']['context_processors'].extend([
    'django.template.context_processors.request',
    'project.head_portrait.context_processors.head_portrait',
    # 'my_template_proc1',
    # 'my_template_proc2',
])

TEMPLATES[0]['DIRS'] = [
    os.path.join(BASE_DIR, 'templates'),
]


# 小米推送
IOS_APP_SECRET = 'UN+ohC2HYHUlDECbvVKefA=='
ANDROID_APP_SECRET = 'WHdmdNYgnXWokStntg87sg=='

# ================ 小米推送 END ==================

################### PING++ SETTINGS ##################
PINGPP_CLENTIP = "121.199.168.159"
PINGPP_APPID = "app_LOOajDn9u9WDjfHa"
PINGPP_APPKEY = "sk_live_HOS4OSW10u5CDyrn5Gn9izLC"


AUTHENTICATION_BACKENDS.extend([
    'allauth.account.auth_backends.AuthenticationBackend',
])

# same here (we update the Spirit caches)
CACHES.update({
    # 'default': {
    #   'BACKEND': 'my.backend.path',
    # },
})


ROOT_URLCONF = 'project.urls'

WSGI_APPLICATION = 'project.wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

MEDIA_URL = '/static/media/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
HEAD_PORTRAIT = "http://img.xiaolumeimei.com/undefined1472268058597lADOa301H8zIzMg_200_200.jpg_620x10000q90g.jpg?imageMogr2/thumbnail/220/crop/220x220/format/jpg" #官方头像
################### QINIU SETTINGS ##################
QINIU_ACCESS_KEY = "M7M4hlQTLlz_wa5-rGKaQ2sh8zzTrdY8JNKNtvKN"
QINIU_SECRET_KEY = "8MkzPO_X7KhYQjINrnxsJ2eq5bsxKU1XmE8oMi4x"
QINIU_PRIVATE_BUCKET = 'invoiceroom'
QINIU_PRIVATE_DOMAIN = '7xrpt3.com2.z0.glb.qiniucdn.com'
QINIU_PUBLIC_BUCKET = 'xiaolumama'
QINIU_PUBLIC_DOMAIN = '7xrst8.com2.z0.glb.qiniucdn.com'

############### REMOTE MEDIA STORAGE ################
QINIU_BUCKET_NAME   = 'mediaroom'
QINIU_BUCKET_DOMAIN = '7xogkj.com1.z0.glb.clouddn.com'
QINIU_SECURE_URL    = 0
DEFAULT_FILE_STORAGE = 'qiniustorage.backends.QiniuStorage'
MEDIA_URL = "http://%s/" % QINIU_BUCKET_DOMAIN
MEDIA_ROOT = "http://%s/" % QINIU_BUCKET_DOMAIN
# MEDIA_ROOT = os.path.join(BASE_DIR, 'static/media')

# Send an email to the site admins
# on error when DEBUG=False,
# log to console on error always.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': ['require_debug_false'],
        },
        'console': {
            'class': 'logging.StreamHandler',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'django.log'),
        },
        'sentry': {
            'level': 'ERROR',
            'class': 'raven.contrib.django.handlers.SentryHandler'
        },
    },
    'loggers': {
        '': {
            'handlers': ['console', 'sentry'],
            'level': 'ERROR',
            'propagate': False,
        },
        'project': {
            'handlers': ['console', 'sentry'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django': {
            'handlers': ['console', 'sentry'],
            'level': 'ERROR',
            'propagate': False,
        },
    }
}

SITE_ID = 1

LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/accounts/xlmm/login/'
