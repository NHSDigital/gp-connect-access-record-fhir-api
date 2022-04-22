from jsonpath_rw import parse
import json

RESOLVED_CLINICAL_STATUS = {
    "coding": [
        {
            "system": "http://terminology.hl7.org/CodeSystem/allergyintolerance-clinical",
            "code": "resolved",
        }
    ]
}


def handle_resolved_allergies(converter_response: dict):
    """
    WORKAROUND while HAPI FHIR library bug is present
    Find allergyIntolerance resources with allergyEnd extension
    Add clinical status resolved to these resources
    """

    query = parse("`this`.entry[*].resource.resourceType")
    matches = query.find(converter_response)

    for match in matches:
        if match.value == "AllergyIntolerance":
            index = match.full_path.left.left.right.index
            allergy_resource = converter_response["entry"][index]["resource"]

            extensions = allergy_resource.get("extension", [])
            for extension in extensions:
                # Checking for STU3 url as fhir-convertor does not handle this url.
                if (
                    extension["url"]
                    == "https://fhir.nhs.uk/STU3/StructureDefinition/Extension-CareConnect-GPC-AllergyIntoleranceEnd-1"
                ):
                    resolved_clinical_status = RESOLVED_CLINICAL_STATUS

                    if not allergy_resource.get("clinicalStatus"):
                        allergy_resource["clinicalStatus"] = resolved_clinical_status
    return converter_response
