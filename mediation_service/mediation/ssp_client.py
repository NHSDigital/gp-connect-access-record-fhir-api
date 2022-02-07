import json

import chevron
import requests

class SspClient:

    def __init__(self, asid: str, nhs_number: int) -> None:
        self.__asid = asid
        self.__nhs_number = nhs_number

    def get_allergy_intolerance_bundle(self, asid_number: str,
                                       nhs_number: int,
                                       ssp_from: int,
                                       ssp_to: int) -> str:

        headers = {
            "Accept": "application/fhir+json",
            "Ssp-From": ssp_from,
            "Ssp-To": ssp_to,
            "Ssp-InteractionID": "urn:nhs:names:services:gpconnect:fhir:operation:gpc.getstructuredrecord-1",
            "Ssp-TraceID": "09a01679-2564-0fb4-5129-aecc81ea2706",
            "Content-Type": "application/fhir+json",
            "Authorization": f"Bearer {self.__get_orange_jwt()}"
        }

        body = self.__get_orange_payload(nhs_number)

        res = requests.post(
            f"https://nhsd-jira.digital.nhs.uk/secure/attachment/407612/providerURL_1_5_x_structured.postman_environment.json#:~:text=https%3A//orange.testlab.nhs.uk/B82617/STU3/1/gpconnect/structured/fhir//Patient/$gpc.getstructuredrecord",
            headers=headers,
            body=body
        )

        return self.__get_filtered_bundle(res.json())


    @staticmethod
    def __get_orange_jwt() -> str:
        return "dummy_jwt_text"

    @staticmethod
    def __get_orange_payload(nhs_number: int) -> str:
        try:
            json_payload = open("getstructuredrecord_payload.json", "r").read()
        except Exception as e:
            return "Payload not loaded" + str(e)

        chevron.render(json_payload, {'patient_nhs_number_1_5_x': nhs_number})

        return json.dumps(json_payload)

    @staticmethod
    def __get_filtered_bundle(self, param):
        return param

