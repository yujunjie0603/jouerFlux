.PHONY: show_log build up test down db_init db_migrate db_upgrade db_downgrade

help:
	@echo "Available commands:"
	@echo "  make show_log       - Show logs for the jouerflux service"
	@echo "  make build          - Build the Docker images"
	@echo "  make up             - Start the Docker containers in detached mode"
	@echo "  make test           - Run tests using pytest"
	@echo "  make down           - Stop and remove the Docker containers"
	@echo "  make db_init        - Initialize the database"
	@echo "  make db_migrate     - Create a new database migration"
	@echo "  make db_upgrade     - Apply the latest database migrations"
	@echo "  make db_downgrade   - Revert the last database migration"

show_log:
	docker compose logs -f jouerflux

build:
	docker compose build

up:
	docker compose up -d

test:
	docker compose run  jouerflux pytest

down:
	docker compose down

db_init:
	docker compose run  jouerflux flask db init

db_migrate:
	docker compose run  jouerflux flask db migrate

db_upgrade:
	docker compose run  jouerflux flask db upgrade

db_downgrade:
	docker compose run  jouerflux flask db downgrade

