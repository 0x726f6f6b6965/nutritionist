PROJECTNAME := $(shell basename "$(PWD)")

include .env
export $(shell sed 's/=.*//' .env)

.PHONY: dev-run
dev-run:
	@uv run --env-file .env fastapi run app/main.py

.PHONY: build
build:
	@docker build -t fastapi-app -f ./deployment/Dockerfile .

.PHONY: run
run: build
	@docker run --env-file ./.env -p 8080:80 fastapi-app

.PHONY: create-menu
create-menu:
	@uv run --env-file .env python ./deployment/richmenu/create_message.py 

.PHONY: delete-menu
delete-menu:
	@curl -v -X DELETE \
		https://api.line.me/v2/bot/user/all/richmenu \
		-H "Authorization: Bearer $(CHANNEL_ACCESS_TOKEN)"

.PHONY: service-up
service-up: build
	@export POSTGRES_DB=postgres && \
	export POSTGRES_USER=postgres && \
	export POSTGRES_PASSWORD=docker && \
	export POSTGRES_PORT=5432 && \
	export POSTGRES_HOST=db && \
	docker-compose -f ./deployment/compose.yaml --project-directory . up -d

.PHONY: service-down
service-down:
	@docker-compose -f ./deployment/compose.yaml --project-directory . down 

