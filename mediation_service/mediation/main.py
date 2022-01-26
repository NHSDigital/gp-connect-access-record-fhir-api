import argparse
import os

import uvicorn
from fastapi import FastAPI, Depends
from starlette.responses import Response
from starlette.status import HTTP_200_OK

from client_credentials import AuthClientCredentials
from pds_client import PdsClient

parser = argparse.ArgumentParser()
parser.add_argument("--jwt-key", help="Absolute path to jwt private key file")
parser.add_argument("--client-id", help="Client ID of apigee app")
parser.add_argument("--kid", help="Key id for PDS client credentials")
parser.add_argument("--apigee-env", help="Apigee environment")

app = FastAPI()


def pds_client() -> PdsClient:
    args = parser.parse_args()
    auth_url = f"https://{args.apigee_env}.api.service.nhs.uk/oauth2"
    aud = f"{auth_url}/token"

    auth_client = AuthClientCredentials(auth_url=auth_url,
                                        private_key_file=args.jwt_key,
                                        client_id=args.client_id,
                                        headers={"kid": args.kid},
                                        aud=aud)

    return PdsClient(auth=auth_client, env=args.apigee_env)


@app.get("/_status")
def status():
    return Response(status_code=HTTP_200_OK)


@app.get("/AllergyIntolerance")
def allergy_intolerance(_pds_client: PdsClient = Depends(pds_client)):
    ods = _pds_client.get_ods_for_patient("9691715791")
    print(ods)
    return Response(status_code=HTTP_200_OK)


@app.get("/test")
def test():
    return len(os.environ.get("SDS_SECRET_CLIENT_KEY", "foo"))


@app.get("/test2")
def test2():
    return len(os.environ.get("GPC_PRIVATE_KEY_INT", "foobar"))


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=9000)
