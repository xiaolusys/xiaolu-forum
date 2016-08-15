# -*- coding: utf-8 -*-
import os
from django.core.wsgi import get_wsgi_application

if os.environ.get('TARGET') in ('staging',):
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings.staging")

elif os.environ.get('TARGET') in ('production',):
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "product.settings.production")

application = get_wsgi_application()