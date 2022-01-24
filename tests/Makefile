setup-test:
	docker build -t nhs-login-authenticator ./nhs-login-authenticator

test:
	$(eval TOKEN := $(shell docker run -e CLIENT_ID -e CLIENT_SECRET -e NHS_LOGIN_USER -e NHS_LOGIN_PASSWORD -e NHS_LOGIN_OTP_CODE nhs-login-authenticator))
	TOKEN=$(TOKEN) poetry run pytest -s -v test_api.py 
