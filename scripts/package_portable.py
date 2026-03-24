"""Create a zip portable package from the PyInstaller onedir output."""

from __future__ import annotations

import hashlib
import shutil
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from teledesk import __version__  # type: ignore[import-not-found]


def sha256_for(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 64), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def main() -> int:
    project_root = PROJECT_ROOT
    dist_dir = project_root / "dist"
    portable_dir = dist_dir / "teledesk"
    if not portable_dir.exists():
        raise FileNotFoundError(f"Portable directory not found: {portable_dir}")

    archive_base = dist_dir / f"teledesk-portable-v{__version__}-windows-x64"
    archive_path = Path(shutil.make_archive(str(archive_base), "zip", root_dir=portable_dir.parent, base_dir=portable_dir.name))
    checksum_path = archive_path.with_suffix(".zip.sha256")
    checksum_path.write_text(f"{sha256_for(archive_path)}  {archive_path.name}\n", encoding="utf-8")
    print(f"Created {archive_path}")
    print(f"Created {checksum_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
