from time import time
from uuid import uuid4

import jwt
import requests
from fastapi import HTTPException


class AuthClientCredentials:
    _client_assertion_type: str = "urn:ietf:params:oauth:client-assertion-type:jwt-bearer"

    def __init__(self, auth_url: str, private_key_content: str = "", client_id: str = "", aud: str = "",
                 headers: dict = None,
                 alg="RS512") -> None:
        self._auth_url = auth_url
        self._client_id = client_id
        self._aud = aud
        self._headers = headers
        self._alg = alg
        self._signing_key = self._reformat_private_key(private_key_content)

    def get_access_token(self):
        _jwt = self._create_jwt(self._signing_key, self._client_id, self._aud, self._headers, self._alg)
        data = {
            "client_assertion": _jwt,
            "client_assertion_type": self._client_assertion_type,
            "grant_type": "client_credentials",
        }
        res = requests.post(f"{self._auth_url}/token", data)

        if res.status_code != 200:
            raise HTTPException(status_code=res.status_code, detail="Client credentials failed.")

        return res.json()["access_token"]

    @staticmethod
    def _create_jwt(signing_key: str, client_id: str, aud: str, headers: dict, alg="RS512", expiry_sec=5) -> str:
        claims = {
            "sub": client_id,
            "iss": client_id,
            "aud": aud,
            "jti": str(uuid4()),
            "exp": int(time()) + expiry_sec
        }

        return jwt.encode(claims, signing_key, headers=headers, algorithm=alg)

    @staticmethod
    def _reformat_private_key(key):
        """Private key that is passed via environment variable replaces new-lines with spaces.
        This function fixes the issue"""

        begin = "-----BEGIN RSA PRIVATE KEY-----"
        end = "-----END RSA PRIVATE KEY-----"

        key = key.replace(begin, "")
        key = key.replace(end, "")
        key = key.replace(" ", "\n")

        return f"{begin}{key}{end}"
