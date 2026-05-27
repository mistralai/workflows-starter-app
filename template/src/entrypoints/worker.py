"""Auto-discover all workflow classes in the `workflows` package and start a worker."""
# ruff: noqa: E402

import asyncio
import importlib
from dotenv import load_dotenv

import inspect
import pkgutil
import sys

load_dotenv(override=True)

import mistralai.workflows as mistralai_workflows
from mistralai.workflows.core.definition.workflow_definition import (
    get_workflow_definition,
)


def discover_workflows() -> list[type]:
    """Scan the `workflows` package and return all workflow classes.

    Only classes *defined* in the scanned module are collected. Without
    this filter, a workflow class imported from a sibling module (for
    example a parent workflow importing a child workflow to call via
    ``execute_workflow``) would be picked up twice and trip Temporal's
    "More than one workflow named X" check at worker startup.
    """
    discovered: list[type] = []
    seen: set[type] = set()
    package = importlib.import_module("workflows")

    for _, modname, ispkg in pkgutil.iter_modules(
        package.__path__, prefix="workflows."
    ):
        if ispkg:
            continue
        module = importlib.import_module(modname)
        for _, obj in inspect.getmembers(module, inspect.isclass):
            if not hasattr(obj, "__workflows_workflow_def"):
                continue
            if obj.__module__ != modname:
                continue  # re-export of a workflow defined elsewhere
            if obj in seen:
                continue
            seen.add(obj)
            discovered.append(obj)

    return discovered


async def main() -> None:
    discovered = discover_workflows()

    if not discovered:
        print("No workflows discovered in the `workflows` package.")
        sys.exit(1)

    names = [get_workflow_definition(wf).name for wf in discovered]
    print(f"Discovered {len(discovered)} workflow(s): {', '.join(names)}")

    await mistralai_workflows.run_worker(discovered)


if __name__ == "__main__":
    asyncio.run(main())
