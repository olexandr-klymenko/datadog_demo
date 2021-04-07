SERVICE_A=django3
DATADOG_DEMO=demo
DEMO_ITERATIONS=100

HIDE_DOCKER_CLI_DETAILES=COMPOSE_DOCKER_CLI_BUILD=1 DOCKER_BUILDKIT=1

build:
	$(HIDE_DOCKER_CLI_DETAILES) docker-compose build

init_db:
	docker-compose run --rm $(SERVICE_A) bash init_db.sh

up:
	docker-compose up -d  --remove-orphans

down:
	docker-compose down

run_demo:
	docker-compose run --rm $(DATADOG_DEMO) python run_demo.py $(DEMO_ITERATIONS)

restart: down build up

logs:
	docker-compose logs -f
