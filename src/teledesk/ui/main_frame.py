"""Main frame for the Teledesk application."""

from __future__ import annotations

import wx  # type: ignore[import-not-found]

from teledesk.services.chat_controller import ChatController
from teledesk.ui.tabs.chat_tab import ChatTab


class MainFrame(wx.Frame):
    def __init__(self, chat_controller: ChatController) -> None:
        super().__init__(parent=None, title="Teledesk", size=(1100, 760))
        self.chat_controller = chat_controller
        self._create_ui()

    def _create_ui(self) -> None:
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        self.notebook = wx.Notebook(panel)
        self.notebook.AddPage(ChatTab(self.notebook, self.chat_controller), "Chat")
        self.notebook.AddPage(self._placeholder_tab("Contacts"), "Contacts")
        self.notebook.AddPage(self._placeholder_tab("Calls"), "Calls")

        sizer.Add(self.notebook, 1, wx.EXPAND | wx.ALL, 8)
        panel.SetSizer(sizer)
        self.CreateStatusBar()
        self.SetStatusText("Ready")

    def _placeholder_tab(self, label: str) -> wx.Panel:
        panel = wx.Panel(self.notebook)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(wx.StaticText(panel, label=f"{label} will land in a later iteration."), 0, wx.ALL, 16)
        panel.SetSizer(sizer)
        return panel
