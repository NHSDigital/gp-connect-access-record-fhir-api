import requests
import json


class FhirConverter:

    def __init__(self, url: str, env: str):
        self.__env = env
        self.__url = url

    def convert(self, bundle: dict, access_token: str):

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/fhir+json; fhirVersion=3.0",
            "Accept": "application/fhir+json; fhirVersion=4.0",
        }

        res = requests.post(
            "https://int.api.service.nhs.uk/fhir-converter/$convert",
            json=json.loads(bundle),
            headers=headers)

        return res
