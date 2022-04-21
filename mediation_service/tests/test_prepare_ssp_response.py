from copy import deepcopy
from mediation_service.mediation.prepare_ssp_response import (
    ENDED_ALLERGIES_LIST_CODE,
    prepare_ssp_response,
    _extract_resolved_allergies,
    _select_lists_with_code,
)
import re


def test_list_selection():
    fhir_res = {
        "entry": [
            {"resource": {"resourceType": "Bar"}},
            {
                "resource": {
                    "resourceType": "List",
                    "title": "Ended allergies",
                    "code": {
                        "coding": [
                            {
                                "system": "http://snomed.info/sct",
                                "code": "1103671000000101",
                                "display": "Ended allergies",
                            }
                        ]
                    },
                }
            },
            {
                "resource": {
                    "resourceType": "List",
                    "title": "Allergies and adverse reactions",
                    "code": {
                        "coding": [
                            {
                                "system": "http://snomed.info/sct",
                                "code": "886921000000105",
                                "display": "Allergies and adverse reactions",
                            }
                        ]
                    },
                }
            },
        ]
    }

    expected = [
        {
            "resourceType": "List",
            "title": "Ended allergies",
            "code": {
                "coding": [
                    {
                        "system": "http://snomed.info/sct",
                        "code": "1103671000000101",
                        "display": "Ended allergies",
                    }
                ]
            },
        }
    ]

    # when
    selected_list = _select_lists_with_code(ENDED_ALLERGIES_LIST_CODE, fhir_res)

    # then
    assert selected_list == expected


def test_remove_comments():
    # Given
    fhir_res = {
        "fhir_res": {
            "fhir_comments": {"k": "v"},
            "other": "str",
            "nested": {"k": "v", "fhir_comments": "foo"},
        }
    }

    expected_res = {
        "type": "searchset",
        "fhir_res": {"other": "str", "nested": {"k": "v"}},
    }

    # When
    act = prepare_ssp_response(fhir_res)

    # Then
    assert expected_res == act


def test_remove_non_allergy_intolerance():
    # Given
    fhir_res = {
        "entry": [
            {"resource": {"resourceType": "Foo"}},
            {"resource": {"resourceType": "AllergyIntolerance"}},
            {"resource": {"resourceType": "Bar"}},
        ]
    }

    expected_res = {
        "type": "searchset",
        "entry": [
            {"resource": {"resourceType": "AllergyIntolerance"}},
        ],
    }

    # When
    act = prepare_ssp_response(fhir_res)

    # Then
    assert expected_res == act


def test_return_active_and_resolved_allergy():
    # Given
    fhir_res = {
        "entry": [
            {"resource": {"resourceType": "Foo"}},
            {"resource": {"resourceType": "Bar"}},
            {"resource": {"resourceType": "AllergyIntolerance"}},
            {"resource": {"resourceType": "AllergyIntolerance"}},
            {
                "resource": {
                    "resourceType": "List",
                    "title": "Ended allergies",
                    "code": {
                        "coding": [
                            {
                                "system": "http://snomed.info/sct",
                                "code": "1103671000000101",
                                "display": "Ended allergies",
                            }
                        ]
                    },
                    "contained": [
                        {
                            "resourceType": "AllergyIntolerance",
                            "id": "1",
                            "extension": [
                                {
                                    "url": "https://fhir.nhs.uk/STU3/StructureDefinition/Extension-CareConnect-GPC-AllergyIntoleranceEnd-1"
                                }
                            ],
                            "clinicalStatus": "resolved",
                        },
                        {
                            "resourceType": "AllergyIntolerance",
                            "id": "2",
                            "extension": [
                                {
                                    "url": "https://fhir.nhs.uk/STU3/StructureDefinition/Extension-CareConnect-GPC-AllergyIntoleranceEnd-1"
                                }
                            ],
                            "clinicalStatus": "resolved",
                        },
                    ],
                }
            },
            {"resource": {"resourceType": "Baz"}},
        ]
    }

    expected_res = {
        "type": "searchset",
        "entry": [
            {"resource": {"resourceType": "AllergyIntolerance"}},
            {"resource": {"resourceType": "AllergyIntolerance"}},
            {
                "resource": {
                    "resourceType": "AllergyIntolerance",
                    "id": "1",
                    "extension": [
                        {
                            "url": "https://fhir.nhs.uk/STU3/StructureDefinition/Extension-CareConnect-GPC-AllergyIntoleranceEnd-1"
                        }
                    ],
                    "clinicalStatus": "resolved",
                },
            },
            {
                "resource": {
                    "resourceType": "AllergyIntolerance",
                    "id": "2",
                    "extension": [
                        {
                            "url": "https://fhir.nhs.uk/STU3/StructureDefinition/Extension-CareConnect-GPC-AllergyIntoleranceEnd-1"
                        }
                    ],
                    "clinicalStatus": "resolved",
                }
            },
        ],
    }

    # When
    actual = prepare_ssp_response(fhir_res)

    assert expected_res == actual


