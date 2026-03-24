"""accessible_output2 backend."""

from __future__ import annotations

from typing import Any


class AccessibleOutput2Backend:
    def __init__(self) -> None:
        self._output: Any | None = None
        try:
            from accessible_output2.outputs.auto import Auto  # type: ignore[import-not-found]

            self._output = Auto()
        except Exception:
            self._output = None

    def is_available(self) -> bool:
        return self._output is not None

    def speak(self, text: str, *, interrupt: bool = False) -> None:
        if self._output is not None:
            self._output.speak(text, interrupt=interrupt)

    def braille(self, text: str) -> None:
        if self._output is not None:
            self._output.braille(text)

    def output(self, text: str, *, interrupt: bool = False) -> None:
        if self._output is not None:
            self._output.output(text, interrupt=interrupt)
