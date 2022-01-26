# flake8: noqa
import pytest
import os


@pytest.fixture(scope='session')
def get_token():
    """
        reads the token from an environment variable

    """
    return os.environ['TOKEN']
