# flake8: noqa

import pytest

from .configuration.cmd_options import options, create_cmd_options


def pytest_addoption(parser):
    for option in options:
        parser.addoption(
            option["name"],
            required=option.get("required", False),
            action=option.get("action", "store"),
            help=option.get("help", ""),
            default=option.get("default")
        )


@pytest.fixture(scope='session', autouse=True)
def cmd_options(request) -> dict:
    return create_cmd_options(request.config.getoption)


@pytest.fixture(scope='session')
def access_token(cmd_options: dict):
    return cmd_options['--access-token']


def get_proxy_base_path(proxy_base_path: str, pr_no: str):
    if pr_no:
        return f"{proxy_base_path}-pr-{pr_no}"
    else:
        return f"{proxy_base_path}"


@pytest.fixture(scope='session')
def proxy_url(cmd_options: dict) -> str:
    env = cmd_options["--apigee-environment"]

    if "local" in env:
        return "http://localhost:9000"
    else:
        pr_no = cmd_options["--pr-no"]
        base_path = get_proxy_base_path(cmd_options["--proxy-base-path"], pr_no)

        return f"https://{env}.api.service.nhs.uk/{base_path}"
