DOCKER_COMPOSE := docker-compose.yml
DOCKER_ENV := .env_dev
DOCKER_COMPOSE_RUNNER := docker compose



.PHONY: migrate-create
migrate-create:
	python -m alembic revision --autogenerate -m "Added initial tables"


.PHONY: migrate-up
migrate-up:
	python -m alembic upgrade head

.PHONY: compose-up
compose-up:
	$(DOCKER_COMPOSE_RUNNER) -f $(DOCKER_COMPOSE) --env-file $(DOCKER_ENV) up -d


.PHONY: compose-build
compose-build:
	$(DOCKER_COMPOSE_RUNNER) -f $(DOCKER_COMPOSE) --env-file $(DOCKER_ENV) build


.PHONY: compose-pull
compose-pull:
	$(DOCKER_COMPOSE_RUNNER) -f $(DOCKER_COMPOSE) --env-file $(DOCKER_ENV) pull

.PHONY: compose-down
compose-down:
	$(DOCKER_COMPOSE_RUNNER) -f $(DOCKER_COMPOSE) --env-file $(DOCKER_ENV) down

.PHONY: compose-logs
compose-logs:
	$(DOCKER_COMPOSE_RUNNER) -f $(DOCKER_COMPOSE) --env-file $(DOCKER_ENV) logs -f