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
    tdlib_root: str = os.getenv("TELEDESK_TDLIB_ROOT", "vendor/tdlib")
    telegram_api_id: str = os.getenv("TELEDESK_TG_API_ID", "")
    telegram_api_hash: str = os.getenv("TELEDESK_TG_API_HASH", "")
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
            tdlib_root=payload.get("tdlib_root", "vendor/tdlib"),
            telegram_api_id=payload.get("telegram_api_id", ""),
            telegram_api_hash=payload.get("telegram_api_hash", ""),
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


def merge_settings(settings: AppSettings, **changes: Any) -> AppSettings:
    payload = asdict(settings)
    payload.update(changes)
    payload["update"] = UpdateSettings(**payload["update"])
    payload["accessibility"] = AccessibilitySettings(**payload["accessibility"])
    return AppSettings(**payload)
