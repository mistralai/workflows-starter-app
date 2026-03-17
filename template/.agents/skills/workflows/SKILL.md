--- 
name: workflows
description: Framework for building durable workflows with orchestrated activities, used for background jobs, multi-step pipelines, scheduled tasks, LLM agents, or any process requiring fault tolerance, retries, and long-running execution. This skill provides comprehensive documentation and guidance for working with the Mistral Workflows framework.
license: Complete terms in LICENSE.txt
---

# Workflows Documentation

This skill provides comprehensive documentation and guidance for the Mistral Workflows framework, which is designed for building durable, fault-tolerant workflows with orchestrated activities.

## About Workflows

Mistral Workflows is an orchestration control plane that accelerates the development and reliable execution of complex, AI-driven workflows. Built on Temporal for fault-tolerant workflow execution, it combines a user-friendly API with a rich Python framework optimized for Mistral's AI services.

## Documentation Structure

The documentation is organized into several categories:

### Getting Started

- **[Introduction](references/getting-started/introduction.mdx)**: Overview of Mistral Workflows and its core architecture
- **[Installation](references/getting-started/installation.mdx)**: Guide to installing and setting up the Workflows framework
- **[Core Concepts](references/getting-started/core-concepts.mdx)**: Explanation of workflows, activities, and workers
- **[Python SDK](references/getting-started/python-sdk.mdx)**: Documentation for the Python SDK and client library
- **[Your First Workflow](references/getting-started/your-first-workflow.mdx)**: Step-by-step guide to creating your first workflow
- **[Useful Links](references/getting-started/useful-links.mdx)**: Collection of helpful resources and references

### Guides

- **[Workflows](references/guides/workflows.mdx)**: Detailed guide on creating and managing workflows
- **[Activities](references/guides/activities.mdx)**: Comprehensive documentation on activities and their implementation
- **[Concurrency](references/guides/concurrency.mdx)**: Guide to handling concurrent workflow execution
- **[Dependency Injection](references/guides/dependency-injection.mdx)**: Explanation of dependency injection patterns
- **[Durable Agents](references/guides/durable-agents.mdx)**: Documentation on building durable AI agents
- **[Handling Large Data](references/guides/handling-large-data.mdx)**: Strategies for working with large datasets
- **[Limitations](references/guides/limitations.mdx)**: Known limitations and constraints of the framework
- **[Local Execution](references/guides/local-execution.mdx)**: Guide to running workflows locally for development
- **[Observability](references/guides/observability.mdx)**: Documentation on monitoring and observability features
- **[Scheduling](references/guides/scheduling.mdx)**: Guide to scheduling workflows and tasks
- **[Signals, Queries, and Updates](references/guides/signals-queries-updates.mdx)**: Documentation on workflow communication patterns
- **[Streaming](references/guides/streaming.mdx)**: Guide to streaming data in workflows
- **[Streaming Consumption](references/guides/streaming-consumption.mdx)**: Documentation on consuming streaming data
- **[Workflows Exception Handling](references/guides/workflows-exception.mdx)**: Guide to exception handling in workflows
- **[Workflows Plugins](references/guides/workflows-plugins.mdx)**: Documentation on extending workflows with plugins
- **[Deployment Patterns](references/guides/_deployment-patterns.mdx)**: Best practices for deploying workflows
- **[Execution IDs](references/execution_ids.md)**: Generate deterministic execution IDs for child workflows
- **[Pipeline Pattern](references/pipeline_pattern.md)**: Build multi-step workflows with declarative step definitions
- **[Progress Decorator](references/progress_decorator.md)**: Track workflow step progress with automatic event recording
- **[Workflow Testing](references/workflow_testing.md)**: Ensure workflow classes are properly registered in workers

### Appendices

- **[Payload Encoding](references/appendices/payload-encoding.mdx)**: Technical details on payload encoding
- **[Streaming](references/appendices/streaming.mdx)**: Additional information on streaming capabilities
- **[Worker Versioning](references/appendices/worker-versioning.mdx)**: Guide to worker versioning and compatibility

### Additional Resources

- **[Cookbooks](references/cookbooks/index.mdx)**: Collection of practical examples and recipes
- **[Contributing](references/guides/contributing.mdx)**: Guide to contributing to the Workflows project
- **[Documentation Structure](references/documentation-structure.mdx)**: Overview of the documentation organization
- **[Robots](references/robots.mdx)**: Information about robots.txt and web crawling policies

## When to Use This Skill

Use this skill when you need to:

1. **Build durable workflows**: Create long-running, fault-tolerant processes
2. **Orchestrate activities**: Coordinate multiple tasks and operations
3. **Handle background jobs**: Manage asynchronous processing and task queues
4. **Create multi-step pipelines**: Build complex workflows with multiple stages
5. **Schedule tasks**: Set up recurring or delayed execution of workflows
6. **Develop LLM agents**: Build AI agents that require persistent state and reliability
7. **Ensure fault tolerance**: Implement systems that can recover from failures automatically

## Key Features

- **Fault tolerance**: Automatic recovery from failures and retries
- **Durable execution**: Workflows can run for extended periods (seconds to years)
- **Deterministic behavior**: Consistent execution regardless of infrastructure failures
- **Rich Python framework**: Easy-to-use decorators and APIs
- **Built-in observability**: Deep integration with OpenTelemetry for monitoring
- **Scalability**: Designed to handle complex, distributed applications

## Usage Patterns

The Workflows framework is particularly well-suited for:

- **AI-driven workflows**: Orchestrating complex AI processes
- **Data processing pipelines**: Managing multi-stage data transformation
- **Background job processing**: Handling asynchronous task execution
- **Scheduled maintenance tasks**: Running periodic system operations
- **Long-running business processes**: Managing workflows that span extended time periods
- **Microservices coordination**: Orchestrating interactions between multiple services