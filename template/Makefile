.PHONY: start-worker execute installdeps

## Install dependencies
installdeps:
	uv sync

## Auto-discover all workflows and start the worker (with file-watch auto-reload)
start-worker:
	uv run python src/dev_worker.py

## Trigger a workflow execution
## Usage: make execute workflow=hello-world input='{"name": "World"}'
execute:
	uv run python src/workflows/start.py $(if $(workflow),--workflow $(workflow),) $(if $(input),--input '$(input)',)
