"""Settings dialog placeholder."""

from __future__ import annotations

import wx  # type: ignore[import-not-found]


class SettingsDialog(wx.Dialog):
    def __init__(self, parent: wx.Window | None) -> None:
        super().__init__(parent, title="Settings")
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(wx.StaticText(self, label="Settings UI will be expanded in the next iteration."), 0, wx.ALL, 16)
        sizer.Add(self.CreateButtonSizer(wx.OK), 0, wx.ALL | wx.ALIGN_RIGHT, 8)
        self.SetSizerAndFit(sizer)
