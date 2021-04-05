HIDE_DOCKER_CLI_DETAILES=COMPOSE_DOCKER_CLI_BUILD=1 DOCKER_BUILDKIT=1

build:
	$(HIDE_DOCKER_CLI_DETAILES) docker-compose build

up:
	docker-compose up -d  --remove-orphans

down:
	docker-compose down

restart: down build up

logs:
	docker-compose logs -f
