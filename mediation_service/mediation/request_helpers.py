import requests
from fastapi import HTTPException


def make_get_request(call_name: str, url, headers=None, params=None):
    res = requests.get(url, headers=headers, params=params)
    handle_error(res, call_name)
    return res


def make_post_request(
    call_name: str, url, headers=None, data=None, json=None, verify=True
):
    res = requests.post(url, headers=headers, data=data, json=json, verify=verify)
    handle_error(res, call_name)
    return res


def handle_error(response, call_name):
    if response.status_code != 200:
        detail = f"Request to {call_name} failed with message: {response.text}"
        raise HTTPException(status_code=response.status_code, detail=detail)
