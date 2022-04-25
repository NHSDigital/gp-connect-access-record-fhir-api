from mediation_service.mediation.handle_resolved_allergy import (
    RESOLVED_CLINICAL_STATUS,
    handle_resolved_allergies,
)


def test_resolved_clinical_status_added():
    """
    Test resolved clinical status added to allergies with allergies end extension
    """
    # Given
    resource = {
        "entry": [
            {
                "resource": {
                    "resourceType": "AllergyIntolerance",
                    "extension": [
                        {
                            "url": "https://fhir.nhs.uk/STU3/StructureDefinition/Extension-CareConnect-GPC-AllergyIntoleranceEnd-1"
                        }
                    ],
                },
            },
            {"resource": {"resourceType": "AllergyIntolerance"}},
        ]
    }

    # When
    actual = handle_resolved_allergies(resource)

    # Then
    assert actual["entry"][0]["resource"]["clinicalStatus"] == RESOLVED_CLINICAL_STATUS
    assert actual["entry"][1]["resource"].get("clinicalStatus") is None
