"""Application settings and path helpers."""

from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


APP_DIR_NAME = "Teledesk"
SETTINGS_FILE_NAME = "settings.json"


@dataclass(slots=True)
class UpdateSettings:
    check_on_startup: bool = True
    channel: str = "stable"
    last_seen_version: str | None = None


@dataclass(slots=True)
class AccessibilitySettings:
    announce_navigation: bool = True
    announce_updates: bool = True
    message_reading_fields: list[str] = field(
        default_factory=lambda: ["sender", "timestamp", "message_type", "text", "status"]
    )


@dataclass(slots=True)
class AppSettings:
    github_owner: str = os.getenv("TELEDESK_GITHUB_OWNER", "Germano")
    github_repo: str = os.getenv("TELEDESK_GITHUB_REPO", "teledesk")
    github_api_base: str = os.getenv("TELEDESK_GITHUB_API_BASE", "https://api.github.com")
    tdlib_root: str = os.getenv("TELEDESK_TDLIB_ROOT", "vendor/tdlib")
    telegram_api_id: str = os.getenv("TELEDESK_TG_API_ID", "")
    telegram_api_hash: str = os.getenv("TELEDESK_TG_API_HASH", "")
    portable_executable_name: str = os.getenv("TELEDESK_PORTABLE_EXE", "teledesk.exe")
    selected_chat_id: int | None = None
    update: UpdateSettings = field(default_factory=UpdateSettings)
    accessibility: AccessibilitySettings = field(default_factory=AccessibilitySettings)


class SettingsStore:
    def __init__(self, root: Path | None = None) -> None:
        self.root = root or default_data_root()
        self.root.mkdir(parents=True, exist_ok=True)
        self.path = self.root / SETTINGS_FILE_NAME

    def load(self) -> AppSettings:
        if not self.path.exists():
            return AppSettings()

        payload = json.loads(self.path.read_text(encoding="utf-8"))
        return AppSettings(
            github_owner=payload.get("github_owner", "Germano"),
            github_repo=payload.get("github_repo", "teledesk"),
            github_api_base=payload.get("github_api_base", "https://api.github.com"),
            tdlib_root=payload.get("tdlib_root", "vendor/tdlib"),
            telegram_api_id=payload.get("telegram_api_id", ""),
            telegram_api_hash=payload.get("telegram_api_hash", ""),
            portable_executable_name=payload.get("portable_executable_name", "teledesk.exe"),
            selected_chat_id=payload.get("selected_chat_id"),
            update=UpdateSettings(**payload.get("update", {})),
            accessibility=AccessibilitySettings(**payload.get("accessibility", {})),
        )

    def save(self, settings: AppSettings) -> None:
        payload = asdict(settings)
        self.path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def default_data_root() -> Path:
    appdata = os.getenv("APPDATA")
    if appdata:
        return Path(appdata) / APP_DIR_NAME
    return Path.home() / ".teledesk"


def find_project_root(start: Path | None = None) -> Path:
    current = (start or Path(__file__).resolve()).resolve()
    for candidate in [current, *current.parents]:
        if candidate.is_dir() and (candidate / "pyproject.toml").exists():
            return candidate
    return Path.cwd()


def load_env_file(path: Path, *, override: bool = False) -> bool:
    if not path.exists():
        return False

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and (override or key not in os.environ):
            os.environ[key] = value
    return True


def bootstrap_environment(start: Path | None = None) -> Path:
    project_root = find_project_root(start)
    load_env_file(project_root / ".env")
    return project_root


def resolve_tdlib_root(settings: AppSettings, *, project_root: Path | None = None) -> Path:
    root = Path(settings.tdlib_root)
    if root.is_absolute():
        return root
    return (project_root or find_project_root()) / root


def merge_settings(settings: AppSettings, **changes: Any) -> AppSettings:
    payload = asdict(settings)
    payload.update(changes)
    payload["update"] = UpdateSettings(**payload["update"])
    payload["accessibility"] = AccessibilitySettings(**payload["accessibility"])
    return AppSettings(**payload)
