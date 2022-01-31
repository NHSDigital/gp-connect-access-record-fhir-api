import os
import uvicorn
from fastapi import FastAPI, Depends
from starlette.responses import Response
from starlette.status import HTTP_200_OK

from sds_client import SdsClient


def init_dev():
    try:
        client_id = os.environ["GPC_CLIENT_ID"]
        apigee_env = os.environ["APIGEE_ENVIRONMENT"]
    except KeyError as e:
        raise Exception(f"Environment variable is required: {e}")

    return {
        "client_id": client_id,
        "apigee_env": apigee_env
    }


app = FastAPI()


@app.get("/_status")
def status():
    return Response(status_code=HTTP_200_OK)


def sds_client() -> SdsClient:
    config = init_dev()
    return SdsClient(client_id=config["client_id"], env=config["apigee_env"])


@app.get("/AllergyIntolerance")
def allergyintollerance(_sds_client: SdsClient = Depends(sds_client)):
    # toASID = _sds_client.get_toASID(ods_code)
    # GPConnectUrl = _sds_client.get_URL(ods_code)
    return Response(status_code=HTTP_200_OK)


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=9000)
