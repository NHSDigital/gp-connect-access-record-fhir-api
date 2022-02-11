from fhirclient.models.bundle import Bundle, BundleEntry
from fhirclient.models.resource import Resource
from fhirclient.models.allergyintolerance import AllergyIntolerance
import json


def filter_for_allergy_intolerance(response: str):
    # response is json str tunr into dict
    response_bundle = _load_bundle(response)

    filtered_bundle = _filter_bundle(response_bundle, AllergyIntolerance)

    filtered_bundle_json = _bundle_as_json(filtered_bundle)
    return filtered_bundle_json


def _load_bundle(response: str):
    response_as_dict = json.loads(response)
    return Bundle(response_as_dict)


def _filter_bundle(original_bundle: Bundle, resource_type: Resource):
    filtered_bundle = Bundle()

    # take out type from the original bundle and add to new
    filtered_bundle.type = original_bundle.type

    filtered_bundle_entries = []

    # extract chosen resource from the original bundle
    for original_entry in original_bundle.entry:
        if isinstance(original_entry.resource, resource_type):
            new_entry = BundleEntry()
            new_entry.resource = original_entry.resource
            filtered_bundle_entries.append(new_entry)

    filtered_bundle.entry = filtered_bundle_entries

    return filtered_bundle


def _bundle_as_json(bundle: Bundle):
    return json.dumps(bundle.as_json())
