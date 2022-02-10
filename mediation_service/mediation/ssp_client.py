import requests

from orange_jwt import create_orange_jwt


class SspClient:

    def __init__(self, url: str) -> None:
        self._url = url

    def get_allergy_intolerance_bundle(self, ods: str):
        headers = {
            "Accept": "application/fhir+json",
            "Ssp-From": "200000000359",
            "Ssp-To": "918999198738",
            "Ssp-InteractionID": "urn:nhs:names:services:gpconnect:fhir:operation:gpc.getstructuredrecord-1",
            "Ssp-TraceID": "09a01679-2564-0fb4-5129-aecc81ea2706",
            "Content-Type": "application/fhir+json",
            "Authorization": f"Bearer {create_orange_jwt(ods)}"
        }

        _body = self.__get_orange_payload()
        # ODS code on the request is hardcoded --- need to be changed
        res = requests.post(
            f"https://{self._url}/B82617/STU3/1/gpconnect/structured/fhir/Patient/$gpc.getstructuredrecord",
            headers=headers,
            data=_body,
            verify=False
        )

        return res.text

    @staticmethod
    def __get_orange_payload() -> str:
        with open('getstructuredrecord_payload.json', 'r') as f:
            json_text = f.read()

        return json_text

    @staticmethod
    def __get_filtered_bundle(param):
        # to use Hirra code to filter original bundle
        return param
