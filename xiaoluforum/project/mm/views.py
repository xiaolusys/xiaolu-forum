# coding:utf-8

from django.conf import settings

from rest_framework import permissions
from rest_framework.compat import OrderedDict
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer, BrowsableAPIRenderer
from rest_framework.views import APIView
from rest_framework.response import Response

from qiniu import Auth

class QiniuAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    renderer_classes = (JSONRenderer,)

    def get(self, request):
        access_key = "M7M4hlQTLlz_wa5-rGKaQ2sh8zzTrdY8JNKNtvKN"
        secret_key = "8MkzPO_X7KhYQjINrnxsJ2eq5bsxKU1XmE8oMi4x"
        bucket_name = "xiaolumm"

        q = Auth(access_key, secret_key)
        token = q.upload_token(bucket_name)
        return Response({'uptoken': token})