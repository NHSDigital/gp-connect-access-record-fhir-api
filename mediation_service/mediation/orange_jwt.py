import base64
import json
import jwt
from datetime import datetime, timedelta


def create_orange_jwt(ods_code: str):

    targetURI = "https://orange.testlab.nhs.uk/B82617/STU3/1/gpconnect/structured/fhir"
    currentTime = datetime.now()
    expiryTime = currentTime + timedelta(minutes=5)
    jwtCreationTime = int(datetime.timestamp(currentTime))
    jwtExpiryTime = int(datetime.timestamp(expiryTime))

    header = {
        "alg": "none",
        "typ": "JWT"
    }
    payload = {
        "iss": "http://gpconnect-postman-url",
        "sub": "1",
        "aud": targetURI,
        "exp": jwtExpiryTime,
        "iat": jwtCreationTime,
        "reason_for_request": "directcare",
        "requested_scope": "patient/*.read",
        "requesting_device": {
            "resourceType": "Device",
            "id": "1",
            "identifier": [
                {
                    "system": "Web Interface",
                    "value": "Postman example consumer"
                }
            ],
            "model": "Postman",
            "version": "1.0"
        },
        "requesting_organization": {
            "resourceType": "Organization",
            "identifier": [
                {
                    "system": "https://fhir.nhs.uk/Id/ods-organization-code",
                    "value": "12"
                }
            ],
            "name": "Postman Organization"
        },
        "requesting_practitioner": {
            "resourceType": "Practitioner",
            "id": "1",
            "identifier": [
                {
                    "system": "https://fhir.nhs.uk/Id/sds-user-id",
                    "value": "G13579135"
                },
                {
                    "system": "https://fhir.nhs.uk/Id/sds-role-profile-id",
                    "value": "111111111"
                },
            ],
            "name": [{
                "family": "Demonstrator",
                "given": [
                    "GPConnect"
                ],
                "prefix": [
                    "Mr"
                ]
            }]
        }
    }

    _jwt = jwt.encode(payload=payload, key=None, headers=header, algorithm="HS256")

    return _jwt


class OrangeJwt:

    def __init__(self) -> None:
        pass



