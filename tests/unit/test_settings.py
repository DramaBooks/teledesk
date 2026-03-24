from pathlib import Path

from teledesk.config.settings import bootstrap_environment, load_env_file, resolve_tdlib_root
from teledesk.config.settings import AppSettings


def test_load_env_file_populates_missing_values(tmp_path: Path, monkeypatch) -> None:
    env_file = tmp_path / ".env"
    env_file.write_text("TELEDESK_GITHUB_OWNER=DramaBooks\nTELEDESK_TDLIB_ROOT=vendor/tdlib\n", encoding="utf-8")
    monkeypatch.delenv("TELEDESK_GITHUB_OWNER", raising=False)

    loaded = load_env_file(env_file)

    assert loaded is True
    assert __import__("os").environ["TELEDESK_GITHUB_OWNER"] == "DramaBooks"


def test_bootstrap_environment_returns_project_root(tmp_path: Path, monkeypatch) -> None:
    (tmp_path / "pyproject.toml").write_text("[project]\nname='demo'\n", encoding="utf-8")
    (tmp_path / ".env").write_text("TELEDESK_GITHUB_REPO=teledesk\n", encoding="utf-8")
    monkeypatch.chdir(tmp_path)

    project_root = bootstrap_environment(tmp_path)

    assert project_root == tmp_path


def test_resolve_tdlib_root_uses_project_root_for_relative_path(tmp_path: Path) -> None:
    settings = AppSettings(tdlib_root="vendor/tdlib")

    resolved = resolve_tdlib_root(settings, project_root=tmp_path)

    assert resolved == tmp_path / "vendor/tdlib"
