---
name: workflows
description: Framework for building durable workflows with orchestrated activities, used for background jobs, multi-step pipelines, scheduled tasks, LLM agents, or any process requiring fault tolerance, retries, and long-running execution. This skill provides comprehensive documentation and guidance for working with the Mistral Workflows framework.
license: Complete terms in LICENSE.txt
---

# Workflows Documentation

This skill provides comprehensive documentation and guidance for the Mistral Workflows framework, which is designed for building durable, fault-tolerant workflows with orchestrated activities.

## About Workflows

Mistral Workflows is a durable-execution orchestration platform that accelerates the development and reliable execution of complex, AI-driven workflows. It combines a user-friendly API with a rich Python framework (`mistralai.workflows`) optimized for Mistral's AI services, providing fault-tolerant execution, automatic retries, and durable state that survives crashes — from simple sequences to long-running, stateful processes (seconds to years).

## SDK Version and Imports

This skill targets the **`mistralai-workflows` SDK v3.4.0 and higher**:

```bash
uv add "mistralai-workflows>=3.4.0,<4.0.0"
```

**Canonical import style** used throughout this skill:

```python
import mistralai.workflows as workflows

@workflows.workflow.define(name="my_workflow")
class MyWorkflow:
    @workflows.workflow.entrypoint
    async def run(self, data: str) -> str:
        ...
```

Focused snippets may use `from mistralai.workflows import workflow, activity, ...` instead.

**Always use the SDK; never import `temporalio` directly.** The SDK re-exports everything user code needs so workflows stay portable and deterministic:

- `workflow.now()`, `workflow.uuid4()`, `workflow.random()` — deterministic replacements for `datetime.now()`, `uuid.uuid4()`, `random` inside workflows
- `workflow.wait_condition()`, `workflow.continue_as_new()`, `workflow.execute_workflow()`
- `workflow.unsafe.imports_passed_through()` / `workflow.unsafe.skip_determinism_enforcement()` — sandbox escape hatches
- `activity_heartbeat()` — heartbeat from inside an activity
- `WorkflowError`, `ActivityError`, `ParentClosePolicy` — all from `mistralai.workflows`

Call activities directly (`await my_activity(args)`); timeouts and retries live on the `@activity(...)` decorator, not at the call site.

## Documentation Structure

The documentation is organized into several categories:

### Getting Started

- **[Introduction](references/getting-started/introduction.mdx)**: Overview of Mistral Workflows and its core architecture
- **[Installation](references/getting-started/installation.mdx)**: Guide to installing and setting up the Workflows framework (CLI scaffolding, optional deps)
- **[Core Concepts](references/getting-started/core-concepts.mdx)**: Workflows, activities, workers, executions vs runs
- **[Python SDK](references/getting-started/python-sdk.mdx)**: Programmatic API via the `mistralai` client (`client.workflows.*`)
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
- **[Streaming Consumption](references/guides/streaming-consumption.mdx)**: `client.workflows.events.get_stream_events_async()`, NATS subjects, SSE API
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
- **[Migration v2 to v3](references/guides/migration-v2-to-v3.mdx)**: Breaking changes and upgrade steps from SDK v2 through v3.4.0

### Testing

- **[Testing Workflows](references/guides/testing.md)**: Integration testing with `create_test_worker`, hang prevention, sandbox pitfalls
- **[Diagnostics](references/guides/diagnostics.md)**: Run `wf-diagnose` locally or on Kubernetes to collect a diagnostic report for support triage

**Quick-test script** — run any workflow in a local test environment with zero setup:
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
- **[Workflow Testing](references/workflow_testing.md)**: Ensure workflow classes are properly registered in workers

## When to Use This Skill

Use this skill when you need to:

1. **Build durable workflows**: Create long-running, fault-tolerant processes
2. **Orchestrate activities**: Coordinate multiple tasks and operations
3. **Handle background jobs**: Manage asynchronous processing and task queues
4. **Create multi-step pipelines**: Build complex workflows with multiple stages
5. **Schedule tasks**: Set up recurring or delayed execution of workflows
6. **Develop LLM agents**: Build durable AI agents with MCP tool support
7. **Build conversational workflows**: Create interactive workflows with HITL, forms, canvas, and rich UI
8. **Ensure fault tolerance**: Implement systems that can recover from failures automatically
9. **Stream events**: Real-time token streaming and progress updates via NATS

## Key Features

- **Fault tolerance**: Automatic recovery from failures and retries
- **Durable execution**: Workflows can run for extended periods (seconds to years)
- **Determinism enforcement**: Sandbox-based determinism, enabled by default (opt out per-workflow with `enforce_determinism=False`)
- **Rich Python framework**: Easy-to-use decorators and APIs (`mistralai.workflows`)
- **Built-in observability**: Deep integration with OpenTelemetry for monitoring
- **Streaming**: NATS-backed real-time token and progress streaming
- **Rate limiting**: Distributed rate limiting shared across workers
- **Dependency injection**: FastAPI-style Depends() pattern
- **Large payload handling**: OffloadableField with S3/Azure/GCS blob storage
- **Conversational workflows**: Interactive workflows with Vibe integration, forms, canvas, and rich UI components
- **Durable agents**: AI agents with MCP support, multi-agent handoffs, and persistent state
- **Scalability**: Designed to handle complex, distributed applications

