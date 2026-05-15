---
name: workflows
description: "Scaffold, configure, and debug Mistral Workflows — durable workflow definitions, activity handlers, retry policies, scheduling, streaming, and durable AI agents. Use when the user asks about Mistral Workflows, durable execution, task orchestration, job queues, workflow pipelines, activity retries, workflow signals/queries, or the mistralai.workflows Python SDK."
license: Complete terms in LICENSE.txt
---

# Mistral Workflows

Scaffold workflow definitions, configure activity handlers and retry policies, set up scheduling, streaming, and durable AI agents using the `mistralai.workflows` Python SDK.

## Quick Start

Minimal workflow with one activity:

```python
import mistralai.workflows as workflows

@workflows.activity()
async def hello_world(name: str) -> dict:
    return {"message": f"Hello, {name}!"}

@workflows.workflow.define(name="simple_example_workflow")
class SimpleExampleWorkflow:
    @workflows.workflow.entrypoint
    async def run(self, name: str) -> dict:
        return await hello_world(name)

async def main() -> None:
    await workflows.run_worker([SimpleExampleWorkflow])
```

Run with `uv run python my_workflow.py`, then trigger from [AI Studio](https://console.mistral.ai/build/workflows).

## Reference Documentation

### Getting Started

- **[Introduction](references/getting-started/introduction.mdx)**: Overview of Mistral Workflows and its core architecture
- **[Installation](references/getting-started/installation.mdx)**: Guide to installing and setting up the Workflows framework (CLI scaffolding, optional deps)
- **[Core Concepts](references/getting-started/core-concepts.mdx)**: Workflows, activities, workers, executions vs runs
- **[Python SDK](references/getting-started/python-sdk.mdx)**: Documentation for the Python SDK and WorkflowsClient
- **[Your First Workflow](references/getting-started/your-first-workflow.mdx)**: Step-by-step guide to creating your first workflow

### Guides

- **[Workflows](references/guides/workflows.mdx)**: Creating workflows, determinism enforcement (sandbox), input types, timeouts, signals/queries/updates, child workflows, continue-as-new
- **[Activities](references/guides/activities.mdx)**: Timeouts, retries, heartbeats, local activities, sticky sessions, nested activities
- **[Workflows Exception Handling](references/guides/workflows-exception.mdx)**: WorkflowsException, ErrorCode enum, factory methods
- **[Error Codes](references/guides/error-codes.mdx)**: API error codes WF_1000-WF_1600 with HTTP status, description, and resolution
- **[Signals, Queries, and Updates](references/guides/signals-queries-updates.mdx)**: Workflow communication patterns with input validation
- **[Scheduling](references/guides/scheduling.mdx)**: Cron expressions, ScheduleDefinition, SchedulePolicy, overlap handling
- **[Dependency Injection](references/guides/dependency-injection.mdx)**: FastAPI-style Depends() pattern
- **[Streaming](references/guides/streaming.mdx)**: Task API, token streaming, progress updates
- **[Streaming Consumption](references/guides/streaming-consumption.mdx)**: WorkflowsClient.stream_events(), NATS subjects, SSE API
- **[Concurrency](references/guides/concurrency.mdx)**: execute_activities_in_parallel() with List/Chain/Offset executors
- **[Rate Limiting](references/guides/rate-limiting.mdx)**: Distributed rate limiting across workers
- **[Handling Large Data](references/guides/handling-large-data.mdx)**: OffloadableField, blob storage (S3/Azure/GCS)
- **[Payload Encoding](references/guides/payload-encoding.mdx)**: Payload offloading, AES-GCM encryption, key rotation
- **[Observability](references/guides/observability.mdx)**: OpenTelemetry traces, trace sampling
- **[Durable Agents](references/guides/durable-agents.mdx)**: Agent, Runner, RemoteSession/LocalSession, MCP, multi-agent handoffs
- **[Conversational Workflows](references/guides/assist-workflows.mdx)**: InteractiveWorkflow, HITL, ChatInput/FormInput, Canvas editing, Rich UI components, Tool UI states
- **[Local Execution](references/guides/local-execution.mdx)**: No-infra dev mode with Pydantic model params
- **[Limitations](references/guides/limitations.mdx)**: System constraints and limits
- **[Workflows Plugins](references/guides/workflows-plugins.mdx)**: Mistral AI plugin, Webhook plugin, Nuage plugin, custom plugins
- **[Deployment Patterns](references/guides/_deployment-patterns.mdx)**: Best practices for deploying workflows
- **[Migration v2 to v3](references/guides/migration-v2-to-v3.mdx)**: Breaking changes and upgrade steps from SDK v2 to v3

### Testing

- **[Testing Workflows](references/guides/testing.md)**: Integration testing with `create_test_worker`, hang prevention, sandbox pitfalls

**Quick-test script** — run any workflow in a local Temporal test environment with zero setup:
```bash
python .agents/skills/workflows/scripts/test_workflow.py <workflow_file> --input '{"key": "value"}' [--timeout 30]
```

**Timeout policy for testing:** Use aggressive (short) timeouts to keep the feedback loop tight. A hanging test wastes more time than a false timeout. Defaults:

| Context | Recommended timeout | When to increase |
|---|---|---|
| `--timeout` (quick-test script) | `15` seconds | Workflow makes multiple LLM calls or heavy I/O |
| `execution_timeout` (pytest) | `timedelta(seconds=10)` | Known long-running workflow |
| `asyncio.wait_for` (pytest) | `15` seconds | Should always be slightly above `execution_timeout` |

If a workflow is known to be long-running (e.g. multi-step agent, large data processing), increase timeouts proportionally — but start short and only raise them when you see legitimate timeout failures, not preemptively.

### Internal References

These are additional patterns and utilities not covered in the official docs:

- **[Execution IDs](references/execution_ids.md)**: Generate deterministic execution IDs for child workflows
- **[Pipeline Pattern](references/pipeline_pattern.md)**: Build multi-step workflows with declarative StepSpec definitions
- **[Progress Decorator](references/progress_decorator.md)**: Track workflow step progress with automatic event recording
- **[Workflow Testing](references/workflow_testing.md)**: Ensure workflow classes are properly registered in workers
