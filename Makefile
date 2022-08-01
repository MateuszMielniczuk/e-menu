include .env

DC = $(COMPOSE)
PY = $(DC) exec api
DUMP = /docker-entrypoint-initdb.d/dump.sql

#======================= CONTAINERS_MANAGEMENT =========================
#=======================================================================
# build and run containers and remove orphan containers
up:
	$(DC) up
buildup:
	$(DC) up --build --remove-orphans
down:
	$(DC) down
# down + volumes
down-v:
	$(DC) down -v
logs:
	$(DC) logs
prune:
	docker system prune -a --volumes


#======================= BACKEND FASTAPI ===============================
#=======================================================================

lint-all: black-exec isort-exec flake8
	@echo 'Linting done!'
backend-shell:
	$(PY) bash
flake8:
	$(PY) flake8 .
# --preview flag helping with wrapping long strings
black:
	$(PY) black --preview --check .
black-diff:
	$(PY) black --preview --diff .
black-exec:
	$(PY) black --preview .
isort:
	$(PY) isort . --check-only --skip venv --skip versions
isort-diff:
	$(PY) isort . --diff --skip venv --skip versions
isort-exec:
	$(PY) isort . --skip venv --skip versions
backend-dump:
	$(RCV) backend /home/python/.local abd-backend

#====================== DATABASE MANAGEMENT ============================
#=======================================================================

makemigration:
	$(PY) bash -c 'echo "Type commit message:" && read && alembic revision --autogenerate -m"$${REPLY}"'
migrate:
	$(PY) alembic upgrade head
migrate-downgrade:
	$(PY) alembic downgrade -1
migrate-upgrate:
	$(PY) alembic upgrade +1

db-dump:
	$(DC) exec postgres /bin/sh -c\
	  "pg_dump $(DATABASE_NAME) -U $(DATABASE_USERNAME) -h $(DATABASE_CLIENT) > $(DUMP)"
