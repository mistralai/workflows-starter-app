"""Trigger a workflow execution from the command line."""

import asyncio
import json
import os
import sys

from dotenv import load_dotenv

load_dotenv(override=True)

from pydantic import create_model

from mistralai_workflows.client import WorkflowsClient


async def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python src/workflows/start.py <workflow-name> [input-json]")
        raise SystemExit(1)

    workflow_name = sys.argv[1]
    raw_input = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {"name": "World"}
    DynamicModel = create_model(
        "Input", **{k: (type(v), v) for k, v in raw_input.items()}
    )
    input_data = DynamicModel(**raw_input)

    api_key = os.environ.get("MISTRAL_API_KEY", "")
    if not api_key:
        print("Error: MISTRAL_API_KEY is not set. Check your .env file.")
        raise SystemExit(1)

    client = WorkflowsClient(
        api_key=api_key, base_url=os.environ.get("SERVER_URL", "https://api.mistral.ai")
    )

    result = await client.execute_workflow_and_wait(
        workflow_name,
        input_data=input_data,
    )
    print(f"Result: {result}")


if __name__ == "__main__":
    asyncio.run(main())
