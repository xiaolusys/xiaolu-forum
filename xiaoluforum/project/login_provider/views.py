import requests
from django.conf import settings
from allauth.socialaccount.providers.oauth2.views import (OAuth2Adapter,
                                                          OAuth2LoginView,
                                                          OAuth2CallbackView)
from .provider import XLMMProvider
from allauth.socialaccount import app_settings


class XLMMOAuth2Adapter(OAuth2Adapter):
    provider_id = XLMMProvider.id
    access_token_url = settings.AUTH_TOKEN_URL
    authorize_url = settings.AUTH_AUTHORIZE_URL
    profile_url = settings.AUTH_PROFILE_URL

    def complete_login(self, request, app, token, **kwargs):
        resp = requests.get(self.profile_url,
                            params={'access_token': token.token})
        extra_data = resp.json()
        return self.get_provider().sociallogin_from_response(request,
                                                             extra_data)

oauth2_login = OAuth2LoginView.adapter_view(XLMMOAuth2Adapter)
oauth2_callback = OAuth2CallbackView.adapter_view(XLMMOAuth2Adapter)
