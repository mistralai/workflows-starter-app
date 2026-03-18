.PHONY: register start installdeps

## Install dependencies
installdeps:
	uv sync

## Discover all workflows and start the worker
register:
	TEMPORAL_TASK_QUEUE=$$(hostname) uv run python src/discover.py

## Trigger a workflow execution
## Usage: make start path=src/workflows/start.py input='{"name": "World"}'
start:
	uv run python $(or $(path),src/workflows/start.py) $(input)
