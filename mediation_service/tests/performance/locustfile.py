import os
from common.auth import Auth
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
    def allergies(self):
        """Open the allergies overview page."""
        self.client.get("/Allergies", headers=self.headers)


if __name__ == "__main__":
    run_single_user(LoadTestUser)
