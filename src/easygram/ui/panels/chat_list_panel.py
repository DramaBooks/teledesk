"""Chat list panel."""

from __future__ import annotations

from collections.abc import Callable

import wx  # type: ignore[import-not-found]


class ChatListPanel(wx.Panel):
    def __init__(self, parent: wx.Window, on_open_chat: Callable[[int], None]) -> None:
        super().__init__(parent)
        self.on_open_chat = on_open_chat
        self._build_ui()
        self._seed_demo_rows()

    def _build_ui(self) -> None:
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.search_ctrl = wx.TextCtrl(self)
        self.chat_list = wx.ListCtrl(self, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
        self.chat_list.AppendColumn("Chat", width=280)
        self.chat_list.AppendColumn("Last message", width=520)
        self.chat_list.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self._handle_open_chat)

        sizer.Add(wx.StaticText(self, label="Search chats"), 0, wx.LEFT | wx.TOP | wx.RIGHT, 8)
        sizer.Add(self.search_ctrl, 0, wx.EXPAND | wx.ALL, 8)
        sizer.Add(self.chat_list, 1, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 8)
        self.SetSizer(sizer)

    def _seed_demo_rows(self) -> None:
        demo_rows = [
            ("Saved Messages", "Initial bootstrap complete."),
            ("Marco", "Ci sentiamo dopo"),
            ("Team Easygram", "Accessibility first, chaos later."),
        ]
        for title, preview in demo_rows:
            index = self.chat_list.InsertItem(self.chat_list.GetItemCount(), title)
            self.chat_list.SetItem(index, 1, preview)

    def _handle_open_chat(self, event: wx.ListEvent) -> None:
        self.on_open_chat(event.GetIndex() + 1)
