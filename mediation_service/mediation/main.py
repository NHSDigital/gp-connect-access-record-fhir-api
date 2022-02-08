import os
import re

import requests
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
        apigee_url = os.environ["APIGEE_URL"]
        ssp_url = os.environ["SSP_URL"]
    except KeyError as e:
        raise KeyError(f"Environment variable is required: {e}")

    return {
        "private_key": private_key,
        "client_id": client_id,
        "kid": kid,
        "apigee_env": apigee_env,
        "apigee_url": apigee_url,
        "ssp_url": ssp_url,
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
    auth_url = f"https://{config['apigee_url']}/oauth2"
    aud = f"{auth_url}/token"

    auth_client = AuthClientCredentials(auth_url=auth_url,
                                        private_key_content=config["private_key"],
                                        client_id=config["client_id"],
                                        headers={"kid": config["kid"]},
                                        aud=aud)

    return PdsClient(url=config["apigee_url"], auth=auth_client, env=config["apigee_env"])


@app.get("/_status")
def status():
    return Response(status_code=HTTP_200_OK)


@app.get("/test-ssp")
def status():
    config = init_env()
    res = requests.get(f"https://{config['ssp_url']}")

    return Response(res.text, status_code=HTTP_200_OK)


@app.get("/test-ssp-url")
def status():
    config = init_env()

    return Response(config["ssp_url"], status_code=HTTP_200_OK)


@app.get("/test-is")
def status():
    config = init_env()
    res = requests.get(f"https://{config['apigee_url']}/oauth2/_ping")

    return Response(res.text, status_code=HTTP_200_OK)


@app.get("/test-is-url")
def status():
    config = init_env()
    return Response(config["apigee_url"], status_code=HTTP_200_OK)


def extract_nhs_number(q: str) -> str:
    r = r"(\d){10}"
    result = re.search(r, q)

    return result.group(0) if result else ""


@app.get("/AllergyIntolerance")
def allergy_intolerance(patient: str, _pds_client: PdsClient = Depends(pds_client)):
    nhs_number = extract_nhs_number(patient)

    ods = _pds_client.get_ods_for_nhs_number(nhs_number)

    return Response(content=str(ods), status_code=HTTP_200_OK)


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=9000)
