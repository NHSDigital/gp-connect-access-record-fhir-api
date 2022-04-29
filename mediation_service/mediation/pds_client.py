from uuid import uuid4

from request_helpers import make_get_request


class PdsClient:
    def __init__(self, url: str, env: str) -> None:
        self._env = env
        self._url = url

    def get_ods_for_nhs_number(self, nhs_number, access_token):

        headers = {
            "X-Request-ID": str(uuid4()),
            "Authorization": f"Bearer {access_token}",
        }
        url = f"https://{self._url}/personal-demographics/FHIR/R4/Patient/{nhs_number}"

        res = make_get_request(call_name="PDS", url=url, headers=headers)

        return self._get_ods(res.json())

    @staticmethod
    def _get_ods(patient: dict) -> str:
        def is_ods_extension(gp):
            return (gp["identifier"]["system"] == "https://fhir.nhs.uk/Id/ods-organization-code")

        ods_ids = filter(is_ods_extension, patient["generalPractitioner"])

        return list(ods_ids)[0]["identifier"]["value"]
