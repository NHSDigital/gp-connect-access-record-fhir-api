from request_helpers import make_post_request


class FhirConverter:
    def __init__(self, url: str, env: str):
        self._env = env
        self._url = url

    def convert(self, bundle: dict, access_token: str):
        url = f"https://{self._url}/fhir-converter/$convert"

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/fhir+json; fhirVersion=3.0",
            "Accept": "application/fhir+json; fhirVersion=4.0",
        }

        res = make_post_request(
            call_name="Fhir Convertor", url=url, json=bundle, headers=headers
        )

        return res.json()
