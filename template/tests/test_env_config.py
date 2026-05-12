import os
import sys
from pathlib import Path
from types import ModuleType

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))


@pytest.fixture(autouse=True)
def clear_env(monkeypatch):
    monkeypatch.delenv("SERVER_URL", raising=False)
    monkeypatch.delenv("MISTRAL_SERVER_URL", raising=False)
    monkeypatch.setattr("dotenv.load_dotenv", lambda **_: None)


@pytest.fixture()
def start_module(monkeypatch):
    fake_extra = ModuleType("mistralai.extra.workflows")
    fake_extra.WorkflowEncodingConfig = object
    fake_extra.configure_workflow_encoding = lambda *args, **kwargs: None
    fake_client = ModuleType("mistralai.workflows.client")
    fake_client.get_mistral_client = lambda **kwargs: kwargs

    monkeypatch.setitem(sys.modules, "mistralai.extra.workflows", fake_extra)
    monkeypatch.setitem(sys.modules, "mistralai.workflows.client", fake_client)

    import workflows.start as start

    return start


def test_load_project_env_prefers_server_url(monkeypatch, capsys, start_module):
    monkeypatch.setenv("SERVER_URL", "https://preferred.example")
    monkeypatch.setenv("MISTRAL_SERVER_URL", "https://legacy.example")

    start_module.load_project_env()

    assert start_module.get_server_url() == "https://preferred.example"
    assert capsys.readouterr().err == ""


def test_load_project_env_accepts_legacy_server_url(monkeypatch, capsys, start_module):
    monkeypatch.setenv("MISTRAL_SERVER_URL", "https://legacy.example")

    start_module.load_project_env()

    assert start_module.get_server_url() == "https://legacy.example"
    assert os.environ["SERVER_URL"] == "https://legacy.example"
    assert "MISTRAL_SERVER_URL is deprecated" in capsys.readouterr().err
