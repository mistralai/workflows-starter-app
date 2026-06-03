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

## Prerequisites

This workflow uses the Linear Connector with [on-behalf-of (OBO)](https://docs.mistral.ai/studio-api/workflows/building-workflows/on_behalf_of) mode, which requires a [hardened deployment](https://docs.mistral.ai/studio-api/workflows/managing-workflows-in-production/hardened_deployments). Complete these steps before running the workflow.

### 1. Create the Linear Connector

1. Open [Studio › Context › Connectors](https://console.mistral.ai/build/connectors).
2. Click **+ Add connector** and select **Linear**.
3. Give it a name (e.g. `linear`) — this must match the connector name referenced in the workflow code.

### 2. Add your Linear credentials

1. Open the connector you just created and switch to the **Credentials** tab.
2. Click **+ Add credentials**, give it a name, and follow the auth flow.
3. Mark it as the default credential so it is used automatically when no specific credential name is provided.

> **Tip**: You can also manage credentials programmatically via `client.beta.connectors`. See the [credentials docs](https://docs.mistral.ai/studio-api/workflows/building-workflows/connectors#credentials) for details.

### 3. Set up a hardened deployment

OBO workflows cannot be registered in a non-hardened deployment. Follow these steps to harden your deployment:

1. **Bootstrap the deployment**: Start the examples worker once with a non-OBO placeholder (or any existing workflow) to create the deployment entry on the platform.
2. **Harden the deployment**: In the Mistral Console, go to **Settings › Hardened Deployments**, find your deployment, and associate your API key with it.
3. **Re-register the OBO workflow**: Start the examples worker again — now the Linear summary workflow (which uses `on_behalf_of=True`) can register successfully.

> For full details on managing hardened deployments, see the [hardened deployments docs](https://docs.mistral.ai/studio-api/workflows/managing-workflows-in-production/hardened_deployments).

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
You can interactively answer the prompts in [Studio](https://console.mistral.ai/build/workflows/linear-weekly-summary).

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