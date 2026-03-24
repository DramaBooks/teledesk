"""Chat conversation panel."""

from __future__ import annotations

from collections.abc import Callable

import wx  # type: ignore[import-not-found]


class ChatViewPanel(wx.Panel):
    def __init__(self, parent: wx.Window, on_back: Callable[[], None]) -> None:
        super().__init__(parent)
        self.on_back = on_back
        self.chat_id: int | None = None
        self._build_ui()

    def _build_ui(self) -> None:
        root = wx.BoxSizer(wx.VERTICAL)

        top_bar = wx.BoxSizer(wx.HORIZONTAL)
        self.btn_back = wx.Button(self, label="Back")
        self.btn_prev_chunk = wx.Button(self, label="Previous messages")
        self.btn_next_chunk = wx.Button(self, label="Next messages")
        self.btn_back.Bind(wx.EVT_BUTTON, lambda _event: self.on_back())
        top_bar.Add(self.btn_back, 0, wx.ALL, 4)
        top_bar.AddStretchSpacer()
        top_bar.Add(self.btn_prev_chunk, 0, wx.ALL, 4)
        top_bar.Add(self.btn_next_chunk, 0, wx.ALL, 4)

        self.message_list = wx.ListCtrl(self, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
        self.message_list.AppendColumn("Message", width=900)

        composer = wx.BoxSizer(wx.HORIZONTAL)
        self.input_ctrl = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        self.btn_send = wx.Button(self, label="Send")
        self.btn_record = wx.Button(self, label="Record")
        self.btn_attach = wx.Button(self, label="Attach")
        composer.Add(self.input_ctrl, 1, wx.EXPAND | wx.ALL, 4)
        composer.Add(self.btn_send, 0, wx.ALL, 4)
        composer.Add(self.btn_record, 0, wx.ALL, 4)
        composer.Add(self.btn_attach, 0, wx.ALL, 4)

        root.Add(top_bar, 0, wx.EXPAND | wx.ALL, 4)
        root.Add(self.message_list, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 8)
        root.Add(composer, 0, wx.EXPAND | wx.ALL, 8)
        self.SetSizer(root)

    def load_chat(self, chat_id: int) -> None:
        self.chat_id = chat_id
        self.message_list.DeleteAllItems()
        for row in [
            "You, 09:41, text, Teledesk bootstrap is alive.",
            "System, 09:42, text, Chat shell loaded.",
        ]:
            self.message_list.InsertItem(self.message_list.GetItemCount(), row)
