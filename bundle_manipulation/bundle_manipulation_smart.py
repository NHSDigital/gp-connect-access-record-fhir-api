"""
Trial using SMART on FHIR library
"""
from fhirclient.models.bundle import Bundle, BundleEntry
from fhirclient.models.patient import Patient
import fhirclient.models.allergyintolerance as allergyintolerance
import json


def load_bundle(filepath):
    return _load_resource(filepath, Bundle)


def load_patient(filepath):
    return _load_resource(filepath, Patient)


def filter_bundle(bundle_object: Bundle):
    # create new bundle
    new_bundle = Bundle()

    # take out type from the original bundle and add to new
    new_bundle.type = bundle_object.type

    # take out the allergy intolerances from the original bundle
    new_bundle_entries = []
    for entry in bundle_object.entry:
        if isinstance(entry.resource, allergyintolerance.AllergyIntolerance):
            bundle_entry = BundleEntry()
            bundle_entry.resource = entry.resource
            new_bundle_entries.append(bundle_entry)

    new_bundle.entry = new_bundle_entries

    return new_bundle


def bundle_as_json(bundle: Bundle):
    return json.dumps(bundle.as_json(), indent=1)


def _load_resource(filepath, resource):
    with open(filepath, "r") as response_json:
        bundle_js = json.load(response_json)
    return resource(bundle_js)
