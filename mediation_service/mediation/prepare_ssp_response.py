from jsonpath_rw import parse
import re
from functools import reduce

def prepare_ssp_response(ssp_response: dict) -> dict:
    #__transform_local_references(ssp_response)
    __filter_non_allergy_intolerance(ssp_response)
    __remove_fhir_comment(ssp_response)

    ssp_response['type'] = 'searchset'

    return ssp_response

def __transform_patient(ref, ssp_response: dict):
    if not isinstance(ref, str) or 'Patient' not in ref:
        return ""

    id_matches = re.findall(r'^Patient/(\d)', ref)
    if id_matches:
        patient_id = id_matches[0]
        query = parse('`this`.entry[*].resource.resourceType')
        matches = query.find(ssp_response)
        for match in matches:
            if match.value == 'Patient':
                index = match.full_path.left.left.right.index
                patient = ssp_response['entry'][index]
                if str(patient['resource'].get('id')) != patient_id:
                    continue  # This is the correct patient only if it's 'id' matches with the one in ref

                query = parse('resource.identifier')
                matches = query.find(patient)
                for identifier in matches:
                    if identifier.value.get('system').lower() == 'https://fhir.nhs.uk/Id/nhs-number'.lower():
                        nhs_number = identifier.value.get('value')
                        return f"AllergyIntolerance?patient:identifier=https://fhir.nhs.uk/Id/nhs-number|{nhs_number}"

        return ""


def __transform_local_references(ssp_response: dict):
    query = parse('`this`.entry[*].resource.resourceType')
    matches = query.find(ssp_response)

    for match in matches:
        if match.value == 'AllergyIntolerance':
            index = match.full_path.left.left.right.index
            allergy = ssp_response['entry'][index]
            query = parse('resource.patient.reference')
            matches = query.find(allergy)
            for ref in matches:
                abs_ref = __transform_patient(ref.value, ssp_response)
                if abs_ref:
                    allergy['resource']['patient']['reference'] = abs_ref

def __filter_non_allergy_intolerance(ssp_response: dict):
    query = parse('`this`.entry[*].resource.resourceType')
    matches = query.find(ssp_response)

    to_remove = []
    for match in matches:
        if match.value != 'AllergyIntolerance':
            index = match.full_path.left.left.right.index
            to_remove.append(ssp_response['entry'][index])

    for item in to_remove:
        ssp_response['entry'].remove(item)

def __remove_fhir_comment(ssp_response: dict):
    query = parse('`this`..fhir_comments')
    matches = query.find(ssp_response)

    for match in matches:
        path = str(match.full_path)
        segments = path.split('.')[0:-1]  # All path segments except last one

        parent_obj_containing_comment = reduce(lambda o, p: o[p], segments, ssp_response)
        parent_obj_containing_comment.pop('fhir_comments')