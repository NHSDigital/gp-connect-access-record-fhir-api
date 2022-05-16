import os
from locust import HttpUser, task, between, run_single_user
from locust.exception import RescheduleTask

RETRY_ON_FAIL = False


class LoadTestUser(HttpUser):
    cookie = ""
    wait_time = between(1, 5)
    host = os.environ["SERVICE_BASE_PATH"]

    @task
    def allergies(self):
        """Hit the AllergyIntolerance endpoint."""
        allergy_endpoint = "/AllergyIntolerance"
        patient_querystring = "?patient=https://fhir.nhs.uk/Id/9690937286"

        with self.client.get(allergy_endpoint + patient_querystring, catch_response=True) as response:
            if response.status_code != 200 and RETRY_ON_FAIL:
                raise RescheduleTask()


if __name__ == "__main__":
    run_single_user(LoadTestUser)
