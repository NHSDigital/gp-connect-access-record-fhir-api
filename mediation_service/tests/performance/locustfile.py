import os
from common.auth import Auth
from random import randint
from locust import HttpUser, task, between, run_single_user


class LoadTestUser(HttpUser):
    cookie = ""
    wait_time = between(1, 5)
    host = "http://localhost:5000"

    def auth(self):
        return Auth(
            url=os.environ["LOCUST_HOST"],
            callback_url=os.environ["CALLBACK_URL"],
            client_id=os.environ["CLIENT_ID"],
            client_secret=os.environ["CLIENT_SECRET"]
        )

    def on_start(self):
        authenticator = self.auth()
        self.credentials = authenticator.login()
        self.headers = {
            "Authorization": self.credentials["token_type"] + " " + self.credentials["access_token"],
            "NHSD-Identity-UUID": "1234567890",
            "NHSD-Session-URID": "1234567890",
        }

    @task
    def index(self):
        """Open the index page."""
        self.client.get("/", headers=self.headers)

    @task
    def home(self):
        """Open the home page."""
        self.client.get("/Home", headers=self.headers)

    @task(3)
    def allergies(self):
        """Open the allergies overview page."""
        self.client.get("/Allergies", headers=self.headers)

    @task(5)
    def allergy_detail(self):
        """Open the detail page for a random allergy."""
        # Pick a random allergy index from the list of allergies in the API response data
        # TODO - base the length off of the size of the actual dataset
        allergy_idx = randint(0, 27)
        self.client.get(f"/AllergyDetails?id={allergy_idx}", headers=self.headers)


if __name__ == "__main__":
    run_single_user(LoadTestUser)
