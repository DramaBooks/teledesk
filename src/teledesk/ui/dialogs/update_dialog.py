"""Update prompt dialog."""

from __future__ import annotations

import wx  # type: ignore[import-not-found]

from teledesk.domain.updates import UpdateCheckResult


class UpdateDialog(wx.MessageDialog):
    def __init__(self, parent: wx.Window | None, result: UpdateCheckResult) -> None:
        message = (
            f"Version {result.latest_version} is available.\n\n"
            "Do you want to download and install the portable update now?"
        )
        super().__init__(
            parent,
            message=message,
            caption="Update available",
            style=wx.YES_NO | wx.ICON_INFORMATION,
        )
