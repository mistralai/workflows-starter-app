# workflows-starter-app

Copier template for bootstrapping Mistral Workflows projects.

## Usage

This template is used by the `mistralai-workflows-cli` CLI:

```bash
uvx mistralai-workflows-cli setup
```

Or directly with copier:

```bash
copier copy gh:mistralai/workflows-starter-app my-project
```

## Template Structure

```
template/
├── .env.jinja                          # MISTRAL_API_KEY injection
├── .gitignore
├── pyproject.toml.jinja                # Project config with SDK dependency
├── README.md.jinja
├── .agents/skills/workflows/SKILL.md   # Vibe skill for creating workflows
└── src/workflows/
    ├── __init__.py
    └── hello.py.jinja                  # Minimal example workflow
```

## Variables

| Variable | Description |
|---|---|
| `project_name` | Name of the project (used in pyproject.toml, workflow names) |
| `mistral_api_key` | Mistral API key (written to `.env`, excluded from git) |

