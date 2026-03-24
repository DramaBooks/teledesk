"""TDLib mapping helpers."""

from __future__ import annotations

from datetime import datetime

from teledesk.domain.models import MessageRecord


def map_text_message(message_id: int, sender: str, text: str) -> MessageRecord:
    return MessageRecord(id=message_id, sender=sender, text=text, timestamp=datetime.now())
