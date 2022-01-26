"""
Tests for using SMART on FHIR library
"""
from fhirclient.models.bundle import Bundle
from fhirclient.models.patient import Patient
from fhirclient.models.fhirabstractbase import FHIRValidationError
from pytest import raises
from bundle_manipulation_smart import load_bundle, load_patient, filter_bundle, bundle_as_json
import os

dir_path = os.path.dirname(os.path.realpath(__file__))


def test_load_patient():
    # example from gpconnect-1-6-0 spec
    # loaded successfully.
    file_path = os.path.join(dir_path, "files/example_patient.json")
    patient = load_patient(file_path)

    assert isinstance(patient, Patient)
    assert patient.name[0].given[0], "Jane"


def test_load_bundle_from_spec():
    # rxample from gpconnect-1-6-0 allergies example
    # is not processed successfully. Error on generalPractitioner - expects this Resource to be a list.
    file_path = os.path.join(dir_path, "files/example_response_spec.json")
    with raises(FHIRValidationError):
        load_bundle(file_path)


def test_load_bundle_from_orange():
    # response from  orange test lab
    # is successfully
    file_path = os.path.join(dir_path, "files/example_response.json")
    original_bundle = load_bundle(file_path)

    assert isinstance(original_bundle, Bundle)


# for a bundle that can be loaded, filter allergy intolerance
def test_filter_bundle():
    # using example_response.json
    file_path = os.path.join(dir_path, "files/example_response.json")
    original_bundle = load_bundle(file_path)

    assert isinstance(original_bundle, Bundle)

    filtered_bundle = filter_bundle(original_bundle)
    assert isinstance(filtered_bundle, Bundle)
    assert len(filtered_bundle.entry) == 28


def test_bundle_as_json():
    """
    Return the filtered bundle as a json.
    """
    file_path = os.path.join(dir_path, "files/example_response.json")
    original_bundle = load_bundle(file_path)

    filtered_bundle = filter_bundle(original_bundle)
    filtered_bundle_json = bundle_as_json(filtered_bundle)

    path_to_write = os.path.join(dir_path, "files/filtered_bundle_output_smart.json")
    with open(path_to_write, 'w') as output_json:
        output_json.write(filtered_bundle_json)


def test_load_bundle_from_int():
    # response from  int
    # is successfully
    file_path = os.path.join(dir_path, "files/example_int.json")
    original_bundle = load_bundle(file_path)

    assert isinstance(original_bundle, Bundle)


def test_filter_bundle_from_int():
    # using example_response.json
    file_path = os.path.join(dir_path, "files/example_int.json")
    original_bundle = load_bundle(file_path)

    assert isinstance(original_bundle, Bundle)

    filtered_bundle = filter_bundle(original_bundle)
    assert isinstance(filtered_bundle, Bundle)
    assert len(filtered_bundle.entry) == 1

    filtered_bundle_json = bundle_as_json(filtered_bundle)
    path_to_write = os.path.join(dir_path, "files/filtered_int_bundle_output_smart.json")
    with open(path_to_write, 'w') as output_json:
        output_json.write(filtered_bundle_json)
