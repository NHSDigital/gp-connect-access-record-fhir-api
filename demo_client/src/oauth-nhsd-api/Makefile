-include .env

build:
	docker build -t democlient .

run:
	docker run -p 5000:5000 -e CLIENT_ID="$(CLIENT_ID)" -e CLIENT_SECRET="$(CLIENT_SECRET)" democlient
