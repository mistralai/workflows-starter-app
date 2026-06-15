from __future__ import annotations

from unittest.mock import patch

import pytest
from click.testing import CliRunner

from mistral_workflows_cli.main import cli
from mistral_workflows_cli.setup import run_setup


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


def test_cli_has_setup_command(runner: CliRunner) -> None:
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "setup" in result.output


def test_setup_fails_without_api_key(tmp_path: object, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("MISTRAL_API_KEY", raising=False)
    with patch("mistral_workflows_cli.setup.Prompt.ask", return_value=""):
        with pytest.raises(SystemExit) as exc_info:
            run_setup(api_key=None, output_dir=str(tmp_path), project_name="test-proj")
        assert exc_info.value.code == 1


def test_setup_uses_env_api_key_without_prompt(tmp_path: object, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("MISTRAL_API_KEY", "sk-from-env")

    with patch("mistral_workflows_cli.setup.Prompt.ask") as prompt_ask:
        with patch("copier.run_copy") as run_copy:
            run_setup(api_key=None, output_dir=str(tmp_path), project_name="test-proj")

    prompt_ask.assert_not_called()
    run_copy.assert_called_once()
    assert run_copy.call_args.kwargs["data"]["mistral_api_key"] == "sk-from-env"


def test_setup_prefers_explicit_api_key_over_env(tmp_path: object, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("MISTRAL_API_KEY", "sk-from-env")

    with patch("copier.run_copy") as run_copy:
        run_setup(api_key="sk-explicit", output_dir=str(tmp_path), project_name="test-proj")

    run_copy.assert_called_once()
    assert run_copy.call_args.kwargs["data"]["mistral_api_key"] == "sk-explicit"


def test_setup_strips_whitespace_only_env_api_key(tmp_path: object, monkeypatch: pytest.MonkeyPatch) -> None:
    """Whitespace-only MISTRAL_API_KEY should not bypass the prompt."""
    monkeypatch.setenv("MISTRAL_API_KEY", "   ")
    with patch("mistral_workflows_cli.setup.Prompt.ask", return_value=""):
        with pytest.raises(SystemExit) as exc_info:
            run_setup(api_key=None, output_dir=str(tmp_path), project_name="test-proj")
        assert exc_info.value.code == 1


def test_setup_fails_if_dir_exists(tmp_path: object) -> None:
    import pathlib

    (pathlib.Path(str(tmp_path)) / "existing").mkdir()
    with pytest.raises(SystemExit) as exc_info:
        run_setup(api_key="sk-test", output_dir=str(tmp_path), project_name="existing")
    assert exc_info.value.code == 1
