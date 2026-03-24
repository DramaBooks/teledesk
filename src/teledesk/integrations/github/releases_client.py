"""GitHub Releases API client."""

from __future__ import annotations

from dataclasses import dataclass

import requests  # type: ignore[import-not-found]

from teledesk.domain.updates import ReleaseAsset, ReleaseInfo

GITHUB_API_BASE = "https://api.github.com"


@dataclass(slots=True)
class GitHubReleasesClient:
    owner: str
    repo: str
    timeout: float = 10.0

    def latest_release(self) -> ReleaseInfo:
        response = requests.get(
            f"{GITHUB_API_BASE}/repos/{self.owner}/{self.repo}/releases/latest",
            headers={"Accept": "application/vnd.github+json"},
            timeout=self.timeout,
        )
        response.raise_for_status()
        payload = response.json()
        return self._parse_release(payload)

    def _parse_release(self, payload: dict) -> ReleaseInfo:
        assets = [
            ReleaseAsset(
                name=item["name"],
                download_url=item["browser_download_url"],
                size=item.get("size", 0),
                content_type=item.get("content_type", "application/octet-stream"),
                digest=item.get("digest"),
            )
            for item in payload.get("assets", [])
        ]
        return ReleaseInfo(
            tag_name=payload["tag_name"],
            name=payload.get("name") or payload["tag_name"],
            html_url=payload["html_url"],
            body=payload.get("body", ""),
            prerelease=payload.get("prerelease", False),
            assets=assets,
        )
