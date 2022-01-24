JWT_PRIVATE_KEY_FILE ?= $(shell pwd)/jwtRS512.key
KID = "test-1"

-include .env

install:
	poetry install

run:
	poetry run python mediation/main.py --jwt-key $(JWT_PRIVATE_KEY_FILE) --client-id $(GPC_CLIENT_ID) --kid $(KID) --apigee-env $(APIGEE_ENVIRONMENT)

docker-build:
	docker build -t mediation:latest .

docker-run:
	docker run -p 9001:9000 mediation:latest
