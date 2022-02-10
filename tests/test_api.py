import pytest
import requests
import json
from assertpy import assert_that


class TestAllergyIntolerance:
    valid_nhs_number = "9690937286"

    @pytest.fixture()
    def url(self, proxy_url: str) -> str:
        allergy_endpoint = "AllergyIntolerance"

        return f"{proxy_url}/{allergy_endpoint}"

    @pytest.mark.mediation
    @pytest.mark.debug
    def test_happy_path(self, access_token, url):
        # Given
        expected_status_code = 200
        # When
        response = requests.get(
            url=url,
            headers={"Authorization": f"Bearer {access_token}"},
            params={"patient": f"https://fhir.nhs.uk/Id/{self.valid_nhs_number}"},
        )
        print(response.text)
        expected_resource_type = self.__get_bundle(response.json())
        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(expected_resource_type).is_equal_to("Bundle")

    @pytest.mark.mediation
    @pytest.mark.debug
    def test_nhs_number_not_matching(self, access_token, url):
        # Given
        expected_status_code = 403
        # When
        response = requests.get(
            url=url,
            headers={"Authorization": f"Bearer {access_token}"},
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
    def test_invalid_patient_query_parameter(self, access_token, url, patient):
        # Given
        expected_status_code = 400
        # When
        response = requests.get(
            url=url,
            headers={"Authorization": f"Bearer {access_token}"},
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

    @staticmethod
    def __get_bundle(resource: dict) -> str:
        return resource["resourceType"]
