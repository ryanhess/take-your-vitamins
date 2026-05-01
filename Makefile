.PHONY: dev

RUN_BACKEND = uv run honcho start backend
RUN_DEMO = $(RUN_BACKEND) demo-frontend
RUN_DB = @docker compose up database -d && until docker compose exec database pg_isready -U postgres; do sleep 0.5; done

dev:
	$(RUN_DB)
	$(RUN_BACKEND) frontend

run-backend:
	$(RUN_DB)
	$(RUN_BACKEND)

tunnel:
	$(RUN_DB)
	$(RUN_BACKEND) frontend tunnel

db-start:
	$(RUN_DB)

db-start-test:
	docker compose up test_database -d

db-sh:
	@docker compose exec database psql -U postgres -d vitapp

stopall:
	-pkill -f "uvicorn backend:app" 2>/dev/null
	-pkill -f "marimo run demo.py" 2>/dev/null
	-pkill -f "npm run dev" 2>/dev/null
	-pkill -f "ngrok http" 2>/dev/null
	docker compose down database

db-stop:
	@docker compose down database test_database

db-drop: db-stop
	docker volume rm -f vitapp_pgdata > /dev/null || true
	@echo "database container stopped, volume deleted"

db-drop-test: db-stop
	docker volume rm -f vitapp_test_pgdata > /dev/null || true
	@echo "test database container stopped, volume deleted"

db-migrate: db-start
	@uv run alembic upgrade head

db-gen-mig: db-start db-migrate
	@uv run alembic revision --autogenerate -m "$(m)"

install:
	@uv sync &&	cp .env.example .env && direnv allow; \
	cd frontend; npm install
