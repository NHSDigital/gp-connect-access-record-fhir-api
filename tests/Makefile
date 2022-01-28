-include .env

setup-test:
	docker build -t nhs-login-authenticator ./nhs-login-authenticator

docker_env := -e CLIENT_ID=$(CLIENT_ID) \
-e CLIENT_SECRET=$(CLIENT_SECRET) \
-e NHS_LOGIN_USER=$(NHS_LOGIN_USER) \
-e NHS_LOGIN_PASSWORD_B64="$(NHS_LOGIN_PASSWORD_B64)"  \
-e NHS_LOGIN_OTP_CODE=$(NHS_LOGIN_OTP_CODE)

token: setup-test
	docker run $(docker_env)  nhs-login-authenticator

test: setup-test
	$(eval TOKEN := $(shell docker run $(docker_env) nhs-login-authenticator))
	TOKEN=$(TOKEN) poetry run pytest -s -v test_api.py
