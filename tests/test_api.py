import os

import pytest
import requests
from assertpy import assert_that


class TestAllergyIntolerance:
    valid_nhs_number = "9690937286"

    @pytest.fixture()
    def url(self, apigee_token) -> str:
        environment = os.environ["APIGEE_ENVIRONMENT"]
        allergy_endpoint = "AllergyIntolerance"
        if not apigee_token:
            return f"http://localhost:9000/{allergy_endpoint}"
        else:
            return f"https://{environment}.api.service.nhs.uk/gp-connect-access-record/{allergy_endpoint}"

    @pytest.mark.mediation
    @pytest.mark.debug
    def test_happy_path(self, apigee_token, url):
        # Given
        url = "https://internal-dev.api.service.nhs.uk/gp-connect-access-record-pr-40/test"
        token = apigee_token
        expected_status_code = 200
        # When
        response = requests.get(
            url=url,
            headers={"Authorization": f"Bearer {token}"},
            params={"patient": f"https://fhir.nhs.uk/Id/{self.valid_nhs_number}"},
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)

    @pytest.mark.mediation
    def test_nhs_number_not_matching(self, apigee_token, url):
        # Given
        token = apigee_token
        expected_status_code = 403
        # When
        response = requests.get(
            url=url,
            headers={"Authorization": f"Bearer {token}"},
            params={"patient": "https://fhir.nhs.uk/Id/0000000000"},
        )
        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)

    @pytest.mark.parametrize(
        "patient",
        [
            "https://fhir.nhs.uk/Id/9661034524/9912003070",
            "https://fhir.nhs.uk/Id/9912003",
            "https://example.com/9661034524",
            "",
        ],
    )
    def test_invalid_patient_query_parameter(self, apigee_token, url, patient):
        # Given
        token = apigee_token
        expected_status_code = 400
        # When
        response = requests.get(
            url=url,
            headers={"Authorization": f"Bearer {token}"},
            params={"patient": f"{patient}"},
        )
        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)

    def test_invalid_token(self, url):
        # Given
        token = "invalid"
        expected_status_code = 401
        # When
        response = requests.get(url=url, headers={"Authorization": f"Bearer {token}"})
        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
