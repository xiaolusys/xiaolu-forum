# -*- coding: utf-8 -*-

# MINIMAL CONFIGURATION FOR PRODUCTION ENV

# Create your own prod_local.py
# import * this module there and use it like this:
# python manage.py runserver --settings=project.settings.prod_local

from __future__ import unicode_literals

from .base import *


DEBUG = False
TEMPLATES[0]['OPTIONS']['debug'] = False
# https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = (('denghui', 'hlkysf@163.com'),)

# Secret key generator: https://djskgen.herokuapp.com/
# You should set your key as an environ variable
SECRET_KEY = 'HicISfd7IEnvyPMOm4fQnvwLK5sreDl0wuS4DAA7ZJ8oZAitF8'

# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['.xiaolumm.com', '.xiaolumeimei.com']

STATIC_ROOT = '/data/forum/static'
MEDIA_ROOT  = '/data/forum/static/media'
SITE_URL    = 'http://forum.xiaolumeimei.com'

# settings for provider auth
AUTH_SITE_URL = 'http://m.xiaolumeimei.com'
AUTH_TOKEN_URL = '%s/o/token/'% AUTH_SITE_URL
AUTH_AUTHORIZE_URL = '%s/o/authorize/'% AUTH_SITE_URL
AUTH_PROFILE_URL = '%s/rest/v1/users/profile'% AUTH_SITE_URL

# You can change this to something like 'MyForum <noreply@example.com>'
DEFAULT_FROM_EMAIL = 'webmaster@localhost'  # Django default
SERVER_EMAIL = DEFAULT_FROM_EMAIL  # For error notifications

# Extend the Spirit installed apps
# Check out the .base.py file for more examples
INSTALLED_APPS.extend([
])

# https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
    # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'xiaoluforum',  # Or path to database file if using sqlite3.
        'USER': 'xiaolufba',  # Not used with sqlite3.
        'PASSWORD': 'Xiaolu_2016forum',  # Not used with sqlite3.
        'HOST': 'rdsvrl2p9pu6536n7d99.mysql.rds.aliyuncs.com',
    # Set to empty string for localhost. Not used with sqlite3. #192.168.0.28
        'PORT': '3306',  # Set to empty string for default. Not used with sqlite3.
        'OPTIONS': {'init_command': 'SET storage_engine=Innodb;',
                    'charset': 'utf8'},  # storage_engine need mysql>5.4,and table_type need mysql<5.4
    }
}

CACHES.update({
    # 'default': {
    #     'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    # },
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': 'rdsvrl2p9pu6536n7d99.mysql.rds.aliyuncs.com',
        'OPTIONS': {
            'DB': 2,
            'PASSWORD': '55a32ec47c8d41f7:Huyiinc12345',
            "SOCKET_CONNECT_TIMEOUT": 5,  # in seconds
            "SOCKET_TIMEOUT": 5,  # in seconds
            # 'PARSER_CLASS': 'redis.connection.HiredisParser',
            'PICKLE_VERSION': 2,
            # 'CONNECTION_POOL_CLASS': 'redis.BlockingConnectionPool',
            'CONNECTION_POOL_CLASS_KWARGS': {
                'max_connections': 50,
                # 'timeout': 10,
            }
        }
    },
    'st_rate_limit': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'spirit_rl_cache',
        'TIMEOUT': 20
    }
})

import raven
RAVEN_CONFIG = {
    'dsn': 'http://ebd1615df16b49b781b07617d95cb608:c444830467e04b4eb431b82f0e12c1d4@sentry.xiaolumm.com/6',
    # If you are using git, you can also automatically configure the
    # release based on the git info.
    'release': raven.fetch_git_sha(os.path.dirname(BASE_DIR)),
}

# These are all the languages Spirit provides.
# https://www.transifex.com/projects/p/spirit/
gettext_noop = lambda s: s
LANGUAGES = [
    ('de', gettext_noop('German')),
    ('en', gettext_noop('English')),
    ('es', gettext_noop('Spanish')),
    ('fr', gettext_noop('French')),
    ('hu', gettext_noop('Hungarian')),
    ('pl', gettext_noop('Polish')),
    ('pl-pl', gettext_noop('Poland Polish')),
    ('ru', gettext_noop('Russian')),
    ('sv', gettext_noop('Swedish')),
    ('tr', gettext_noop('Turkish')),
    ('zh-hans', gettext_noop('Simplified Chinese')),
]

# Default language
LANGUAGE_CODE = 'zh-hans'


TEMPLATES[0]['OPTIONS']['debug'] = False
# Keep templates in memory
del TEMPLATES[0]['APP_DIRS']
TEMPLATES[0]['OPTIONS']['loaders'] = [
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
]

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Append the MD5 hash of the file’s content to the filename
# STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'


PUSH_LOGIN_URL = 'http://m.xiaolumm.com/admin/login/'
PUSH_URL = 'http://m.xiaolumm.com/luntan/at_push/'
PUSH_ADMIN_INFO = {'username':'dev.huideng', 'password': 'yduk9s71'}