def test_extract_resolved_allergies():
    # Given
    fhir_res = {
        "entry": [
            {"resource": {"resourceType": "Foo"}},
            {"resource": {"resourceType": "AllergyIntolerance"}},
            {
                "resource": {
                    "resourceType": "List",
                    "title": "Ended allergies",
                    "code": {
                        "coding": [
                            {
                                "system": "http://snomed.info/sct",
                                "code": "1103671000000101",
                                "display": "Ended allergies",
                            }
                        ]
                    },
                    "contained": [
                        {
                            "resourceType": "AllergyIntolerance",
                            "id": "1",
                            "extension": [
                                {
                                    "url": "https://fhir.nhs.uk/STU3/StructureDefinition/Extension-CareConnect-GPC-AllergyIntoleranceEnd-1"
                                }
                            ],
                            "clinicalStatus": "resolved",
                        },
                        {
                            "resourceType": "AllergyIntolerance",
                            "id": "2",
                            "extension": [
                                {
                                    "url": "https://fhir.nhs.uk/STU3/StructureDefinition/Extension-CareConnect-GPC-AllergyIntoleranceEnd-1"
                                }
                            ],
                            "clinicalStatus": "resolved",
                        },
                    ],
                }
            },
            {"resource": {"resourceType": "Baz"}},
        ]
    }

    expected = [
        {
            "resource": {
                "resourceType": "AllergyIntolerance",
                "id": "1",
                "extension": [
                    {
                        "url": "https://fhir.nhs.uk/STU3/StructureDefinition/Extension-CareConnect-GPC-AllergyIntoleranceEnd-1"
                    }
                ],
                "clinicalStatus": "resolved",
            },
        },
        {
            "resource": {
                "resourceType": "AllergyIntolerance",
                "id": "2",
                "extension": [
                    {
                        "url": "https://fhir.nhs.uk/STU3/StructureDefinition/Extension-CareConnect-GPC-AllergyIntoleranceEnd-1"
                    }
                ],
                "clinicalStatus": "resolved",
            },
        },
    ]

    # When
    actual = _extract_resolved_allergies(fhir_res)

    # Then
    assert actual == expected


def test_extract_resolved_allergies_when_none():
    fhir_res = {
        "entry": [
            {"resource": {"resourceType": "Foo"}},
            {"resource": {"resourceType": "AllergyIntolerance"}},
            {"resource": {"resourceType": "Baz"}},
        ]
    }

    # When
    actual = _extract_resolved_allergies(fhir_res)

    # Then
    assert actual == []


