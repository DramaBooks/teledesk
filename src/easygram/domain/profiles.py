"""Column and reading profiles."""

from __future__ import annotations

from dataclasses import dataclass, field


DEFAULT_MESSAGE_FIELDS = ["sender", "timestamp", "message_type", "text", "status"]


@dataclass(frozen=True, slots=True)
class ColumnProfile:
    name: str
    fields: list[str] = field(default_factory=list)

    @classmethod
    def default_message_profile(cls) -> "ColumnProfile":
        return cls(name="standard", fields=list(DEFAULT_MESSAGE_FIELDS))
