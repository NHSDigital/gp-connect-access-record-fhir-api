import os
from mediation_service.mediation.filter_bundle import BundleFilter
from fhirclient.models.allergyintolerance import AllergyIntolerance
from fhirclient.models.bundle import Bundle
import pytest

dir_path = os.path.dirname(os.path.realpath(__file__))


@pytest.fixture
def example_allergies_response():
    file_path = os.path.join(dir_path, "resources/9690937286_allergies_response.json")
    with open(file=file_path, mode="r") as f:
        resource_str = f.read()
    return resource_str


@pytest.fixture
def allergies_filterer():
    return BundleFilter(AllergyIntolerance)


def test_load_bundle(allergies_filterer: BundleFilter, example_allergies_response):
    bundle = allergies_filterer._load_bundle(example_allergies_response)

    assert isinstance(bundle, Bundle)


def test_filter_bundle_for_allergy_intolerance(
    allergies_filterer: BundleFilter, example_allergies_response
):
    response_bundle = allergies_filterer._load_bundle(example_allergies_response)

    filtered_bundle = allergies_filterer._filter_bundle(response_bundle)

    assert isinstance(filtered_bundle, Bundle)
    assert filtered_bundle.type == "collection"
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
