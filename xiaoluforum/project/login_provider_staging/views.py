import requests

from allauth.socialaccount.providers.oauth2.views import (OAuth2Adapter,
                                                          OAuth2LoginView,
                                                          OAuth2CallbackView)
from .provider import XLMMProvider
from allauth.socialaccount import app_settings


class XLMMOAuth2Adapter(OAuth2Adapter):
    provider_id = XLMMProvider.id
    access_token_url = 'http://staging.xiaolumeimei.com/o/token/'
    authorize_url = 'http://staging.xiaolumeimei.com/o/authorize/'
    profile_url = 'http://staging.xiaolumeimei.com/rest/v1/users/profile'

    def complete_login(self, request, app, token, **kwargs):
        resp = requests.get(self.profile_url,
                            params={'access_token': token.token})
        extra_data = resp.json()
        return self.get_provider().sociallogin_from_response(request,
                                                             extra_data)

oauth2_login = OAuth2LoginView.adapter_view(XLMMOAuth2Adapter)
oauth2_callback = OAuth2CallbackView.adapter_view(XLMMOAuth2Adapter)
