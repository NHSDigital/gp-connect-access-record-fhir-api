import os
from pydantic import ValidationError

from pytest import raises
from bundle_manipulation_fr import load_patient, load_bundle, filter_bundle, bundle_as_json
from fhir.resources.STU3.patient import Patient
from fhir.resources.STU3.bundle import Bundle

dir_path = os.path.dirname(os.path.realpath(__file__))

def test_load_patient():
    # example from https://developer.nhs.uk/apis/gpconnect-1-6-0/foundations_use_case_read_a_patient.html
    # loaded successfully. 
    file_path = os.path.join(dir_path, "files/example_patient.json")
    patient = load_patient(file_path)

    assert isinstance(patient, Patient)
    assert patient.name[0].given[0], "Jane"

def test_load_bundle_from_spec():
    # example from https://developer.nhs.uk/apis/gpconnect-1-6-0/accessrecord_structured_development_fhir_examples_allergies.html
    # is not processed successfully. 
    # entry -> 0 -> resource -> generalPractitioner value is not a valid list (type=type_error.list) 
    file_path = os.path.join(dir_path, "files/example_response_spec.json")
    with raises(ValidationError):
        original_bundle = load_bundle(file_path)

def test_load_bundle_from_orange():
    # response from  orange test lab
    # is loaded but fails validation - ids do not match expected regex - they have _ in them.
    file_path = os.path.join(dir_path, "files/example_response.json")
    with raises(ValidationError):
        original_bundle = load_bundle(file_path)

def test_load_bundle_clean_id():
    # example_response.json but with underscores changed to -
    file_path = os.path.join(dir_path, "files/example_response_clean_id.json")
    original_bundle = load_bundle(file_path)

    assert isinstance(original_bundle, Bundle)

# for bundle that can be loaded test filtering. 
def test_filter_bundle():
    # using example_response_12.json
    file_path = os.path.join(dir_path, "files/example_response_clean_id.json")
    original_bundle = load_bundle(file_path)

    assert isinstance(original_bundle, Bundle)

    filtered_bundle = filter_bundle(original_bundle)
    assert isinstance(filtered_bundle, Bundle)
    assert filtered_bundle.type == 'collection'
    assert len(filtered_bundle.entry) == 28

def test_bundle_as_json():
    """
    Return the filtered bundle as a json.
    """
    file_path = os.path.join(dir_path, "files/example_response_clean_id.json")
    original_bundle = load_bundle(file_path)

    filtered_bundle = filter_bundle(original_bundle)
    filtered_bundle_json = bundle_as_json(filtered_bundle)

    path_to_write = os.path.join(dir_path, "files/filtered_bundle_output_fr.json")
    with open(path_to_write, 'w') as output_json:
        output_json.write(filtered_bundle_json)