import os

from orange_jwt import create_orange_jwt
from request_helpers import make_post_request


class SspClient:

    def __init__(self, url: str) -> None:
        self._url = url

    def get_allergy_intolerance_bundle(self, ods: dict):
        # update Ssp-From with to_ASID from dict
        url = f"https://{self._url}/B82617/STU3/1/gpconnect/structured/fhir/Patient/$gpc.getstructuredrecord"
        headers = {
            "Accept": "application/fhir+json",
            "Ssp-From": "200000000359",
            "Ssp-To": "918999198738",
            "Ssp-InteractionID": "urn:nhs:names:services:gpconnect:fhir:operation:gpc.getstructuredrecord-1",
            "Ssp-TraceID": "09a01679-2564-0fb4-5129-aecc81ea2706",
            "Content-Type": "application/fhir+json",
            "Authorization": f"Bearer {create_orange_jwt(ods['to_ASID'])}"
        }

        _body = self.__get_orange_payload()
        # ODS code on the request is hardcoded --- need to be changed
        res = make_post_request(call_name="SSP get allergy intolerance bundle", url=url, headers=headers, data=_body, verify=False)

        return res.json()

    @staticmethod
    def __get_orange_payload() -> str:
        dir_path = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(dir_path, 'getstructuredrecord_payload.json')

        with open(file_path, 'r') as f:
            json_text = f.read()

        return json_text
