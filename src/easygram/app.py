"""Application bootstrap."""

from __future__ import annotations

import sys
from pathlib import Path

from easygram.config.settings import AppSettings, SettingsStore, bootstrap_environment
from easygram.config.version import current_version
from easygram.integrations.accessibility.accessible_output2_backend import AccessibleOutput2Backend
from easygram.integrations.accessibility.null_backend import NullAccessibilityBackend
from easygram.integrations.accessibility.service import AccessibilityService
from easygram.integrations.github.releases_client import GitHubReleasesClient
from easygram.services.chat_controller import ChatController
from easygram.services.portable_updater import PortableUpdater
from easygram.services.update_service import UpdateService


def _build_accessibility_service() -> AccessibilityService:
    backend = AccessibleOutput2Backend()
    if not backend.is_available():
        backend = NullAccessibilityBackend()
    return AccessibilityService(backend=backend)


def _missing_dependency_message(exc: Exception) -> int:
    print(
        "Easygram requires desktop dependencies that are not installed yet. "
        f"Original error: {exc}",
        file=sys.stderr,
    )
    return 1


def _running_install_dir() -> Path | None:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return None


def _maybe_prompt_for_updates(
    *,
    wx: object,
    frame: object,
    settings_store: SettingsStore,
    settings: AppSettings,
    accessibility: AccessibilityService,
) -> None:
    if not settings.update.check_on_startup:
        return

    client = GitHubReleasesClient(
        owner=settings.github_owner,
        repo=settings.github_repo,
        api_base=settings.github_api_base,
    )
    update_service = UpdateService(client)
    result = update_service.check_for_updates_safely()
    if not result.update_available or result.release is None:
        return

    from easygram.ui.dialogs.update_dialog import UpdateDialog

    if settings.accessibility.announce_updates:
        accessibility.announce(f"Update available: version {result.latest_version}.")

    dialog = UpdateDialog(frame, result)
    try:
        choice = dialog.ShowModal()
    finally:
        dialog.Destroy()

    if choice != wx.ID_YES:
        settings.update.last_seen_version = result.latest_version
        settings_store.save(settings)
        return

    asset = update_service.select_portable_asset(result.release)
    if asset is None:
        wx.MessageBox(
            "A newer release exists, but no portable Windows asset was found.",
            "Update unavailable",
            wx.OK | wx.ICON_WARNING,
        )
        return

    downloaded = update_service.download_release(result.release, asset)
    if not update_service.verify_digest(downloaded.archive_path, asset.digest):
        wx.MessageBox(
            "The downloaded update failed checksum verification and will not be installed.",
            "Update failed",
            wx.OK | wx.ICON_ERROR,
        )
        return

    install_dir = _running_install_dir()
    if install_dir is None:
        wx.MessageBox(
            f"Update downloaded to:\n{downloaded.archive_path}\n\n"
            "Automatic replacement is available only in the packaged portable build.",
            "Update downloaded",
            wx.OK | wx.ICON_INFORMATION,
        )
        return

    updater = PortableUpdater()
    updater.apply_portable_update(
        archive_path=downloaded.archive_path,
        install_dir=install_dir,
        executable_name=settings.portable_executable_name,
    )
    settings.update.last_seen_version = result.latest_version
    settings_store.save(settings)
    wx.MessageBox(
        "The update has been staged. Easygram will now exit so the portable files can be replaced.",
        "Applying update",
        wx.OK | wx.ICON_INFORMATION,
    )
    raise SystemExit(0)


def run(settings: AppSettings | None = None) -> int:
    bootstrap_environment()
    try:
        import wx  # type: ignore[import-not-found]
    except Exception as exc:
        return _missing_dependency_message(exc)

    settings_store = SettingsStore()
    loaded_settings = settings or settings_store.load()
    chat_controller = ChatController()
    accessibility = _build_accessibility_service()
    accessibility.announce("Easygram started.")

    from easygram.ui.main_frame import MainFrame

    app = wx.App(False)
    frame = MainFrame(chat_controller)
    frame.Show(True)
    frame.SetStatusText(f"Ready - v{current_version().raw}")
    _maybe_prompt_for_updates(
        wx=wx,
        frame=frame,
        settings_store=settings_store,
        settings=loaded_settings,
        accessibility=accessibility,
    )
    exit_code = app.MainLoop()
    settings_store.save(loaded_settings)
    return int(exit_code or 0)


def main() -> int:
    return run()
