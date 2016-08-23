# -*- coding: utf-8 -*-

# THIS IS FOR DEVELOPMENT ENVIRONMENT
# DO NOT USE IT IN PRODUCTION

# This is used to test settings and urls from example directory
# with `./runtests.py example`

from __future__ import unicode_literals

from .base import *


DEBUG = True

SECRET_KEY = "TEST"

INSTALLED_APPS.extend([
    'spirit.core.tests',
])

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db_test.sqlite3'),
    }
}

# ROOT_URLCONF = 'example.project.urls'
SITE_URL = '127.0.0.1'

# settings for provider auth
AUTH_SITE_URL = '127.0.0.1:8000'
AUTH_TOKEN_URL = '%s/o/token/'% AUTH_SITE_URL
AUTH_AUTHORIZE_URL = '%s/o/authorize/'% AUTH_SITE_URL
AUTH_PROFILE_URL = '%s/rest/v1/users/profile'% AUTH_SITE_URL

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

MEDIA_ROOT = os.path.join(BASE_DIR, 'media_test')

STATIC_ROOT = os.path.join(BASE_DIR, 'static_test')
