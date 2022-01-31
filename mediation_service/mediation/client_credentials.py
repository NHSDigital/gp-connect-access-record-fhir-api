from time import time
from uuid import uuid4

import jwt
import requests


class AuthClientCredentials:
    __client_assertion_type: str = "urn:ietf:params:oauth:client-assertion-type:jwt-bearer"

    def __init__(self, auth_url: str, private_key_content: str = "", client_id: str = "", aud: str = "",
                 headers: dict = None,
                 alg="RS512") -> None:
        self.__auth_url = auth_url
        self.__client_id = client_id
        self.__aud = aud
        self.__headers = headers
        self.__alg = alg
        self.__signing_key = self.__reformat_private_key(private_key_content)

    def get_access_token(self):
        _jwt = self.__create_jwt(self.__signing_key, self.__client_id, self.__aud, self.__headers, self.__alg)
        data = {
            "client_assertion": _jwt,
            "client_assertion_type": self.__client_assertion_type,
            "grant_type": "client_credentials",
        }
        res = requests.post(f"{self.__auth_url}/token", data)

        if res.status_code != 200:
            raise Exception("Authenticating with client credentials failed", res)

        return res.json()["access_token"]

    @staticmethod
    def __create_jwt(signing_key: str, client_id: str, aud: str, headers: dict, alg="RS512", expiry_sec=5) -> str:
        claims = {
            "sub": client_id,
            "iss": client_id,
            "aud": aud,
            "jti": str(uuid4()),
            "exp": int(time()) + expiry_sec
        }

        return jwt.encode(claims, signing_key, headers=headers, algorithm=alg)

    @staticmethod
    def __reformat_private_key(key):
        """Private key that is passed via environment variable replaces new-lines with spaces.
        This function fixes the issue"""

        begin = "-----BEGIN RSA PRIVATE KEY-----"
        end = "-----END RSA PRIVATE KEY-----"

        key = key.replace(begin, "")
        key = key.replace(end, "")
        key = key.replace(" ", "\n")

        return f"{begin}{key}{end}"
