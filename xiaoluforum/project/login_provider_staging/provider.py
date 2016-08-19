from allauth.socialaccount import providers
from allauth.socialaccount.providers.base import ProviderAccount
from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider


class XLMMAccount(ProviderAccount):
    def get_avatar_url(self):
        return self.account.extra_data.get('thumbmail')

    def to_str(self):
        dflt = super(XLMMAccount, self).to_str()
        return next(
            value
            for value in (
                self.account.extra_data.get('nick', None),
                self.account.extra_data.get('username', None),
                dflt
            )
            if value is not None
        )


class XLMMProvider(OAuth2Provider):
    id = 'xlmm'
    name = 'XLMM'
    account_class = XLMMAccount

    def get_default_scope(self):
        return ['read']

    def extract_uid(self, data):
        return str(data['id'])

    def extract_common_fields(self, data):
        return dict(email=data.get('email'),
                    username=data.get('username'),
                    name=data.get('nick'))


providers.registry.register(XLMMProvider)
