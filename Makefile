.PHONY: integration-test

GENERATED_PROJECT := /tmp/starter-app-integration-test

## Generate a project from the template and run integration tests
integration-test:
	rm -rf $(GENERATED_PROJECT)
	copier copy --defaults --UNSAFE --vcs-ref=HEAD . $(GENERATED_PROJECT)
	cd $(GENERATED_PROJECT) && uv sync
	$(MAKE) _test-discover
	$(MAKE) _test-start-worker
	$(MAKE) _test-start-worker-module
	$(MAKE) _test-start-examples
	$(MAKE) _test-execute-help
	$(MAKE) _test-execute-bad-json
	@echo ""
	@echo "All integration tests passed."

_test-discover:
	@echo "--- test: workflow discovery"
	cd $(GENERATED_PROJECT) && uv run python -c \
		"from entrypoints.worker import discover_workflows; wfs = discover_workflows(); assert len(wfs) > 0, 'No workflows discovered'; print(f'OK: discovered {len(wfs)} workflow(s)')"

_test-start-worker:
	@echo "--- test: entrypoints.worker discovers workflows before connecting"
	cd $(GENERATED_PROJECT) && uv run python -m entrypoints.worker 2>&1 \
		| grep -q "Discovered .* workflow(s)" \
		&& echo "OK: worker discovered workflows" \
		|| (echo "FAIL: worker did not print discovery message" && exit 1)

_test-start-worker-module:
	@echo "--- test: python -m worker discovers workflows before connecting"
	cd $(GENERATED_PROJECT) && uv run python -m worker 2>&1 \
		| grep -q "Discovered .* workflow(s)" \
		&& echo "OK: worker module discovered workflows" \
		|| (echo "FAIL: worker module did not print discovery message" && exit 1)

_test-start-examples:
	@echo "--- test: examples.worker loads example workflows before connecting"
	cd $(GENERATED_PROJECT) && uv run python -m examples.worker 2>&1 \
		| grep -q "Starting worker with .* example(s)" \
		&& echo "OK: examples worker started" \
		|| (echo "FAIL: examples worker did not print start message" && exit 1)

_test-execute-help:
	@echo "--- test: entrypoints.start --help"
	cd $(GENERATED_PROJECT) && uv run python -m entrypoints.start --help > /dev/null 2>&1 \
		&& echo "OK: --help works" \
		|| (echo "FAIL: --help failed" && exit 1)

_test-execute-bad-json:
	@echo "--- test: entrypoints.start rejects invalid JSON"
	cd $(GENERATED_PROJECT) && uv run python -m entrypoints.start --workflow hello-world --input 'not-json' 2>&1 \
		| grep -q "invalid JSON" \
		&& echo "OK: bad JSON rejected" \
		|| (echo "FAIL: bad JSON not rejected" && exit 1)
