# workflows-starter-app

Copier template **and** the `mistralai-workflows-cli` that scaffolds from it.
Both live in this repo so template and CLI changes ship in a single PR.

- `src/mistral_workflows_cli/` — the `uvx mistralai-workflows-cli` CLI
- `src/mistral_workflows_cli/_template/` — the copier template (`copier.yml` + `template/`) it scaffolds from

## Usage

```bash
uvx mistralai-workflows-cli setup
```


## Template Structure

```
src/mistral_workflows_cli/_template/template/
├── .env.jinja                          # MISTRAL_API_KEY injection
├── .gitignore
├── pyproject.toml.jinja                # Project config with SDK dependency
├── README.md.jinja
├── Makefile                            # start-worker & execute commands
├── .agents/skills/workflows/SKILL.md   # Vibe skill for creating workflows
└── src/
    ├── discover.py             # Auto-discovers workflow classes & starts worker
    └── workflows/
        ├── __init__.py
        ├── hello.py                     # Minimal example workflow
        └── start.py                    # CLI to execute a workflow by name
```

## Auto-Discovery

Workflows are auto-discovered at worker startup. Any class decorated with `@workflows.workflow.define` in `src/workflows/` is automatically registered — no manual imports needed. Just add a new file and restart the worker.

## Variables

| Variable          | Description                                                  |
| ----------------- | ------------------------------------------------------------ |
| `project_name`    | Name of the project (used in pyproject.toml, workflow names) |
| `mistral_api_key` | Mistral API key (written to `.env`, excluded from git)       |
| `deployment_name` | Deployment name used to identify the deployment in AI Studio |

## CLI Development

The CLI source lives in `src/mistral_workflows_cli/`, and the copier template it
scaffolds from lives next to it in `src/mistral_workflows_cli/_template/`. Because
the template is package data, the same path is used whether running from a source
checkout (`uv run`) or the installed wheel (`uvx`).

```bash
uv sync
uv run mistral-workflows --help
make test
```

## Publishing

Tag with `mistralai-workflows-cli/v<version>` to trigger the PyPI publish workflow.

```bash
git tag mistralai-workflows-cli/v0.1.0
git push origin mistralai-workflows-cli/v0.1.0
```
