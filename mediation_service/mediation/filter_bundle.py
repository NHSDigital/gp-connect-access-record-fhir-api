from fhirclient.models.bundle import Bundle, BundleEntry
from fhirclient.models.resource import Resource
import json


class BundleFilter:
    def __init__(self, resource: Resource) -> None:
        self.resource = resource

    def filter_for_resource(self, response: str):
        cleaned_response_dict = self._clean_response(response)

        response_bundle = self._load_bundle(cleaned_response_dict)

        filtered_bundle = self._filter_bundle(response_bundle)

        filtered_bundle_json = self._bundle_as_json(filtered_bundle)
        return filtered_bundle_json

    def _filter_bundle(self, original_bundle: Bundle):
        """Extract a chosen resource from a bundle"""
        filtered_bundle = Bundle()

        # take out type from the original bundle and add to new
        filtered_bundle.type = original_bundle.type

        filtered_bundle_entries = []

        for original_entry in original_bundle.entry:
            if isinstance(original_entry.resource, self.resource):
                new_entry = BundleEntry()
                new_entry.resource = original_entry.resource
                filtered_bundle_entries.append(new_entry)

        filtered_bundle.entry = filtered_bundle_entries

        return filtered_bundle

    def _clean_response(self, response: str):
        """Remove any fhir_comments from json response before creating Bundle object"""
        response_dict = json.loads(response)
        return self._remove_comments(response_dict)

    def _remove_comments(self, json_obj):
        """Walk through json object to remove selected key"""
        if not isinstance(json_obj, (dict, list)):
            return json_obj

        if isinstance(json_obj, list):
            return [self._remove_comments(value) for value in json_obj]

        return {
            key: self._remove_comments(value)
            for key, value in json_obj.items()
            if key not in ["fhir_comments"]
        }

    @staticmethod
    def _load_bundle(response: dict):
        return Bundle(response)

    @staticmethod
    def _bundle_as_json(bundle: Bundle):
        return json.dumps(bundle.as_json())
