import json

import pytest
import requests
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
        expected_content = {
            "to_ASID": "200000001329",
            "GPConnect_URL": "https://gpconnect-win1.itblab.nic.cfh.nhs.uk/B82617/STU3/1/gpconnect/structured/fhir",
            "resourceType": "Bundle",
        }

        # When
        response = requests.get(
            url=url,
            headers={"Authorization": f"Bearer {access_token}"},
            params={"patient": f"https://fhir.nhs.uk/Id/{self.valid_nhs_number}"},
        )

        response_dict = response.json()
        bundleObj = json.loads(response_dict["response"])

        response_resourceType = bundleObj["resourceType"]
        bundle_type = bundleObj["type"]
        bundle_url = bundleObj["meta"]["profile"][0]
        response_number_of_entries = len(bundleObj["entry"])

        resourceType_operationoutcome = bundleObj["entry"][30]["resource"][
            "resourceType"
        ]

        resourceType_allergy = bundleObj["entry"][0]["resource"]["resourceType"]
        patient_reference = bundleObj["entry"][2]["resource"]["patient"]["reference"]
        allergy_url = bundleObj["entry"][2]["resource"]["meta"]["profile"][0]

        # One of two resolved allergies
        resolved_allergy = bundleObj["entry"][28]["resource"]
        resourceType_resolved_allergy = resolved_allergy["resourceType"]
        resolved_allergy_clinical_status = resolved_allergy["clinicalStatus"]["coding"][0]["code"]

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(expected_content["resourceType"]).is_equal_to(response_resourceType)
        assert_that("searchset").is_equal_to(bundle_type)
        assert_that(
            "https://fhir.hl7.org.uk/StructureDefinition/UKCore-Bundle"
        ).is_equal_to(bundle_url)
        assert_that(31).is_equal_to(response_number_of_entries)

        assert_that("OperationOutcome").is_equal_to(resourceType_operationoutcome)

        assert_that("AllergyIntolerance").is_equal_to(resourceType_allergy)
        assert_that(
            "AllergyIntolerance?patient:identifier=https://fhir.nhs.uk/Id/nhs-number|9690937332"
        ).is_equal_to(patient_reference)
        assert_that(
            "https://fhir.hl7.org.uk/StructureDefinition/UKCore-AllergyIntolerance"
        ).is_equal_to(allergy_url)

        assert_that("AllergyIntolerance").is_equal_to(resourceType_resolved_allergy)
        assert_that("resolved").is_equal_to(resolved_allergy_clinical_status)

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
