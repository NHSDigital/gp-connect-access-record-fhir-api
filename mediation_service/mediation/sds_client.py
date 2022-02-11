import requests


class SdsClient:
    def __init__(self, client_id: str, apigee_url: str) -> None:
        self.__client_id = client_id
        self.__apigee_url = apigee_url

    def get_toASID(self, ods_code):
        headers = {"apikey": self.__client_id}

        params = {
            "organization": f"https://fhir.nhs.uk/Id/ods-organization-code|{ods_code}",
            "identifier": "https://fhir.nhs.uk/Id/nhsServiceInteractionId|urn:nhs:names:services:gpconnect:fhir:operation:gpc.getstructuredrecord-1",
        }

        res = requests.get(
            f"https://{self.__apigee_url}/spine-directory/FHIR/R4/Device",
            headers=headers,
            params=params,
        )

        return self.__get_toAsid(res.json())

    def __get_toAsid(self, bundle) -> str:
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
        headers = {"apikey": self.__client_id}

        params = {
            "organization": f"https://fhir.nhs.uk/Id/ods-organization-code|{ods_code}",
            "identifier": "https://fhir.nhs.uk/Id/nhsServiceInteractionId|urn:nhs:names:services:gpconnect:fhir:operation:gpc.getstructuredrecord-1",
        }

        res = requests.get(
            f"https://{self.__apigee_url}/spine-directory/FHIR/R4/Endpoint",
            headers=headers,
            params=params,
        )

        return self.__get_URL(res.json())

    def __get_URL(self, bundle) -> str:
        if bundle["total"] == 0:
            return None
        else:
            return bundle["entry"][0]["resource"]["address"]
