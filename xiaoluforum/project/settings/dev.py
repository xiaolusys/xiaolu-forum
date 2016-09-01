# -*- coding: utf-8 -*-

# THIS IS FOR DEVELOPMENT ENVIRONMENT
# DO NOT USE IT IN PRODUCTION

# Create your own dev_local.py
# import * this module there and use it like this:
# python manage.py runserver --settings=project.settings.dev_local

from __future__ import unicode_literals

from .base import *


DEBUG = True

TEMPLATES[0]['OPTIONS']['debug'] = False
# TEMPLATES[0]['OPTIONS']['string_if_invalid'] = '{{ %s }}'  # Some Django templates relies on this being the default

ADMINS = (('John', 'john@example.com'), )  # Log email to console when DEBUG = False

SECRET_KEY = "DEV"

ALLOWED_HOSTS = ['.xiaolumm.com', '.xiaolumeimei.com']
SITE_URL = 'http://forum-stg.xiaolumm.com'

# settings for provider auth
AUTH_SITE_URL = 'http://staging.xiaolumeimei.com'
AUTH_TOKEN_URL = '%s/o/token/'% AUTH_SITE_URL
AUTH_AUTHORIZE_URL = '%s/o/authorize/'% AUTH_SITE_URL
AUTH_PROFILE_URL = '%s/rest/v1/users/profile'% AUTH_SITE_URL

# INSTALLED_APPS.extend([
#    'debug_toolbar',
# ])


INSTALLED_APPS.extend([
])
#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#    }
#}

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
MEDIA_ROOT = "http://%s/" % QINIU_BUCKET_DOMAIN



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
    # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'xiaoluforum',  # Or path to database file if using sqlite3.
        'USER': 'xiaolufdev',  # Not used with sqlite3.\
        'PASSWORD': 'Xiaolu_test123',  # Not used with sqlite3.
        'HOST': 'dev.xiaolumm.com',  # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '30001',  # Set to empty string for default. Not used with sqlite3.
        'OPTIONS': {'init_command': 'SET storage_engine=Innodb;',
                    'charset': 'utf8'},  # storage_engine need mysql>5.4,and table_type need mysql<5.4
        'TEST': {
            'NAME': 'test_xiaoluforum',
            'CHARSET': 'utf8',
        }
    }
}


CACHES.update({
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    },
    'st_rate_limit': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'spirit_rl_cache',
        'TIMEOUT': None
    }
})


import raven
RAVEN_CONFIG = {
    'dsn': 'http://c4b7824ed957431788b1868cd7bcf4f7:2f3a26553abc4827aa62c665e1fcbe0a@sentry.xiaolumm.com/7',
    # If you are using git, you can also automatically configure the
    # release based on the git info.
    'release': raven.fetch_git_sha(os.path.dirname(BASE_DIR)),
}

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

PUSH_LOGIN_URL = 'http://192.168.1.8:8000/admin/login/'
PUSH_URL = 'http://192.168.1.8:8000/luntan/at_push/'
PUSH_ADMIN_INFO = {'username':'hui.deng', 'password': '139cnm'}