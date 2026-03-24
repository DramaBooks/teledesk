"""Update prompt dialog."""

from __future__ import annotations

import wx  # type: ignore[import-not-found]

from easygram.domain.updates import UpdateCheckResult


class UpdateDialog(wx.MessageDialog):
    def __init__(self, parent: wx.Window | None, result: UpdateCheckResult) -> None:
        release_summary = ""
        if result.release and result.release.body:
            first_line = result.release.body.strip().splitlines()[0]
            release_summary = f"\n\nRelease notes: {first_line[:160]}"
        message = (
            f"Version {result.latest_version} is available.\n\n"
            "Do you want to download and install the portable update now?"
            f"{release_summary}"
        )
        super().__init__(
            parent,
            message=message,
            caption="Update available",
            style=wx.YES_NO | wx.ICON_INFORMATION,
        )
