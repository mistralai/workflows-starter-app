import os
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import env_config


@pytest.fixture(autouse=True)
def clear_env(monkeypatch):
    monkeypatch.delenv("SERVER_URL", raising=False)
    monkeypatch.delenv("MISTRAL_SERVER_URL", raising=False)
    monkeypatch.setattr(env_config, "load_dotenv", lambda **_: None)


def test_load_project_env_prefers_server_url(monkeypatch, capsys):
    monkeypatch.setenv("SERVER_URL", "https://preferred.example")
    monkeypatch.setenv("MISTRAL_SERVER_URL", "https://legacy.example")

    env_config.load_project_env()

    assert env_config.get_server_url() == "https://preferred.example"
    assert capsys.readouterr().err == ""


def test_load_project_env_accepts_legacy_server_url(monkeypatch, capsys):
    monkeypatch.setenv("MISTRAL_SERVER_URL", "https://legacy.example")

    env_config.load_project_env()

    assert env_config.get_server_url() == "https://legacy.example"
    assert os.environ["SERVER_URL"] == "https://legacy.example"
    assert "MISTRAL_SERVER_URL is deprecated" in capsys.readouterr().err
