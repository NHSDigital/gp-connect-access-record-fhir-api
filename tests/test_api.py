import requests
import pytest
from assertpy import assert_that


class TestAllergyIntolerance:
    @pytest.fixture()
    def url(self) -> str:
        return (
            "https://int.api.service.nhs.uk/gp-connect-access-record/AllergyIntolerance"
        )

    def test_happy_path(self, apigee_token, url):
        # Given
        token = apigee_token
        expected_status_code = 200
        # When
        response = requests.get(url=url, headers={"Authorization": f"Bearer {token}"})
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
