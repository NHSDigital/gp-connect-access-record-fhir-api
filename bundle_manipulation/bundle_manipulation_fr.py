"""
Trial using fhir.resources library
"""
from fhir.resources.STU3.bundle import Bundle, BundleEntry
from fhir.resources.STU3.patient import Patient
from fhir.resources.STU3.allergyintolerance import AllergyIntolerance


def load_patient(filepath):
    return Patient.parse_file(filepath)


def load_bundle(filepath):
    return Bundle.parse_file(filepath)


def filter_bundle(bundle_object: Bundle):
    # create new bundle
    new_bundle = Bundle.construct()

    # take out type from the original bundle and add to new
    new_bundle.type = bundle_object.type

    # take out the allergy intolerances from the original bundle
    new_bundle_entries = []
    for entry in bundle_object.entry:
        if isinstance(entry.resource, AllergyIntolerance):
            bundle_entry = BundleEntry.construct()
            bundle_entry.resource = entry.resource
            new_bundle_entries.append(bundle_entry)

    new_bundle.entry = new_bundle_entries

    return new_bundle


def bundle_as_json(bundle: Bundle):
    return bundle.json(indent=1)
