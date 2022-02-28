import json
import os
import re
from filter_bundle import BundleFilter
from fhirclient.models.allergyintolerance import AllergyIntolerance

import uvicorn
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from starlette.responses import Response
from starlette.status import HTTP_200_OK

from fhir_converter_client import FhirConverter
from sds_client import SdsClient
from client_credentials import AuthClientCredentials
from pds_client import PdsClient
from ssp_client import SspClient


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
        content={
            "message": f"Http request failed with status code {exc.status_code} and message: {exc.detail}"
        },
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


def auth_client() -> AuthClientCredentials:
    config = init_env()
    auth_url = f"https://{config['apigee_url']}/oauth2"
    aud = "https://int.api.service.nhs.uk/oauth2/token"

    auth_client = AuthClientCredentials(
        auth_url=auth_url,
        private_key_content=config["private_key"],
        client_id=config["client_id"],
        headers={"kid": config["kid"]},
        aud=aud,
    )
    return auth_client


def pds_client() -> PdsClient:
    config = init_env()

    return PdsClient(
        url=config["apigee_url"], env=config["apigee_env"]
    )


def fhir_convert_client() -> FhirConverter:
    config = init_env()
    return FhirConverter(url=config["apigee_url"], env="int")


def ssp_client() -> SspClient:
    config = init_env()
    return SspClient(url=config["ssp_url"])


@app.get("/_status")
def status():
    return Response(status_code=HTTP_200_OK)


def sds_client() -> SdsClient:
    config = init_env()
    return SdsClient(client_id=config["client_id"], apigee_url=config["apigee_url"])


def extract_nhs_number(q: str) -> str:
    r = r"(\d){10}"
    result = re.search(r, q)

    return result.group(0) if result else ""


@app.get("/AllergyIntolerance")
def allergy_intolerance(
    patient: str,
    _pds_client: PdsClient = Depends(pds_client),
    _ssp_client: SspClient = Depends(ssp_client),
    _sds_client: SdsClient = Depends(sds_client),
    _fhir_convert_client: FhirConverter = Depends(fhir_convert_client),
    _auth_client: AuthClientCredentials = Depends(auth_client)
):
    nhs_number = extract_nhs_number(patient)
    access_token = _auth_client.get_access_token()

    ods = _pds_client.get_ods_for_nhs_number(nhs_number, access_token)

    to_ASID = _sds_client.get_toASID(ods)
    GPConnect_URL = _sds_client.get_URL(ods)

    values = {"to_ASID": to_ASID, "GPConnect_URL": GPConnect_URL}

    allergy_bundle = _ssp_client.get_allergy_intolerance_bundle(
        values
    )  # returned as a json str

    bundle_filterer = BundleFilter(AllergyIntolerance)
    filtered_bundle_json = bundle_filterer.filter_for_resource(allergy_bundle.text)
    converted_bundle = _fhir_convert_client.convert(filtered_bundle_json, access_token)

    response_for_test_while_using_orange_test = {
        "to_ASID": to_ASID,
        "GPConnect_URL": GPConnect_URL,
        "response": converted_bundle,
    }

    return Response(
        content=json.dumps(response_for_test_while_using_orange_test),
        status_code=HTTP_200_OK,
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9000)
