install:
	poetry install

run:
	GPC_CLIENT_ID=$(GPC_CLIENT_ID) APIGEE_ENVIRONMENT=$(APIGEE_ENVIRONMENT) poetry run python mediation/main.py

docker-build:
	docker build -t mediation:latest .

docker-run:
	docker run -p 9000:9000 -e GPC_CLIENT_ID=$(GPC_CLIENT_ID) -e APIGEE_ENVIRONMENT=$(APIGEE_ENVIRONMENT) mediation:latest