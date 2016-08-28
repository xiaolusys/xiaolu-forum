from django.conf import settings

def head_portrait(request):
    return {'HEAD_PORTRAIT' : settings.HEAD_PORTRAIT}