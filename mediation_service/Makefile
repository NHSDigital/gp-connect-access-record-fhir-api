JWT_PRIVATE_KEY_FILE ?= $(shell pwd)/jwtRS512.key
JWT_PRIVATE_KEY_CONTENT ?= $(shell cat `pwd`/jwtRS512.key)
KID = "test-1"

-include .env

install:
	poetry install

run:
	GPC_PRIVATE_KEY_INT="$(JWT_PRIVATE_KEY_CONTENT)" GPC_CLIENT_ID=$(GPC_CLIENT_ID) KID=$(KID) APIGEE_ENVIRONMENT=$(APIGEE_ENVIRONMENT) poetry run python mediation/main.py

docker-build:
	docker build -t mediation:latest .

docker-run: docker-build
	docker run -p 9000:9000 -e GPC_PRIVATE_KEY_INT="$(JWT_PRIVATE_KEY_CONTENT)" -e GPC_CLIENT_ID=$(GPC_CLIENT_ID) -e KID=$(KID) -e APIGEE_ENVIRONMENT=$(APIGEE_ENVIRONMENT) mediation:latest
