"""Accessibility service contracts."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


class AccessibilityBackend(Protocol):
    def speak(self, text: str, *, interrupt: bool = False) -> None: ...
    def braille(self, text: str) -> None: ...
    def output(self, text: str, *, interrupt: bool = False) -> None: ...
    def is_available(self) -> bool: ...


@dataclass(slots=True)
class AccessibilityService:
    backend: AccessibilityBackend

    def announce(self, text: str, *, interrupt: bool = False) -> None:
        if self.backend.is_available() and text:
            self.backend.output(text, interrupt=interrupt)
