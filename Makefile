.PHONY: dev

RUN = uv run honcho start backend demo-frontend

dev:
	$(RUN)
	
dev-tunnel:
	$(RUN) tunnel

db-start:
	docker compose up database -d
	@until docker compose exec database pg_isready -U postgres; do sleep 0.5; done

db-sh:
	@docker compose exec database psql -U postgres -d vitapp

db-stop:
	docker compose down database

db-drop: db-stop
	docker volume rm -f unnamed-budget-app_pgdata > /dev/null || true
	@echo "database container stopped, volume deleted"