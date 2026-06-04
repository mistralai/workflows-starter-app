"""Minimal example workflow — edit this file or create new ones."""

import mistralai.workflows as workflows
from pydantic import BaseModel


class HelloInput(BaseModel):
    name: str = "World"


@workflows.activity()
async def greet(name: str) -> str:
    """A simple activity that returns a greeting."""
    return f"Hello, {name}! Hello from mono repo"


@workflows.workflow.define(
    name="hello-world",
    workflow_display_name="Hello World",
    workflow_description="A minimal hello-world workflow.",
)
class HelloWorkflow:
    @workflows.workflow.entrypoint
    async def run(self, input: HelloInput) -> str:
        return await greet(input.name)
