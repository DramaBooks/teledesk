"""Portable update handoff helpers for Windows.

The replacement is delegated to a temporary batch script so the running process
can exit before files are replaced.
"""

from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path
from zipfile import ZipFile


class PortableUpdater:
    def extract_archive(self, archive_path: Path) -> Path:
        extract_root = Path(tempfile.mkdtemp(prefix="easygram-update-extract-"))
        with ZipFile(archive_path) as archive:
            archive.extractall(extract_root)
        candidates = [path for path in extract_root.iterdir() if path.is_dir()]
        if len(candidates) == 1:
            return candidates[0]
        return extract_root

    def create_replace_script(
        self,
        *,
        install_dir: Path,
        extracted_dir: Path,
        executable_name: str,
        script_path: Path,
    ) -> Path:
        script_path.write_text(
            "\n".join(
                [
                    "@echo off",
                    "setlocal",
                    "timeout /t 2 /nobreak >nul",
                    f'xcopy /E /I /Y "{extracted_dir}" "{install_dir}" >nul',
                    f'start "" "{install_dir / executable_name}"',
                    "del %~f0",
                ]
            ),
            encoding="utf-8",
        )
        return script_path

    def launch_replace_script(self, script_path: Path) -> None:
        subprocess.Popen(["cmd.exe", "/c", str(script_path)], close_fds=True)

    def apply_portable_update(
        self,
        *,
        archive_path: Path,
        install_dir: Path,
        executable_name: str,
    ) -> Path:
        extracted_dir = self.extract_archive(archive_path)
        script_path = archive_path.parent / "apply_easygram_update.cmd"
        self.create_replace_script(
            install_dir=install_dir,
            extracted_dir=extracted_dir,
            executable_name=executable_name,
            script_path=script_path,
        )
        self.launch_replace_script(script_path)
        return script_path
