import uvicorn
from fastapi import FastAPI
from starlette.responses import Response
from starlette.status import HTTP_200_OK

app = FastAPI()


@app.get("/_status")
def status():
    return Response(status_code=HTTP_200_OK)


@app.get("/allergyintollerance")
def allergyintollerance():
    return Response(status_code=HTTP_200_OK)


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=9000)
