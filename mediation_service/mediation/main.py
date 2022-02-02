import os
import re

import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from starlette.responses import Response
from starlette.status import HTTP_200_OK

from client_credentials import AuthClientCredentials
from pds_client import PdsClient


def init_dev():
    try:
        private_key = os.environ["GPC_PRIVATE_KEY_INT"]
        client_id = os.environ["GPC_CLIENT_ID"]
        kid = os.environ["KID"]
        apigee_env = os.environ["APIGEE_ENVIRONMENT"]
    except KeyError as e:
        raise Exception(f"Environment variable is required: {e}")

    return {
        "private_key": private_key,
        "client_id": client_id,
        "kid": kid,
        "apigee_env": apigee_env
    }


app = FastAPI()


def pds_client() -> PdsClient:
    config = init_dev()
    auth_url = f"https://{config['apigee_env']}.api.service.nhs.uk/oauth2"
    aud = f"{auth_url}/token"

    auth_client = AuthClientCredentials(auth_url=auth_url,
                                        private_key_content=config["private_key"],
                                        client_id=config["client_id"],
                                        headers={"kid": config["kid"]},
                                        aud=aud)

    return PdsClient(auth=auth_client, env=config["apigee_env"])


@app.get("/_status")
def status():
    return Response(status_code=HTTP_200_OK)


def extract_nhs_number(q: str) -> str:
    r = r"(\d){10}"
    result = re.search(r, q)

    return result.group(0) if result else ""


@app.get("/AllergyIntolerance")
def allergy_intolerance(patient: str, _pds_client: PdsClient = Depends(pds_client)):
    nhs_number = extract_nhs_number(patient)

    ods = _pds_client.get_ods_for_nhs_number(nhs_number)

    return Response(content=ods, status_code=HTTP_200_OK)


@app.get("/testEnvVars")
def get_env_vars():
    try:
        config = init_dev()
    except Exception as e:
        raise HTTPException(status_code=404, detail=e)

    private_key_content = config["private_key"],
    client_id = config["client_id"],
    kid = config["kid"]

    ods = {"private_key": private_key_content, "client_id": client_id, "kid": kid}

    return Response(content=ods, status_code=HTTP_200_OK)


@app.get("/testPdsClientInt")
def test_pds_client( _pds_client: PdsClient = Depends(pds_client)):
    try:
        ods = _pds_client.get_ods_for_nhs_number(9690937286)
    except Exception as e:
        raise HTTPException(status_code=404, detail=e)

    return Response(content=ods, status_code=HTTP_200_OK)


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=9000)
