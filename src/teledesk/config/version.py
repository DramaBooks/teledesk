"""Version helpers for Teledesk."""

from __future__ import annotations

from dataclasses import dataclass

from packaging.version import Version

from teledesk import __version__


@dataclass(frozen=True, slots=True)
class AppVersion:
    raw: str

    @property
    def parsed(self) -> Version:
        return Version(self.raw)

    def is_newer_than(self, other: "AppVersion") -> bool:
        return self.parsed > other.parsed


def current_version() -> AppVersion:
    return AppVersion(__version__)
