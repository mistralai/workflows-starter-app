"""Environment helpers for the starter Workflows app."""

import os
import sys

from dotenv import load_dotenv

DEFAULT_SERVER_URL = "https://api.mistral.ai"
SERVER_URL_ENV_VAR = "SERVER_URL"
LEGACY_SERVER_URL_ENV_VAR = "MISTRAL_SERVER_URL"


def load_project_env() -> None:
    """Load `.env` and normalize legacy variable names."""
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


def get_server_url() -> str:
    return os.environ.get(SERVER_URL_ENV_VAR, DEFAULT_SERVER_URL)
