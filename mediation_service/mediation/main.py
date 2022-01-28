import os
from idlelib.query import Query

import uvicorn
from fastapi import FastAPI, Depends
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


@app.get("/AllergyIntolerance/{patient_id}")
def allergy_intolerance(patient_id: str = Query(..., min_length=3), _pds_client: PdsClient = Depends(pds_client)):
    ods = _pds_client.get_ods_for_patient(patient_id)
    print(ods)
    return Response(content=ods, status_code=HTTP_200_OK)


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=9000)
