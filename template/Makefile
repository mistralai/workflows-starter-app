.PHONY: start-worker execute installdeps

## Install dependencies
installdeps:
	uv sync

## Auto-discover all workflows and start the worker
start-worker:
	TEMPORAL_TASK_QUEUE=$$(hostname) uv run python src/discover.py

## Trigger a workflow execution
## Usage: make execute workflow=hello input='{"name": "World"}'
execute:
	TEMPORAL_TASK_QUEUE=$$(hostname) uv run python src/workflows/start.py $(or $(workflow),hello) $(input)
