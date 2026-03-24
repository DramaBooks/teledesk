"""Release and updater models."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ReleaseAsset:
    name: str
    download_url: str
    size: int
    content_type: str
    digest: str | None = None

    @property
    def is_portable_bundle(self) -> bool:
        lowered = self.name.lower()
        return lowered.endswith(".zip") and "portable" in lowered


@dataclass(frozen=True, slots=True)
class ReleaseInfo:
    tag_name: str
    name: str
    html_url: str
    body: str
    prerelease: bool
    assets: list[ReleaseAsset]

    @property
    def version(self) -> str:
        return self.tag_name.removeprefix("v")


@dataclass(frozen=True, slots=True)
class UpdateCheckResult:
    update_available: bool
    current_version: str
    latest_version: str | None = None
    release: ReleaseInfo | None = None
    reason: str = ""
