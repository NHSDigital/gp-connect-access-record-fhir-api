import os

import uvicorn
from fastapi import FastAPI
from starlette.responses import Response
from starlette.status import HTTP_200_OK

app = FastAPI()


@app.get("/_status")
def status():
    return Response(status_code=HTTP_200_OK)


@app.get("/AllergyIntolerance")
def allergyintollerance():
    return Response(status_code=HTTP_200_OK)


@app.get("/test")
def test():
    return len(os.environ.get("GPC_CLIENT_ID", "foo"))


@app.get("/test2")
def test():
    return len(os.environ.get("GPC_PRVIVATE_KEY_INT", "foo"))


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=9000)
