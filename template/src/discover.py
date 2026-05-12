"""Auto-discover all workflow classes in src/workflows/ and start a worker."""
# ruff: noqa: E402

import asyncio
import importlib
import inspect
import os
import pkgutil
import sys
from dotenv import load_dotenv

DEFAULT_SERVER_URL = "https://api.mistral.ai"
SERVER_URL_ENV_VAR = "SERVER_URL"
LEGACY_SERVER_URL_ENV_VAR = "MISTRAL_SERVER_URL"


def load_project_env() -> None:
    load_dotenv(override=True)

    if os.environ.get(SERVER_URL_ENV_VAR):
        return

    legacy_server_url = os.environ.get(LEGACY_SERVER_URL_ENV_VAR)
    if not legacy_server_url:
        return

    os.environ[SERVER_URL_ENV_VAR] = legacy_server_url
    print(
        "Warning: MISTRAL_SERVER_URL is deprecated. Rename it to SERVER_URL.",
        file=sys.stderr,
    )


load_project_env()

import mistralai.workflows as workflows
from mistralai.workflows.core.definition.workflow_definition import (
    get_workflow_definition,
)


def discover_workflows() -> list[type]:
    """Scan the workflows package and return all workflow classes."""
    discovered = []
    package = importlib.import_module("workflows")

    for _, modname, ispkg in pkgutil.iter_modules(
        package.__path__, prefix="workflows."
    ):
        if ispkg:
            continue
        module = importlib.import_module(modname)
        for _, obj in inspect.getmembers(module, inspect.isclass):
            if hasattr(obj, "__workflows_workflow_def"):
                discovered.append(obj)

    return discovered


async def main() -> None:
    discovered = discover_workflows()

    if not discovered:
        print("No workflows discovered in src/workflows/")
        sys.exit(1)

    names = [get_workflow_definition(wf).name for wf in discovered]
    print(f"Discovered {len(discovered)} workflow(s): {', '.join(names)}")

    await workflows.run_worker(discovered)


if __name__ == "__main__":
    asyncio.run(main())
