#!/usr/bin/env python

import os
import sys

if __name__ == "__main__":
    if os.environ.get('TARGET') in ('staging',):
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings.staging")

    elif os.environ.get('TARGET') in ('production',):
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "product.settings.production")

    else:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings.test")

    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
