from pathlib import Path

from easygram.config.settings import bootstrap_environment, load_env_file, resolve_tdlib_root
from easygram.config.settings import AppSettings


def test_load_env_file_populates_missing_values(tmp_path: Path, monkeypatch) -> None:
    env_file = tmp_path / ".env"
    env_file.write_text("EASYGRAM_GITHUB_OWNER=DramaBooks\nEASYGRAM_TDLIB_ROOT=vendor/tdlib\n", encoding="utf-8")
    monkeypatch.delenv("EASYGRAM_GITHUB_OWNER", raising=False)

    loaded = load_env_file(env_file)

    assert loaded is True
    assert __import__("os").environ["EASYGRAM_GITHUB_OWNER"] == "DramaBooks"


def test_bootstrap_environment_returns_project_root(tmp_path: Path, monkeypatch) -> None:
    (tmp_path / "pyproject.toml").write_text("[project]\nname='demo'\n", encoding="utf-8")
    (tmp_path / ".env").write_text("EASYGRAM_GITHUB_REPO=easygram\n", encoding="utf-8")
    monkeypatch.chdir(tmp_path)

    project_root = bootstrap_environment(tmp_path)

    assert project_root == tmp_path


def test_app_settings_accept_legacy_env_names(monkeypatch) -> None:
    monkeypatch.delenv("EASYGRAM_GITHUB_REPO", raising=False)
    monkeypatch.setenv("TELEDESK_GITHUB_REPO", "easygram-legacy")

    settings = AppSettings()

    assert settings.github_repo == "easygram-legacy"


def test_app_settings_prefer_easygram_env_names(monkeypatch) -> None:
    monkeypatch.setenv("TELEDESK_GITHUB_REPO", "easygram-legacy")
    monkeypatch.setenv("EASYGRAM_GITHUB_REPO", "easygram")

    settings = AppSettings()

    assert settings.github_repo == "easygram"


def test_resolve_tdlib_root_uses_project_root_for_relative_path(tmp_path: Path) -> None:
    settings = AppSettings(tdlib_root="vendor/tdlib")

    resolved = resolve_tdlib_root(settings, project_root=tmp_path)

    assert resolved == tmp_path / "vendor/tdlib"
