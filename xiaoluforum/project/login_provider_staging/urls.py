from allauth.socialaccount.providers.oauth2.urls import default_urlpatterns
from .provider import XLMMProvider

urlpatterns = default_urlpatterns(XLMMProvider)
