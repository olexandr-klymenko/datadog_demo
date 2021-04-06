SERVICE_A=django3
DATADOG_DEMO=datadog_demo

HIDE_DOCKER_CLI_DETAILES=COMPOSE_DOCKER_CLI_BUILD=1 DOCKER_BUILDKIT=1

build:
	$(HIDE_DOCKER_CLI_DETAILES) docker-compose build

init_db:
	docker-compose run --rm $(SERVICE_A) bash init_db.sh

up:
	docker-compose up -d  --remove-orphans

down:
	docker-compose down

build_demo:
	docker build demo -t $(DATADOG_DEMO)

run_demo:
	docker run -t $(DATADOG_DEMO) python run_demo.py

restart: down build up

logs:
	docker-compose logs -f
