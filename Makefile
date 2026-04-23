.PHONY: dev

RUN_BACKEND = uv run honcho start backend
RUN_DEMO = $(RUN_BACKEND) demo-frontend
RUN_DB = @docker compose up database -d && until docker compose exec database pg_isready -U postgres; do sleep 0.5; done

dev:
	$(RUN_DB)
	$(RUN_DEMO)

run-backend:
	$(RUN_DB)
	$(RUN_BACKEND)

dev-tunnel:
	$(RUN_DB)
	$(RUN_DEMO) tunnel

db-start:
	$(RUN_DB)

db-sh:
	@docker compose exec database psql -U postgres -d vitapp

db-stop:
	docker compose down database

db-drop: db-stop
	docker volume rm -f vitapp_pgdata > /dev/null || true
	@echo "database container stopped, volume deleted"

db-migrate: db-start
	@uv run alembic upgrade head

db-gen-mig: db-start db-migrate
	@uv run alembic revision --autogenerate -m "$(m)"