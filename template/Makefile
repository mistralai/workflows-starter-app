.PHONY: register start installdeps

## Install dependencies
installdeps:
	uv sync

## Register a workflow and start its worker
## Usage: make register path=src/workflows/hello.py
register:
	uv run python $(or $(path),src/workflows/hello.py)

## Trigger a workflow execution
## Usage: make start path=src/workflows/start.py input='{"name": "World"}'
start:
	uv run python $(or $(path),src/workflows/start.py) $(input)
