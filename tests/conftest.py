# flake8: noqa
import pytest
import os


@pytest.fixture(scope='session')
def apigee_token():
    """
        Reads the apigee token from an environment variable

    """
    return os.environ['TOKEN']
