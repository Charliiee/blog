import json
from urllib.request import urlopen

from flask import current_app, redirect, request, url_for
from rauth import OAuth2Service



class OAuthSignIn(object):
    providers = None

    def __init__(self, provider_name):
        self.provider_name = provider_name
        credentials = current_app.config['OAUTH_CREDENTIALS'][provider_name]
        self.consumer_id = credentials['id']
        self.consumer_secret = credentials['secret']

    def authorize(self):
        pass

    def callback(self):
        pass

    def get_callback_url(self):
        return url_for('oauth_callback',
                       provider=self.provider_name,
                       _external=True)

    @classmethod
    def get_provider(cls, provider_name):
        if cls.providers is None:
            cls.providers = {}
            for provider_class in cls.__subclasses__():
                provider = provider_class()
                cls.providers[provider.provider_name] = provider
        return cls.providers[provider_name]


class FacebookSignIn(OAuthSignIn):

    def __init__(self):
        super(FacebookSignIn, self).__init__('facebook')
        self.service = OAuth2Service(
            name='facebook',
            client_id=self.consumer_id,
            client_secret=self.consumer_secret,
            authorize_url='https://graph.facebook.com/oauth/authorize',
            access_token_url='https://graph.facebook.com/oauth/access_token',
            base_url='https://graph.facebook.com/'
        )

    def authorize(self):
        return redirect(self.service.get_authorize_url(
                        scope='email',
                        response_type='code',
                        redirect_uri=self.get_callback_url())
                        )

    def callback(self):
        if 'code' not in request.args:
            return None, None, None
        oauth_session = self.service.get_auth_session(
            data={'code': request.args['code'],
                  'grant_type': 'authorization_code',
                  'redirect_uri': self.get_callback_url()
                  }
        )
        me = oauth_session.get('me?fields=id,email,first_name').json()
        return ('facebook$' + me['id'], me['first_name'], me.get('email'))


class GoogleSignIn(OAuthSignIn):

    def __init__(self):
        super(GoogleSignIn, self).__init__('google')
        googleinfo = urlopen(
            'https://accounts.google.com/.well-known/openid-configuration'
        ).read().decode('utf-8')

        google_params = json.loads(googleinfo)
        self.service = OAuth2Service(
            name='google',
            client_id=self.consumer_id,
            client_secret=self.consumer_secret,
            authorize_url=google_params.get('authorization_endpoint'),
            access_token_url=google_params.get('token_endpoint'),
            base_url=google_params.get('userinfo_endpoint')
        )

    def authorize(self):
        return redirect(self.service.get_authorize_url(
                        scope='email',
                        response_type='code',
                        redirect_uri=self.get_callback_url())
                        )

    def callback(self):
        if 'code' not in request.args:
            return None, None, None
        # Google response crashes service.get_auth_session() on python 3
        # but getting raw access token doesn't, though  get_auth_session
        # just call this one. It's probably a not handled json case for python3
        response = self.service.get_raw_access_token(
            data={'code': request.args['code'],
                  'grant_type': 'authorization_code',
                  'redirect_uri': self.get_callback_url()
                  }
        )
        response = response.json()
        oauth_session = self.service.get_session(response['access_token'])
        me = oauth_session.get('https://www.googleapis.com/oauth2/v2/userinfo')
        me = me.json()
        return ('google$' + me['id'], me['given_name'], me.get('email'))

# class TwitterSignIn(OAuthSignIn):
#     pass
