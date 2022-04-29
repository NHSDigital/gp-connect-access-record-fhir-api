from request_helpers import make_get_request


class SdsClient:
    def __init__(self, client_id: str, apigee_url: str) -> None:
        self._client_id = client_id
        self._apigee_url = apigee_url

    def get_toASID(self, ods_code):
        url = f"https://{self._apigee_url}/spine-directory/FHIR/R4/Device"

        headers = {"apikey": self._client_id}

        params = {
            "organization": f"https://fhir.nhs.uk/Id/ods-organization-code|{ods_code}",
            "identifier": "https://fhir.nhs.uk/Id/nhsServiceInteractionId|urn:nhs:names:services:gpconnect:fhir:operation:gpc.getstructuredrecord-1",
        }

        res = make_get_request(
            call_name="SDS get_toASID", url=url, headers=headers, params=params
        )

        return self._get_toAsid(res.json())

    def _get_toAsid(self, bundle) -> str:
        if bundle["total"] == 0:
            return None
        else:
            device = bundle["entry"][0]["resource"]
            for asidId in device:
                if (
                    device["identifier"][0]["system"]
                    == "https://fhir.nhs.uk/Id/nhsSpineASID"
                ):
                    return device["identifier"][0]["value"]
            return asidId

    def get_URL(self, ods_code):
        url = f"https://{self._apigee_url}/spine-directory/FHIR/R4/Endpoint"

        headers = {"apikey": self._client_id}

        params = {
            "organization": f"https://fhir.nhs.uk/Id/ods-organization-code|{ods_code}",
            "identifier": "https://fhir.nhs.uk/Id/nhsServiceInteractionId|urn:nhs:names:services:gpconnect:fhir:operation:gpc.getstructuredrecord-1",
        }

        res = make_get_request(
            call_name="SDS get_URL", url=url, headers=headers, params=params
        )

        return self._get_URL(res.json())

    def _get_URL(self, bundle) -> str:
        if bundle["total"] == 0:
            return None
        else:
            return bundle["entry"][0]["resource"]["address"]
