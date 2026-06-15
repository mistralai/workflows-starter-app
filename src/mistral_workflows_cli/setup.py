from __future__ import annotations

import os
import socket
from pathlib import Path

from rich.console import Console
from rich.prompt import Prompt

TEMPLATE_URL = "gh:mistralai/workflows-starter-app"
API_KEYS_URL = "https://console.mistral.ai/api-keys"


def run_setup(
    api_key: str | None,
    output_dir: str,
    project_name: str | None,
) -> None:
    console = Console()

    console.print("\n[bold]Mistral Workflows — Project Setup[/bold]\n")

    # 1. Project name
    if not project_name:
        project_name = Prompt.ask("Project name", default="my-workflow")

    # 2. API key
    if not api_key:
        api_key = os.getenv("MISTRAL_API_KEY", "").strip() or None
        if api_key:
            console.print("API key was fetched from existing env variable `MISTRAL_API_KEY`")

    if not api_key:
        console.print(f"Create an API key at: [link={API_KEYS_URL}]{API_KEYS_URL}[/link]\n")
        api_key = Prompt.ask("Paste your Mistral API key")
    if api_key:
        console.print("The provided API key will be stored in the generated `.env`")
    if not api_key:
        console.print("[bold red]No API key provided. Aborting.[/bold red]")
        raise SystemExit(1)

    # 3. Clone template via copier
    dest = Path(output_dir) / project_name

    if dest.exists():
        console.print(f"[bold red]Directory already exists: {dest}[/bold red]")
        raise SystemExit(1)

    console.print(f"\nScaffolding project into [bold]{dest}[/bold] ...\n")

    try:
        import copier
    except ImportError:
        console.print("[bold red]copier is not installed. Run: pip install copier[/bold red]")
        raise SystemExit(1)

    copier.run_copy(
        TEMPLATE_URL,
        str(dest),
        data={
            "project_name": project_name,
            "mistral_api_key": api_key,
            "deployment_name": socket.gethostname(),
        },
        unsafe=True,
    )

    # 4. Success
    console.print(f"\n[bold green]Project created at {dest}[/bold green]\n")
    console.print("Get started:\n")
    console.print(f"  cd {project_name}")
    console.print("  vibe\n")
