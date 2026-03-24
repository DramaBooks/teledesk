"""Application bootstrap."""

from __future__ import annotations

import sys

from teledesk.config.settings import AppSettings, SettingsStore
from teledesk.integrations.accessibility.accessible_output2_backend import AccessibleOutput2Backend
from teledesk.integrations.accessibility.null_backend import NullAccessibilityBackend
from teledesk.integrations.accessibility.service import AccessibilityService
from teledesk.services.chat_controller import ChatController


def _build_accessibility_service() -> AccessibilityService:
    backend = AccessibleOutput2Backend()
    if not backend.is_available():
        backend = NullAccessibilityBackend()
    return AccessibilityService(backend=backend)


def _missing_dependency_message(exc: Exception) -> int:
    print(
        "Teledesk requires desktop dependencies that are not installed yet. "
        f"Original error: {exc}",
        file=sys.stderr,
    )
    return 1


def run(settings: AppSettings | None = None) -> int:
    try:
        import wx  # type: ignore[import-not-found]
    except Exception as exc:
        return _missing_dependency_message(exc)

    settings_store = SettingsStore()
    loaded_settings = settings or settings_store.load()
    chat_controller = ChatController()
    accessibility = _build_accessibility_service()
    accessibility.announce("Teledesk started.")

    from teledesk.ui.main_frame import MainFrame

    app = wx.App(False)
    frame = MainFrame(chat_controller)
    frame.Show(True)
    exit_code = app.MainLoop()
    settings_store.save(loaded_settings)
    return int(exit_code or 0)


def main() -> int:
    return run()
