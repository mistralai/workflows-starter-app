"""Trigger a workflow execution from the command line."""

import asyncio
import json
import os
import sys

from dotenv import load_dotenv

from pydantic import create_model

from mistralai.workflows.client import get_mistral_client

load_dotenv(override=True)


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

    client = get_mistral_client(
        api_key=api_key, server_url=os.environ.get("SERVER_URL", "https://api.mistral.ai")
    )

    result = await client.workflows.execute_workflow_and_wait_async(
        workflow_identifier=workflow_name,
        input=input_data.model_dump(mode="json"),
        task_queue=os.environ.get("DEPLOYMENT_NAME", "default"),
    )
    print(f"Result: {result}")


if __name__ == "__main__":
    asyncio.run(main())
