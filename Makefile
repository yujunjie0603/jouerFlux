.PHONY: show_log build up test down db_init db_migrate db_upgrade db_downgrade

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

