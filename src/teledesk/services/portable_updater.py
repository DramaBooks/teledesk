"""Portable update handoff helpers for Windows.

The replacement is delegated to a temporary batch script so the running process
can exit before files are replaced.
"""

from __future__ import annotations

import subprocess
from pathlib import Path


class PortableUpdater:
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
