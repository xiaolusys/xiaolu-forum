# -*- coding: utf-8 -*-

# THIS IS FOR DEVELOPMENT ENVIRONMENT
# DO NOT USE IT IN PRODUCTION

# Create your own dev_local.py
# import * this module there and use it like this:
# python manage.py runserver --settings=project.settings.dev_local

from __future__ import unicode_literals

from .base import *


DEBUG = False

TEMPLATES[0]['OPTIONS']['debug'] = False
# TEMPLATES[0]['OPTIONS']['string_if_invalid'] = '{{ %s }}'  # Some Django templates relies on this being the default

ADMINS = (('John', 'john@example.com'), )  # Log email to console when DEBUG = False

SECRET_KEY = "DEV"

ALLOWED_HOSTS = ['.xiaolumm.com', '.xiaolumeimei.com']
SITE_URL = 'forum.xiaolumeimei.com'

# settings for provider auth
AUTH_SITE_URL = 'http://m.xiaolumeimei.com'
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

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
    # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'xiaoluforum',  # Or path to database file if using sqlite3.
        'USER': 'xiaolufdev',  # Not used with sqlite3.\
        'PASSWORD': 'Xiaolu_test123',  # Not used with sqlite3.
        'HOST': 'rm-bp17ea269uu21f9i1.mysql.rds.aliyuncs.com',  # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '3306',  # Set to empty string for default. Not used with sqlite3.
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
        'TIMEOUT': 20
    }
})

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
