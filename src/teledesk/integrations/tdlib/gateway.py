"""TDLib gateway skeleton.

This module intentionally starts as a thin abstraction. The actual tdjson loading
and receive loop will be expanded as the Telegram implementation lands.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from queue import Queue
from threading import Event, Thread
from typing import Any


@dataclass(slots=True)
class TdlibGateway:
    event_queue: Queue[dict[str, Any]] = field(default_factory=Queue)
    _running: Event = field(default_factory=Event)
    _thread: Thread | None = None

    def start(self) -> None:
        self._running.set()

    def stop(self) -> None:
        self._running.clear()

    def send(self, query: dict[str, Any]) -> None:
        self.event_queue.put({"kind": "request", "payload": query})