def test_transform_references_for_patient():

    # Give AllergyIntolerance has a local reference to Patient with id 2
    nhs_num = "9690937286"
    patient = {
        "resource": {
            "resourceType": "Patient",
            "id": "2",
            "identifier": [
                {"system": "https://fhir.nhs.uk/Id/nhs-number", "value": nhs_num}
            ],
        }
    }

    allergy_intolerance = {
        "resource": {
            "resourceType": "AllergyIntolerance",
            "patient": {"reference": "Patient/2"},
        }
    }

    fhir_res = {"entry": [patient, allergy_intolerance]}

    modified_allergy = deepcopy(allergy_intolerance)
    modified_allergy["resource"]["patient"][
        "reference"
    ] = f"AllergyIntolerance?patient:identifier=https://fhir.nhs.uk/Id/nhs-number|{nhs_num}"
    expected_resource = {"type": "searchset", "entry": [modified_allergy]}

    # When
    actual_resource = prepare_ssp_response(fhir_res)

    # actual_resource e' uam string
    # Then
    assert expected_resource == actual_resource


def test_transform_references_for_patient_if_exists():
    # Given the local reference doesn't match with any resource
    nhs_num = "9690937286"
    patient = {
        "resource": {
            "resourceType": "Patient",
            "id": "3",  # The id does NOT match with the reference
            "identifier": [
                {"system": "https://fhir.nhs.uk/Id/nhs-number", "value": nhs_num}
            ],
        }
    }

    allergy_intolerance = {
        "resource": {
            "resourceType": "AllergyIntolerance",
            "patient": {"reference": "Patient/2"},
        }
    }

    fhir_res = {"entry": [patient, allergy_intolerance]}

    modified_allergy = deepcopy(allergy_intolerance)
    modified_allergy["resource"]["patient"][
        "reference"
    ] = "Patient/2"  # The reference is the same i.e. no transformation
    expected_resource = {"type": "searchset", "entry": [modified_allergy]}

    # When
    actual_resource = prepare_ssp_response(fhir_res)

    # Then
    assert expected_resource == actual_resource


def test_change_bundle_type():
    fhir_res = {"type": "some-type"}
    expected_resource = {"type": "searchset"}

    # When
    actual_resource = prepare_ssp_response(fhir_res)

    # Then
    assert expected_resource == actual_resource


def test_warning_filter():
    # Given
    fhir_res = {
        "entry": [
            {"resource": {"resourceType": "AllergyIntolerance"}},
            {
                "resource": {
                    "resourceType": "List",
                    "title": "Allergies and adverse reactions",
                    "code": {
                        "coding": [
                            {
                                "system": "http://snomed.info/sct",
                                "code": "886921000000105",
                                "display": "Allergies and adverse reactions",
                            }
                        ]
                    },
                    "extension": [
                        {
                            "url": "https://fhir.nhs.uk/STU3/StructureDefinition/Extension-CareConnect-GPC-ListWarningCode-1",
                            "valueCode": "data-in-transit",
                        },
                        {
                            "url": "https://fhir.nhs.uk/STU3/StructureDefinition/Extension-CareConnect-GPC-ListWarningCode-1",
                            "valueCode": "confidential-items",
                        },
                    ],
                }
            },
        ]
    }

    # When
    result = prepare_ssp_response(fhir_res)

    # Then
    assert result["entry"][0]["resource"]["resourceType"] == "AllergyIntolerance"
    assert result["entry"][1]["resource"]["resourceType"] == "OperationOutcome"
    assert len(result["entry"][1]["resource"]["issue"]) == 2

    # ensure date matches fhir regex.
    operation_outcome_last_updated = result["entry"][1]["resource"]["meta"][
        "lastUpdated"
    ]
    pattern = re.compile(
        (
            r"([0-9]([0-9]([0-9][1-9]|[1-9]0)|[1-9]00)|[1-9]000)-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]"
            r"|3[0-1])T([01][0-9]|2[0-3]):[0-5][0-9]:([0-5][0-9]|60)(\.[0-9]+)?(Z|(\+|-)((0[0-9]"
            r"|1[0-3]):[0-5][0-9]|14:00))"
        )
    )
    pattern.fullmatch(operation_outcome_last_updated)
