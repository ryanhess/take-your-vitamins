.PHONY: dev

RUN = uv run honcho start backend demo-frontend

dev:
	$(RUN)
	
dev-tunnel:
	$(RUN) tunnel