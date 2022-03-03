import os
from mediation_service.mediation.filter_bundle import BundleFilter
from fhirclient.models.allergyintolerance import AllergyIntolerance
from fhirclient.models.bundle import Bundle
import pytest
import json

dir_path = os.path.dirname(os.path.realpath(__file__))


@pytest.fixture
def example_allergies_response():
    file_path = os.path.join(dir_path, "resources/9690937286_allergies_response.json")
    with open(file=file_path, mode="r") as f:
        resource_str = f.read()
    return json.loads(resource_str)


@pytest.fixture
def example_bundle_with_warning_response():
    file_path = os.path.join(dir_path, "resources/example_bundle_with_warning.json")
    with open(file=file_path, mode="r") as f:
        resource_str = f.read()
    return json.loads(resource_str)


@pytest.fixture
def allergies_filterer():
    return BundleFilter(AllergyIntolerance)


def test_load_bundle(allergies_filterer: BundleFilter, example_allergies_response):
    bundle = allergies_filterer._load_bundle(example_allergies_response)

    assert isinstance(bundle, Bundle)


example_types = [("", "collection"), ("searchset", "searchset")]


@pytest.mark.parametrize("new_bundle_type, expected_type", example_types)
def test_filter_bundle_for_allergy_intolerance(
    new_bundle_type,
    expected_type,
    allergies_filterer: BundleFilter,
    example_allergies_response,
):
    response_bundle = allergies_filterer._load_bundle(example_allergies_response)

    filtered_bundle = allergies_filterer._filter_bundle(
        response_bundle, new_bundle_type
    )

    assert isinstance(filtered_bundle, Bundle)
    assert filtered_bundle.type == expected_type
    assert len(filtered_bundle.entry) == 1


example_responses = [
    (
        """{"fhir_comments":[" part 2 "],"resource":{"resourceType":"ProcedureRequest"}}""",
        {"resource": {"resourceType": "ProcedureRequest"}},
    ),
    (
        """{"resource":{"resourceType":"ProcedureRequest"}}""",
        {"resource": {"resourceType": "ProcedureRequest"}},
    ),
    (
        (
            """{"resourceType":"Bundle","id":"1234","type":"collection","""
            """"entry":[{"resource":{"resourceType":"Patient","id":"2","""
            """"meta":{"versionId":"1234","profile":["profile"],"fhir_comments":["nested comment"]}}}]}"""
        ),
        {
            "resourceType": "Bundle",
            "id": "1234",
            "type": "collection",
            "entry": [
                {
                    "resource": {
                        "resourceType": "Patient",
                        "id": "2",
                        "meta": {
                            "versionId": "1234",
                            "profile": ["profile"],
                        },
                    }
                }
            ],
        },
    ),
]

@pytest.mark.parametrize("input, expected", example_responses)
def test_clean_bundle(input, expected, allergies_filterer: BundleFilter):
    cleaned_dict = allergies_filterer._clean_response(input)

    assert cleaned_dict == expected


@pytest.mark.parametrize("new_bundle_type, expected_type", example_types)
def test_converting_warnings_to_operationoutcome(
    new_bundle_type,
    expected_type,
    allergies_filterer: BundleFilter,
    example_bundle_with_warning_response,
):
    response_bundle = allergies_filterer._load_bundle(example_bundle_with_warning_response)

    filtered_bundle = allergies_filterer._filter_bundle(
        response_bundle, new_bundle_type
    )

    response_as_json = json.loads(json.dumps(filtered_bundle.as_json()))

    print(response_as_json["entry"][1]["resource"]["resourceType"])
    assert response_as_json["resourceType"] == "Bundle"
    assert len(response_as_json["entry"]) == 2
    assert response_as_json["entry"][1]["resource"]["resourceType"] == "OperationOutcome"


