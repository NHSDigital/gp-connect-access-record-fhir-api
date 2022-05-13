JWT_PRIVATE_KEY_CONTENT ?= $(shell cat `pwd`/jwtRS512.key)
KID = "test-1"

-include .env

install:
	poetry install

run:
	GPC_PRIVATE_KEY_INT="$(JWT_PRIVATE_KEY_CONTENT)" GPC_CLIENT_ID=$(GPC_CLIENT_ID) KID=$(KID) APIGEE_ENVIRONMENT=$(APIGEE_ENVIRONMENT) SSP_URL=$(SSP_URL) APIGEE_URL=$(APIGEE_URL) poetry run python mediation/main.py

docker-build:
	docker build -t mediation:latest .

docker-run: docker-build
	docker run -p 9000:9000 -e GPC_PRIVATE_KEY_INT="$(JWT_PRIVATE_KEY_CONTENT)" -e GPC_CLIENT_ID=$(GPC_CLIENT_ID) -e KID=$(KID) -e APIGEE_ENVIRONMENT=$(APIGEE_ENVIRONMENT) -e APIGEE_URL=$(APIGEE_URL) -e SSP_URL=$(SSP_URL) mediation:latest

locust:
	LOCUST_HOST="$(LOCUST_HOST)" CALLBACK_URL="$(CALLBACK_URL)" CLIENT_ID="$(CLIENT_ID)" CLIENT_SECRET="$(CLIENT_SECRET)" locust -f tests/performance/locustfile.py
