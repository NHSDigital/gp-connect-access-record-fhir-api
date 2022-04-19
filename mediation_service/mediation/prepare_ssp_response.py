from copy import deepcopy
from datetime import datetime, timezone
from functools import reduce

from fhirclient.models.codeableconcept import CodeableConcept
from fhirclient.models.coding import Coding
from fhirclient.models.extension import Extension
from fhirclient.models.fhirdate import FHIRDate
from fhirclient.models.meta import Meta
from fhirclient.models.operationoutcome import OperationOutcome
from fhirclient.models.operationoutcome import OperationOutcomeIssue
from jsonpath_rw import parse


def prepare_ssp_response(ssp_response: dict) -> dict:
    __transform_allergy_local_references(ssp_response)
    operationoutcome = __filter_warnings_to_operationoutcome(ssp_response)
    # take list first.
    # extract resolved allergies
    resolved_allergy_intolerance_entries = _extract_resolved_allergies(ssp_response)
    # remove all things that are not allergy intolerance
    # add the resolved resources to entry.
    _filter_non_allergy_intolerance(ssp_response)
    __remove_fhir_comment(ssp_response)

    if resolved_allergy_intolerance_entries:
        ssp_response["entry"].extend(resolved_allergy_intolerance_entries)

    if operationoutcome:
        operationoutcome_object = {"resource": operationoutcome.as_json()}
        ssp_response["entry"].append(operationoutcome_object)

    ssp_response["type"] = "searchset"
    return ssp_response


def __filter_warnings_to_operationoutcome(ssp_response: dict) -> OperationOutcome:
    query = parse("`this`.entry[*].resource.resourceType")
    matches = query.find(ssp_response)

    operation_outcome_list = []
    for match in matches:
        if match.value == "List":
            index = match.full_path.left.left.right.index
            list = ssp_response["entry"][index]["resource"]

            # check list title to only select list with allergy intolerance warnings.
            list_title = list.get("title")
            if list_title == "Allergies and adverse reactions":

                for extension in list["extension"]:
                    if (
                        extension["url"]
                        == "https://fhir.nhs.uk/STU3/StructureDefinition/Extension-CareConnect-GPC"
                        "-ListWarningCode-1"
                    ):
                        operation_outcome_list.append(
                            __build_operationoutcome_issue(extension)
                        )

    if operation_outcome_list:
        return __build_operationoutcome(operation_outcome_list)


def __build_operationoutcome_issue(extension: Extension) -> OperationOutcomeIssue:
    op_outcome_issue = OperationOutcomeIssue()
    codeable_concept = CodeableConcept()
    coding_list = []
    coding = Coding()

    op_outcome_issue.code = "processing"
    op_outcome_issue.severity = "warning"

    codeable_concept.system = "https://fhir.nhs.uk/CodeSystem/Spine-ErrorOrWarningCode"

    if extension["valueCode"] == "confidential-items":
        op_outcome_issue.diagnostics = (
            "Items excluded due to confidentiality and/or patient preferences."
        )
        coding.code = "CONFIDENTIAL_ITEMS"
        coding_list.append(coding)
        codeable_concept.coding = coding_list
        codeable_concept.display = "Confidential Items"
    if extension["valueCode"] == "data-in-transit":
        op_outcome_issue.diagnostics = (
            "Patient record transfer from previous GP practice not yet complete; any "
            "information recorded before dd-mmm-yyyy has been excluded "
        )
        coding.code = "DATA_IN_TRANSIT"
        coding_list.append(coding)
        codeable_concept.coding = coding_list
        codeable_concept.display = "Data in Transit"
    if extension["valueCode"] == "data-awaiting-filing":
        op_outcome_issue.diagnostics = (
            "Patient data may be incomplete as there is data supplied by a third party "
            "awaiting review before becoming available. "
        )
        coding.code = "DATA_AWAITING_FILING"
        coding_list.append(coding)
        codeable_concept.coding = coding_list
        codeable_concept.display = "Data Awaiting Filing"

    op_outcome_issue.details = codeable_concept

    location_list = ["/entry"]
    op_outcome_issue.location = location_list

    return op_outcome_issue


