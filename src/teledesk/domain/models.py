"""Core domain models."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Literal

MessageType = Literal["text", "voice", "photo", "file", "system"]
AuthStage = Literal[
    "wait_tdlib_parameters",
    "wait_phone_number",
    "wait_code",
    "wait_password",
    "ready",
    "closed",
    "error",
]


@dataclass(frozen=True, slots=True)
class ChatSummary:
    id: int
    title: str
    unread_count: int = 0
    last_message_preview: str = ""


@dataclass(frozen=True, slots=True)
class MessageRecord:
    id: int
    sender: str
    timestamp: datetime
    text: str = ""
    message_type: MessageType = "text"
    duration: int | None = None
    status: str = ""
    has_attachment: bool = False
    reply_preview: str | None = None


@dataclass(frozen=True, slots=True)
class FileTransferState:
    file_id: int
    local_path: str | None = None
    bytes_downloaded: int = 0
    bytes_total: int = 0
    is_complete: bool = False


@dataclass(frozen=True, slots=True)
class AuthorizationState:
    stage: AuthStage
    hint: str = ""
    is_authorized: bool = False


@dataclass(slots=True)
class ChatViewState:
    selected_index: int = 0
    browse_index: int = 0
    chunk_anchor_message_id: int | None = None
    has_older_chunk: bool = False
    has_newer_chunk: bool = False
    messages: list[MessageRecord] = field(default_factory=list)
