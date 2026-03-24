"""Update checking and download orchestration."""

from __future__ import annotations

import hashlib
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Final

import requests  # type: ignore[import-not-found]

from teledesk.config.version import AppVersion, current_version
from teledesk.domain.updates import ReleaseAsset, ReleaseInfo, UpdateCheckResult
from teledesk.integrations.github.releases_client import GitHubReleasesClient


@dataclass(slots=True)
class DownloadedRelease:
    release: ReleaseInfo
    asset: ReleaseAsset
    archive_path: Path


class UpdateService:
    PORTABLE_PLATFORM_HINT: Final[str] = "windows-x64"

    def __init__(self, releases_client: GitHubReleasesClient) -> None:
        self.releases_client = releases_client

    def check_for_updates(self) -> UpdateCheckResult:
        release = self.releases_client.latest_release()
        latest = AppVersion(release.tag_name.removeprefix("v"))
        current = current_version()
        if latest.is_newer_than(current):
            return UpdateCheckResult(
                update_available=True,
                current_version=current.raw,
                latest_version=latest.raw,
                release=release,
            )
        return UpdateCheckResult(
            update_available=False,
            current_version=current.raw,
            latest_version=latest.raw,
            reason="Already on latest version.",
        )

    def check_for_updates_safely(self) -> UpdateCheckResult:
        current = current_version()
        try:
            return self.check_for_updates()
        except requests.RequestException as exc:
            return UpdateCheckResult(
                update_available=False,
                current_version=current.raw,
                reason=f"Update check failed: {exc}",
            )
        except Exception as exc:
            return UpdateCheckResult(
                update_available=False,
                current_version=current.raw,
                reason=f"Unexpected update error: {exc}",
            )

    def select_portable_asset(self, release: ReleaseInfo) -> ReleaseAsset | None:
        preferred: list[ReleaseAsset] = []
        for asset in release.assets:
            lowered = asset.name.lower()
            if asset.is_portable_bundle and self.PORTABLE_PLATFORM_HINT in lowered:
                preferred.append(asset)
        if preferred:
            preferred.sort(key=lambda item: item.size, reverse=True)
            return preferred[0]
        return None

    def download_release(self, release: ReleaseInfo, asset: ReleaseAsset) -> DownloadedRelease:
        response = requests.get(asset.download_url, timeout=30.0, stream=True)
        response.raise_for_status()
        releases_dir = Path(tempfile.mkdtemp(prefix="teledesk-update-"))
        archive_path = releases_dir / asset.name
        with archive_path.open("wb") as handle:
            for chunk in response.iter_content(chunk_size=1024 * 64):
                if chunk:
                    handle.write(chunk)
        return DownloadedRelease(release=release, asset=asset, archive_path=archive_path)

    def verify_digest(self, archive_path: Path, expected_digest: str | None) -> bool:
        if not expected_digest:
            return True
        algorithm, _, expected_hash = expected_digest.partition(":")
        if not algorithm or not expected_hash:
            return False
        hasher = hashlib.new(algorithm)
        with archive_path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 64), b""):
                hasher.update(chunk)
        return hasher.hexdigest().lower() == expected_hash.lower()