def __build_operationoutcome(operation_outcome_list) -> OperationOutcome:
    operationoutcome = OperationOutcome()
    meta = Meta()
    fhir_date = FHIRDate()

    # current UTC datetime
    now_utc = datetime.now(timezone.utc)
    now_utc_isoformat = now_utc.astimezone(timezone.utc)
    fhir_date.date = now_utc_isoformat

    meta.lastUpdated = fhir_date
    operationoutcome.meta = meta
    operationoutcome.issue = operation_outcome_list

    return operationoutcome


def __transform_patient(ssp_response: dict) -> dict:
    patient_dict_to_return = {}
    query = parse("`this`.entry[*].resource.resourceType")
    matches = query.find(ssp_response)
    for match in matches:
        if match.value == "Patient":
            index = match.full_path.left.left.right.index
            patient = ssp_response["entry"][index]
            query = parse("resource.identifier")
            matches = query.find(patient)
            for identifier in matches:
                for item in identifier.value:
                    if (
                        item.get("system").lower()
                        == "https://fhir.nhs.uk/Id/nhs-number".lower()
                    ):
                        nhs_number = item.get("value")
                        patient_dict_to_return[
                            patient["resource"].get("id")
                        ] = f"AllergyIntolerance?patient:identifier=https://fhir.nhs.uk/Id/nhs-number|{nhs_number}"

    return patient_dict_to_return


def __transform_allergy_local_references(ssp_response: dict):
    patient_list = __transform_patient(ssp_response)

    query = parse("`this`.entry[*].resource.resourceType")
    matches = query.find(ssp_response)

    for match in matches:
        if match.value == "AllergyIntolerance":
            index = match.full_path.left.left.right.index
            allergy = ssp_response["entry"][index]

            if allergy.get("resource").get("patient"):
                patient_ref = allergy.get("resource").get("patient").get("reference")
                patient_id = patient_ref.split("/")
                ssp_response["entry"][index]["resource"]["patient"][
                    "reference"
                ] = patient_list.get(patient_id[1], patient_ref)

def _extract_resolved_allergies(ssp_response: dict):
    """Extract resolved allergy intolernace resources from list"""
    query = parse("`this`.entry[*].resource.resourceType")
    matches = query.find(ssp_response)

    resolved_allergy_intolerance_entries = []

    for match in matches:
        if match.value == "List":
            index = match.full_path.left.left.right.index
            list_resource = ssp_response["entry"][index]["resource"]
            # check list title
            list_title = list_resource.get("title")
            if list_title == "Ended allergies":
                contained = list_resource.get("contained")
                for resource in contained:
                    resource_entry = {"resource": resource}
                    resolved_allergy_intolerance_entries.append(resource_entry)

    return resolved_allergy_intolerance_entries



def _filter_non_allergy_intolerance(ssp_response: dict):
    """
    Select active and resolved allergy intolerance resources
    Extract resolved allergy intolerance resources from list
    """
    # handle bundle with no entries
    if not ssp_response.get("entry"):
        return

    query = parse("`this`.entry[*].resource.resourceType")
    matches = query.find(ssp_response)

    entry_to_keep = []

    for match in matches:
        allergy_intolerances = __allergy_intolerances_to_keep(match, ssp_response)
        #ended_allergy_list = __ended_allergy_list_to_keep(match, ssp_response)
        entry_to_keep.extend(allergy_intolerances)

    copy_entries = deepcopy(ssp_response["entry"])

    for entry in copy_entries:
        if entry not in entry_to_keep:
            ssp_response["entry"].remove(entry)

def __allergy_intolerances_to_keep(match, ssp_response):
    allergy_to_keep = []
    if match.value == "AllergyIntolerance":
        index = match.full_path.left.left.right.index
        allergy_to_keep.append(ssp_response["entry"][index])
    return allergy_to_keep

def __ended_allergy_list_to_keep(match, ssp_response):
    list_to_retain = []
    if match.value == "List":
        index = match.full_path.left.left.right.index
        list_resource = ssp_response["entry"][index]["resource"]
        # check list title
        list_title = list_resource.get("title")
        if list_title == "Ended allergies":
            list_to_retain.append(ssp_response["entry"][index])
    return list_to_retain

def __remove_fhir_comment(ssp_response: dict):
    query = parse("`this`..fhir_comments")
    matches = query.find(ssp_response)

    for match in matches:
        path = str(match.full_path)
        segments = path.split(".")[0:-1]  # All path segments except last one

        parent_obj_containing_comment = reduce(
            lambda o, p: o[p], segments, ssp_response
        )
        parent_obj_containing_comment.pop("fhir_comments")
