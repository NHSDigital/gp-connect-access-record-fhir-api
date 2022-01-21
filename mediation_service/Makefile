install:
	poetry install

run:
	poetry run python mediation/main.py

docker-build:
	docker build -t mediation:latest .

docker-run:
	docker run -p 9001:9000 mediation:latest
