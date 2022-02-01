import json
from uuid import uuid4

import requests

from client_credentials import AuthClientCredentials


class PdsClient:

    def __init__(self, auth: AuthClientCredentials, env: str) -> None:
        self.__auth = auth
        self.__env = env

    def get_ods_for_nhs_number(self, nhs_number):
        access_token = self.__auth.get_access_token()
        headers = {
            "X-Request-ID": str(uuid4()),
            "Authorization": f"Bearer {access_token}"
        }

        try:
            res = requests.get(
                f"https://{self.__env}.api.service.nhs.uk/personal-demographics/FHIR/R4/Patients/{nhs_number}",
                headers=headers)

        except Exception as e:
            return json.dumps({"exception": e})

        return json.dumps({"text": res.text, "status": res.status_code})
        # return self.__get_ods(res.json())

    @staticmethod
    def __get_ods(patient: dict) -> str:
        def is_ods_extension(gp):
            return gp["identifier"]["system"] == "https://fhir.nhs.uk/Id/ods-organization-code"

        ods_ids = filter(is_ods_extension, patient["generalPractitioner"])

        return list(ods_ids)[0]["identifier"]["value"]
