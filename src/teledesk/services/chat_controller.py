"""Chat state controller."""

from __future__ import annotations

from dataclasses import dataclass, field

from teledesk.domain.models import ChatSummary, ChatViewState


@dataclass(slots=True)
class ChatController:
    chats: list[ChatSummary] = field(default_factory=list)
    current_chat_id: int | None = None
    chat_states: dict[int, ChatViewState] = field(default_factory=dict)
    chat_list_index: int = 0

    def open_chat(self, chat_id: int) -> ChatViewState:
        self.current_chat_id = chat_id
        return self.chat_states.setdefault(chat_id, ChatViewState())

    def close_chat(self) -> None:
        self.current_chat_id = None

    def selected_chat_state(self) -> ChatViewState | None:
        if self.current_chat_id is None:
            return None
        return self.chat_states.get(self.current_chat_id)
