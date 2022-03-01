SERVICE_NAME = gp-connect-access-record-fhir-api
PROXY_BASE_PATH = gp-connect-access-record

-include .env

setup-test:
	docker build -t nhs-login-authenticator ./nhs-login-authenticator

docker_env := -e CLIENT_ID=$(CLIENT_ID) \
-e CLIENT_SECRET=$(CLIENT_SECRET) \
-e NHS_LOGIN_USER=$(NHS_LOGIN_USER) \
-e NHS_LOGIN_PASSWORD_B64="$(NHS_LOGIN_PASSWORD_B64)"  \
-e NHS_LOGIN_OTP_CODE=$(NHS_LOGIN_OTP_CODE) \
-e APIGEE_ENVIRONMENT=$(APIGEE_ENVIRONMENT)

token: setup-test
	docker run $(docker_env)  nhs-login-authenticator

cmd_opts = --service-name="$(SERVICE_NAME)" \
		   --proxy-base-path="$(PROXY_BASE_PATH)" \
		   --apigee-environment="$(APIGEE_ENVIRONMENT)" \
		   --pr-no="$(PR_NO)" \
		   --status-api-key="$(STATUS_API_KEY)"

run: setup-test
	$(eval TOKEN := $(shell docker run $(docker_env) nhs-login-authenticator))
	poetry run pytest -s -v $(cmd_opts) --access-token="$(TOKEN)"  $(f)

run-%: setup-test
	$(eval TOKEN := $(shell docker run $(docker_env) nhs-login-authenticator))
	poetry run pytest -s -m $(subst run-,,$@) -v $(cmd_opts) --access-token="$(TOKEN)" test_api.py

