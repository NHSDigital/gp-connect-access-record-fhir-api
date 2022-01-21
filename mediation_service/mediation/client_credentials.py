from time import time
from typing import NamedTuple
from uuid import uuid4

import jwt
import requests


class Claims(NamedTuple):
    sub: str
    iss: str
    aud: str
    exp: int
    jti: str

    def dict(self):
        return self._asdict()

    @staticmethod
    def new(client_id: str, aud: str, valid_for_sec=5):
        return Claims(
            sub=client_id,
            iss=client_id,
            aud=aud,
            jti=str(uuid4()),
            exp=int(time()) + valid_for_sec
        )


def create_jwt(signing_key: str, client_id: str, aud: str, headers: dict, alg="RS512") -> str:
    claims = Claims.new(client_id, aud).dict()

    return jwt.encode(claims, signing_key, headers=headers, algorithm=alg)


class AuthClientCredentials:
    __client_assertion_type: str = "urn:ietf:params:oauth:client-assertion-type:jwt-bearer"

    def __init__(self, auth_url: str, private_key_file: str = "", client_id: str = "", aud: str = "",
                 headers: dict = None,
                 alg="RS512") -> None:
        self.__auth_url = auth_url
        self.__client_id = client_id
        self.__aud = aud
        self.__headers = headers
        self.__alg = alg

        if private_key_file:
            with open(private_key_file, "r") as f:
                self.__signing_key = f.read()

    def get_access_token(self):
        _jwt = create_jwt(self.__signing_key, self.__client_id, self.__aud, self.__headers, self.__alg)
        data = {
            "client_assertion": _jwt,
            "client_assertion_type": self.__client_assertion_type,
            "grant_type": "client_credentials",
        }
        res = requests.post(f"{self.__auth_url}/token", data)

        if res.status_code != 200:
            raise Exception("Authenticating with client credentials failed", res)

        return res.json()["access_token"]
