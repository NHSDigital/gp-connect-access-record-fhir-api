import gevent.monkey
# If gevent is installed, it needs to monkey-patch the python sockets to cooperate (see documentation or this
# github issue https://github.com/gevent/gevent/issues/941).
gevent.monkey.patch_all()
import requests
import json
import urllib.parse as urlparse
from urllib.parse import parse_qs

"""
Based on NHSDigital/personal-demographics-service-api/blob/master/tests/performance/auth.py

This class is useful for authenticating Locust simulated users that need to hit endpoints that require NHS Login
authorisation, instantiate an Auth object within your TestUser Locust class, call `Auth.login()` within the
Locust HttpUser's `on_start()` method, and pass the auth headers in your requests.
"""


class Auth:
    def __init__(self, url, callback_url, client_id, client_secret):
        self.session = requests.Session()
        self.base_url = url
        self.callback_url = callback_url
        self.client_id = client_id
        self.client_secret = client_secret

    def login(self):
        state = self.get_state()
        redirect = self.get_redirect_callback(state)
        code = self.get_auth_code(redirect)
        return self.get_access_token(code)

    def get_state(self):
        url = f"{self.base_url}/oauth2/authorize"
        params = {
            "client_id": self.client_id,
            "redirect_uri": self.callback_url,
            "response_type": "code",
            "scope": "nhs-login",
            "state": "1234567890"
        }
        response = self.session.get(url, params=params)
        parsed = urlparse.urlparse(response.url)
        return parse_qs(parsed.query)['state'][0]

    def get_redirect_callback(self, state):
        url = "https://internal-dev.api.service.nhs.uk/mock-nhsid-jwks/nhs_login_simulated_auth"
        params = {
            "response_type": "code",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "redirect_uri": self.callback_url,
            "scope": "nhs-login",
            "state": state
        }
        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip,deflate",
            "Cache-Control": "max-age=0",
            "Content-Type": "application/x-www-form-urlencoded",
            "Upgrade-Insecure-Requests": "1"
        }
        payload = {
            "state": state
        }
        response = self.session.post(url, params=params, data=payload, headers=headers, allow_redirects=False)
        redirect = response.headers['Location']
        return redirect

    def get_auth_code(self, redirect_url):
        response = self.session.get(redirect_url, allow_redirects=False)
        parsed = urlparse.urlparse(response.headers['Location'])

        return parse_qs(parsed.query)["code"][0]

    def get_access_token(self, code):
        url = f"{self.base_url}/oauth2/token"
        headers = {
            "Accept": "*/*",
            "connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        payload = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self.callback_url,
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }
        response = self.session.post(url, data=payload, headers=headers, allow_redirects=False)

        credentials = json.loads(response.text)
        return credentials
