import json
import os
import re

import uvicorn
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from starlette.responses import Response
from starlette.status import HTTP_200_OK

from client_credentials import AuthClientCredentials
from pds_client import PdsClient


def init_env():
    try:
        private_key = os.environ["GPC_PRIVATE_KEY_INT"]
        client_id = os.environ["GPC_CLIENT_ID"]
        kid = os.environ["KID"]
        apigee_env = os.environ["APIGEE_ENVIRONMENT"]
    except KeyError as e:
        raise KeyError(f"Environment variable is required: {e}")

    return {
        "private_key": private_key,
        "client_id": client_id,
        "kid": kid,
        "apigee_env": apigee_env
    }


app = FastAPI()


@app.exception_handler(KeyError)
async def env_var_exception_handler(_: Request, exc: KeyError):
    return JSONResponse(
        status_code=500,
        content={"message": str(exc)},
    )


@app.exception_handler(HTTPException)
async def http_client_exception_handler(_: Request, exc: HTTPException):
    return JSONResponse(
        status_code=500,
        content={"message": f"Http request failed with status code {exc.status_code} and message: {exc.detail}"},
    )


@app.exception_handler(ValueError)
async def value_exception_handler(_: Request, exc: ValueError):
    return JSONResponse(
        status_code=500,
        content={"message": f"ValueError: {exc}"},
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(_: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"message": f"Unhandled Error: {exc}"},
    )


def pds_client() -> PdsClient:
    config = init_env()
    auth_url = f"https://{config['apigee_env']}.api.service.nhs.uk/oauth2"
    aud = f"{auth_url}/token"

    auth_client = AuthClientCredentials(auth_url=auth_url,
                                        private_key_content=config["private_key"],
                                        client_id=config["client_id"],
                                        headers={"kid": config["kid"]},
                                        aud=aud)
    auth_client.get_access_token()

    return PdsClient(auth=auth_client, env=config["apigee_env"])


@app.get("/error")
def error(_pds_client: PdsClient = Depends(pds_client)):
    return Response(content=json.dumps({"message": "no error"}), status_code=HTTP_200_OK)


@app.get("/_status")
def status():
    return Response(status_code=HTTP_200_OK)


@app.get("/test")
def test():
    config = init_env()
    auth_url = f"https://{config['apigee_env']}.api.service.nhs.uk/oauth2"
    aud = f"{auth_url}/token"

    auth_client = AuthClientCredentials(auth_url=auth_url,
                                        private_key_content=config["private_key"],
                                        client_id=config["client_id"],
                                        headers={"kid": config["kid"]},
                                        aud=aud)
    # PdsClient(auth=auth_client, env=config["apigee_env"])

    response = {}
    at = ""

    try:
        at = auth_client.get_access_token()
    except Exception as e:
        response["exception"] = str(e)

    response["at"] = at

    return Response(content=json.dumps(response), status_code=HTTP_200_OK)


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
        config = init_env()
    except Exception as e:
        raise HTTPException(status_code=404, detail=e)

    private_key_content = config["private_key"],
    client_id = config["client_id"],
    kid = config["kid"]

    ods = {"private_key": private_key_content, "client_id": client_id, "kid": kid}

    return Response(content=ods, status_code=HTTP_200_OK)


@app.get("/testPdsClientInt")
def test_pds_client(_pds_client: PdsClient = Depends(pds_client)):
    try:
        ods = _pds_client.get_ods_for_nhs_number(9690937286)
    except Exception as e:
        raise HTTPException(status_code=404, detail=e)

    return Response(content=ods, status_code=HTTP_200_OK)


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=9000)
