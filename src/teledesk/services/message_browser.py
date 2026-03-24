"""Browse pointer logic for message reading from the input control."""

from __future__ import annotations

from dataclasses import dataclass

from teledesk.domain.models import ChatViewState, MessageRecord


@dataclass(slots=True)
class BrowseResult:
    message: MessageRecord | None
    reason: str = ""


class MessageBrowser:
    def move_previous(self, state: ChatViewState) -> BrowseResult:
        if not state.messages:
            return BrowseResult(message=None, reason="No messages loaded.")
        if state.browse_index <= 0:
            return BrowseResult(message=None, reason="Older messages may be available.")
        state.browse_index -= 1
        return BrowseResult(message=state.messages[state.browse_index])

    def move_next(self, state: ChatViewState) -> BrowseResult:
        if not state.messages:
            return BrowseResult(message=None, reason="No messages loaded.")
        if state.browse_index >= len(state.messages) - 1:
            return BrowseResult(message=None, reason="End of messages.")
        state.browse_index += 1
        return BrowseResult(message=state.messages[state.browse_index])
