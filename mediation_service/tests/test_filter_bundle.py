import os
from mediation_service.mediation.filter_bundle import _load_bundle
from fhirclient.models.bundle import Bundle
import pytest

dir_path = os.path.dirname(os.path.realpath(__file__))


@pytest.fixture
def example_response():
    file_path = os.path.join(dir_path, "resources/9690937286_response.json")
    with open(file=file_path, mode="r") as f:
        resource_str = f.read()
    return resource_str


def test_load_bundle(example_response):
    bundle = _load_bundle(example_response)

    assert isinstance(bundle, Bundle)
