# Linear Weekly Summary Workflow

## Use case

The Linear Weekly Summary workflow automates the process of generating concise, actionable summaries of recent activity in Linear projects. This workflow is ideal for teams that want to stay informed about progress, blockers, and key updates without manually reviewing every issue.

## Workflow primitives demonstrated

| Primitive | How it's used |
|---|---|
| Dynamic input handling | Accepts team/project names or IDs and resolves them dynamically |
| Parallel activities | Fetches recent issues and generates summaries concurrently |
| HITL (Human-in-the-Loop) fallback | Requests clarification if team/project resolution fails |
| Structured output | Summaries are returned as structured JSON for easy integration |
| Observability | AI Studio tracks each step, including API calls and retries |

> **Model**: All LLM calls use `mistral-chat-latest`.

## How to run

### 1. Start the examples worker

```bash
make start-examples
```

### 2. Trigger an execution (separate terminal)

```bash
make execute-linear-summary
```

This workflow expects a team name or ID and team project or ID as input.
When no input is provided, the workflow pauses and waits for user input.
You can interactively answer the prompts in [AI Studio](https://console.mistral.ai/build/workflows/linear-weekly-summary).

Alternatively, you can provide input via the command line:

```bash
make execute-linear-summary \
  input='{"team":"Engineering","project":"*"}'
```

### Run the workflow in AI Studio

1. Start the examples worker: `make start-examples`
2. Navigate to Workflows in the Mistral Console.
3. Select `linear-weekly-summary`.
4. Click **Start Workflow** and provide input such as:

```json
{
  "team": "Engineering",
  "project": "*"
}
```