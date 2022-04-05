from mediation_service.mediation.pds_client import PdsClient
from mediation_service.mediation.sds_client import SdsClient
from mediation_service.mediation.ssp_client import SspClient
from mediation_service.mediation.fhir_converter_client import FhirConverter
from unittest.mock import Mock
from fastapi import HTTPException

from unittest.mock import patch
import pytest


@pytest.fixture
def mock_404_response():
    return Mock(status_code=404, text="an error occured")


@patch("requests.get")
def test_pds_client_raises_exception(mock_404_request: Mock, mock_404_response):
    mock_404_request.return_value = mock_404_response
    client = PdsClient(url=Mock(), env=Mock())

    with pytest.raises(HTTPException) as exception:
        client.get_ods_for_nhs_number("99999999999", "dummy token")

    assert exception.type == HTTPException
    assert exception.value.status_code == 404
    assert (
        exception.value.detail == "Request to PDS failed with message: an error occured"
    )


@patch("requests.get")
def test_sds_get_to_asid_raises_exception(mock_404_request: Mock, mock_404_response):
    mock_404_request.return_value = mock_404_response
    client = SdsClient("dummy id", "dummy url")

    with pytest.raises(HTTPException) as exception:
        client.get_toASID("dummy ods")

    assert exception.type == HTTPException
    assert exception.value.status_code == 404
    assert (
        exception.value.detail
        == "Request to SDS get_toASID failed with message: an error occured"
    )


@patch("requests.get")
def test_sds_get_url_raises_exception(mock_404_request: Mock, mock_404_response):
    mock_404_request.return_value = mock_404_response
    client = SdsClient("dummy id", "dummy url")

    with pytest.raises(HTTPException) as exception:
        client.get_URL("dummy ods")

    assert exception.type == HTTPException
    assert exception.value.status_code == 404
    assert (
        exception.value.detail
        == "Request to SDS get_URL failed with message: an error occured"
    )


@patch("requests.post")
def test_ssp_get_bundle_raises_exception(mock_404_request: Mock, mock_404_response):
    mock_404_request.return_value = mock_404_response
    client = SspClient(url="dummy url")

    with pytest.raises(HTTPException) as exception:
        ods_dict = {"to_ASID": "dummy", "GPConnect_URL": "dummy"}
        client.get_allergy_intolerance_bundle(ods_dict)

    assert exception.type == HTTPException
    assert exception.value.status_code == 404
    assert (
        exception.value.detail
        == "Request to SSP get allergy intolerance bundle failed with message: an error occured"
    )


@patch("requests.post")
def test_fhir_convertor_raises_exception(mock_404_request: Mock, mock_404_response):
    mock_404_request.return_value = mock_404_response
    client = FhirConverter(url="dummy url", env=Mock())

    with pytest.raises(HTTPException) as exception:
        bundle = {"resource": {"resourceType": "Bundle"}}
        client.convert(bundle=bundle, access_token="dummy")

    assert exception.type == HTTPException
    assert exception.value.status_code == 404
    assert (
        exception.value.detail
        == "Request to Fhir Convertor failed with message: an error occured"
    )
