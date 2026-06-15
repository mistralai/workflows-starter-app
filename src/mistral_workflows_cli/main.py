import click

from mistral_workflows_cli._version import __version__


@click.group()
@click.version_option(version=__version__)
def cli() -> None:
    """Mistral Workflows CLI — bootstrap and manage workflow projects."""


@cli.command()
@click.option("--api-key", default=None, help="Mistral API key.")
@click.option("--output-dir", "-o", default=".", help="Parent directory for the new project.")
@click.option("--project-name", "-n", default=None, help="Project name (also used as directory name).")
def setup(api_key: str | None, output_dir: str, project_name: str | None) -> None:
    """Bootstrap a new Mistral Workflows project."""
    from mistral_workflows_cli.setup import run_setup

    run_setup(api_key=api_key, output_dir=output_dir, project_name=project_name)
