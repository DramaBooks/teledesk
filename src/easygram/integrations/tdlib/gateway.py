"""TDLib gateway skeleton.

This module intentionally starts as a thin abstraction. The actual tdjson loading
and receive loop will be expanded as the Telegram implementation lands.
"""

from __future__ import annotations

import ctypes
from dataclasses import dataclass, field
from pathlib import Path
from queue import Queue
from threading import Event, Thread
from typing import Any


TDJSON_DLL_CANDIDATES = (
    "tdjson.dll",
    "libtdjson.dll",
)


@dataclass(slots=True)
class TdjsonBindings:
    library_path: Path
    library: ctypes.CDLL

    @classmethod
    def load(cls, library_path: Path) -> "TdjsonBindings":
        library = ctypes.CDLL(str(library_path))
        library.td_json_client_create.restype = ctypes.c_void_p
        library.td_json_client_send.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
        library.td_json_client_receive.argtypes = [ctypes.c_void_p, ctypes.c_double]
        library.td_json_client_receive.restype = ctypes.c_char_p
        library.td_json_client_execute.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
        library.td_json_client_execute.restype = ctypes.c_char_p
        library.td_json_client_destroy.argtypes = [ctypes.c_void_p]
        return cls(library_path=library_path, library=library)

    def create_client(self) -> ctypes.c_void_p:
        return ctypes.c_void_p(self.library.td_json_client_create())


@dataclass(slots=True)
class TdlibGateway:
    tdlib_root: Path | None = None
    event_queue: Queue[dict[str, Any]] = field(default_factory=Queue)
    _running: Event = field(default_factory=Event)
    _thread: Thread | None = None
    _client: ctypes.c_void_p | None = None
    _tdjson: TdjsonBindings | None = None
    last_error: str = ""

    def candidate_library_paths(self) -> list[Path]:
        candidates: list[Path] = []
        if self.tdlib_root is not None:
            for base in [self.tdlib_root, self.tdlib_root / "bin", self.tdlib_root / "lib"]:
                for name in TDJSON_DLL_CANDIDATES:
                    candidates.append(base / name)
        for name in TDJSON_DLL_CANDIDATES:
            candidates.append(Path(name))
        unique: list[Path] = []
        seen: set[str] = set()
        for item in candidates:
            key = str(item).lower()
            if key not in seen:
                seen.add(key)
                unique.append(item)
        return unique

    def load_library(self) -> bool:
        for candidate in self.candidate_library_paths():
            try:
                if candidate.exists() or candidate.parent == Path("."):
                    self._tdjson = TdjsonBindings.load(candidate)
                    self.last_error = ""
                    return True
            except OSError as exc:
                self.last_error = str(exc)
        if not self.last_error:
            self.last_error = "tdjson library not found."
        return False

    def is_available(self) -> bool:
        return self._tdjson is not None or self.load_library()

    def start(self) -> None:
        self._running.set()
        if self._client is None and self.is_available() and self._tdjson is not None:
            self._client = self._tdjson.create_client()

    def stop(self) -> None:
        self._running.clear()
        if self._client is not None and self._tdjson is not None:
            self._tdjson.library.td_json_client_destroy(self._client)
            self._client = None

    def send(self, query: dict[str, Any]) -> None:
        self.event_queue.put({"kind": "request", "payload": query})
