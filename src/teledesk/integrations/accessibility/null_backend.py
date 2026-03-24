"""No-op accessibility backend for unsupported environments and tests."""

from __future__ import annotations


class NullAccessibilityBackend:
    def is_available(self) -> bool:
        return True

    def speak(self, text: str, *, interrupt: bool = False) -> None:
        return None

    def braille(self, text: str) -> None:
        return None

    def output(self, text: str, *, interrupt: bool = False) -> None:
        return None
