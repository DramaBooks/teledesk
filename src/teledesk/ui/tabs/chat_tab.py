"""Chat tab host panel."""

from __future__ import annotations

import wx  # type: ignore[import-not-found]

from teledesk.services.chat_controller import ChatController
from teledesk.ui.panels.chat_list_panel import ChatListPanel
from teledesk.ui.panels.chat_view_panel import ChatViewPanel


class ChatTab(wx.Panel):
    def __init__(self, parent: wx.Window, chat_controller: ChatController) -> None:
        super().__init__(parent)
        self.chat_controller = chat_controller
        self._stack = wx.BoxSizer(wx.VERTICAL)
        self.chat_list_panel = ChatListPanel(self, on_open_chat=self._open_chat)
        self.chat_view_panel = ChatViewPanel(self, on_back=self._back_to_list)
        self._stack.Add(self.chat_list_panel, 1, wx.EXPAND)
        self._stack.Add(self.chat_view_panel, 1, wx.EXPAND)
        self.SetSizer(self._stack)
        self._show_list()

    def _show_list(self) -> None:
        self.chat_list_panel.Show()
        self.chat_view_panel.Hide()
        self.Layout()

    def _show_chat(self) -> None:
        self.chat_list_panel.Hide()
        self.chat_view_panel.Show()
        self.Layout()

    def _open_chat(self, chat_id: int) -> None:
        self.chat_controller.open_chat(chat_id)
        self.chat_view_panel.load_chat(chat_id)
        self._show_chat()

    def _back_to_list(self) -> None:
        self.chat_controller.close_chat()
        self._show_list()
