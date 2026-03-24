"""Formatting helpers for accessible announcements."""

from __future__ import annotations

from easygram.domain.models import MessageRecord
from easygram.domain.profiles import ColumnProfile


class AccessibleFormatter:
    def format_message(self, message: MessageRecord, profile: ColumnProfile) -> str:
        values: list[str] = []
        for field in profile.fields:
            value = getattr(message, field, None)
            if value is None or value == "":
                continue
            if field == "timestamp":
                values.append(message.timestamp.strftime("%Y-%m-%d %H:%M"))
            elif field == "duration" and message.duration is not None:
                values.append(f"{message.duration} seconds")
            else:
                values.append(str(value))
        return ", ".join(values)
