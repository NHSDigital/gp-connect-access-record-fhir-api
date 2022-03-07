from copy import deepcopy

from mediation_service.mediation.prepare_ssp_response import prepare_ssp_response


def test_remove_comments():
    # Given
    fhir_res = {'fhir_res': {'fhir_comments': {'k': 'v'},
                             'other': 'str',
                             'nested': {'k': 'v', 'fhir_comments': 'foo'}}}

    expected_res = {'type': 'searchset', 'fhir_res': {
        'other': 'str',
        'nested': {'k': 'v'}}}

    # When
    act = prepare_ssp_response(fhir_res)

    # Then
    assert expected_res == act


def test_remove_non_allergy_intolerance():
    # Given
    fhir_res = {'entry': [
        {'resource': {'resourceType': 'Foo'}},
        {'resource': {'resourceType': 'AllergyIntolerance'}},
        {'resource': {'resourceType': 'Bar'}},
    ]}

    expected_res = {'type': 'searchset', 'entry': [
        {'resource': {'resourceType': 'AllergyIntolerance'}},
    ]}

    # When
    act = prepare_ssp_response(fhir_res)

    # Then
    assert expected_res == act


def test_transform_references_for_patient():
    # Give AllergyIntolerance has a local reference to Patient with id 2
    nhs_num = '9690937286'
    patient = {'resource': {'resourceType': 'Patient', 'id': 2,
                            'identifier': {'system': 'https://fhir.nhs.uk/Id/nhs-number', 'value': nhs_num}}}

    allergy_intolerance = {'resource': {'resourceType': 'AllergyIntolerance', 'patient': {'reference': 'Patient/2'}}}

    fhir_res = {'entry': [patient, allergy_intolerance]}

    modified_allergy = deepcopy(allergy_intolerance)
    modified_allergy['resource']['patient']['reference'] = f"http/p/{nhs_num}"
    expected_resource = {'type': 'searchset', 'entry': [modified_allergy]}

    # When
    actual_resource = prepare_ssp_response(fhir_res)

    # Then
    assert expected_resource == actual_resource


def test_transform_references_for_patient_if_exists():
    # Given the local reference doesn't match with any resource
    nhs_num = '9690937286'
    patient = {'resource': {'resourceType': 'Patient', 'id': 3,  # The id does NOT match with the reference
                            'identifier': {'system': 'https://fhir.nhs.uk/Id/nhs-number', 'value': nhs_num}}}

    allergy_intolerance = {'resource': {'resourceType': 'AllergyIntolerance', 'patient': {'reference': 'Patient/2'}}}

    fhir_res = {'entry': [patient, allergy_intolerance]}

    modified_allergy = deepcopy(allergy_intolerance)
    modified_allergy['resource']['patient'][
        'reference'] = f"Patient/2"  # The reference is the same i.e. no transformation
    expected_resource = {'type': 'searchset', 'entry': [modified_allergy]}

    # When
    actual_resource = prepare_ssp_response(fhir_res)

    # Then
    assert expected_resource == actual_resource


def test_change_bundle_type():
    fhir_res = {'type': 'some-type'}
    expected_resource = {'type': 'searchset'}

    # When
    actual_resource = prepare_ssp_response(fhir_res)

    # Then
    assert expected_resource == actual_resource
