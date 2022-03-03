import datetime
import json

from fhirclient.models.bundle import Bundle, BundleEntry
from fhirclient.models.codeableconcept import CodeableConcept
from fhirclient.models.coding import Coding
from fhirclient.models.extension import Extension
from fhirclient.models.fhirdate import FHIRDate
from fhirclient.models.list import List
from fhirclient.models.meta import Meta
from fhirclient.models.operationoutcome import OperationOutcome
from fhirclient.models.operationoutcome import OperationOutcomeIssue
from fhirclient.models.resource import Resource


class BundleFilter:
    def __init__(self, resource: Resource) -> None:
        self.resource = resource

    def filter_for_resource(self, response: str):
        cleaned_response_dict = self._clean_response(response)

        response_bundle = self._load_bundle(cleaned_response_dict)

        filtered_bundle = self._filter_bundle(response_bundle, "searchset")

        filtered_bundle_json = self._bundle_as_json(filtered_bundle)
        return filtered_bundle_json

    def _filter_bundle(self, original_bundle: Bundle, new_bundle_type: str = ""):
        """Extract a chosen resource from existing Bundle and return a new Bundle"""
        filtered_bundle = Bundle()

        if new_bundle_type:
            filtered_bundle.type = new_bundle_type
        else:
            filtered_bundle.type = original_bundle.type

        filtered_bundle_entries = []

        for original_entry in original_bundle.entry:
            if isinstance(original_entry.resource, List):
                op_outcome = self._handle_warnings(original_entry.resource)
                if op_outcome is not None:
                    new_entry = BundleEntry()
                    new_entry.resource = op_outcome
                    filtered_bundle_entries.append(new_entry)
            if isinstance(original_entry.resource, self.resource):
                new_entry = BundleEntry()
                new_entry.resource = original_entry.resource
                filtered_bundle_entries.append(new_entry)
        filtered_bundle.entry = filtered_bundle_entries

        return filtered_bundle

    def _handle_warnings(self, resource: Resource):
        list_resource = resource
        if list_resource.extension:
            for extension in list_resource.extension:
                if (
                    extension.url == "https://fhir.nhs.uk/STU3/StructureDefinition/Extension-CareConnect-GPC"
                                     "-ListWarningCode-1"):
                    return self._build_operationoutcome(extension)

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

    def _build_operationoutcome(self, extension: Extension) -> OperationOutcome:
        op_outcome_issue_list = []
        op_outcome_issue = OperationOutcomeIssue()
        new_opoutcome = OperationOutcome()
        meta = Meta()
        fhir_date = FHIRDate()
        codeable_concept = CodeableConcept()
        coding_list = []
        coding = Coding()

        op_outcome_issue.code = "processing"
        op_outcome_issue.severity = "warning"

        fhir_date.date = datetime.datetime.now()
        meta.lastUpdated = fhir_date
        new_opoutcome.meta = meta

        codeable_concept.system = "https://fhir.nhs.uk/CodeSystem/Spine-ErrorOrWarningCode"

        if extension.valueCode == "confidential-items":
            new_opoutcome.diagnostics = "Items excluded due to confidentiality and/or patient preferences."
            coding.code = "CONFIDENTIAL_ITEMS"
            coding_list.append(coding)
            codeable_concept.coding = coding_list
            codeable_concept.display = "Confidential Items"
        if extension.valueCode == "data-in-transit":
            new_opoutcome.diagnostics = "Patient record transfer from previous GP practice not yet complete; any " \
                                        "information recorded before dd-mmm-yyyy has been excluded "
            coding.code = "DATA_IN_TRANSIT"
            coding_list.append(coding)
            codeable_concept.coding = coding_list
            codeable_concept.display = "Data in Transit"
        if extension.valueCode == "data-awaiting-filing":
            new_opoutcome.diagnostics = "Patient data may be incomplete as there is data supplied by a third party " \
                                        "awaiting review before becoming available. "
            coding.code = "DATA_AWAITING_FILING"
            coding_list.append(coding)
            codeable_concept.coding = coding_list
            codeable_concept.display = "Data Awaiting Filing"
        op_outcome_issue.details = codeable_concept

        location_list = ["/entry"]
        op_outcome_issue.location = location_list

        op_outcome_issue_list.append(op_outcome_issue)
        new_opoutcome.issue = op_outcome_issue_list

        return new_opoutcome

    @staticmethod
    def _load_bundle(response: dict):
        return Bundle(response)

    @staticmethod
    def _bundle_as_json(bundle: Bundle):
        return json.dumps(bundle.as_json())
