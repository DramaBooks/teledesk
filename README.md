# Easygram

Easygram is an accessible Windows Telegram client built with `wxPython`, `TDLib`, and a dedicated accessibility layer designed for screen readers and braille output.

## Current status

This repository is in active bootstrap. The initial implementation focuses on:

- Windows-first desktop architecture
- accessible Chat tab behavior
- public GitHub distribution
- portable builds via PyInstaller (one-folder mode)
- in-app update checks via GitHub Releases

## Planned architecture

- `wxPython` for the desktop UI
- `TDLib` via `tdjson` for Telegram integration
- `accessible-output2` behind an abstraction layer
- GitHub Releases for portable distribution
- helper-based portable self-update flow

## Repository and release strategy

- Repository name: `easygram`
- Recommended visibility: public
- Binary distribution: GitHub Releases assets
- Packaging: PyInstaller one-folder bundle zipped as portable app
- Update source: GitHub Releases API (`/releases/latest`)

## Environment variables

Copy `.env.example` to `.env` and fill in the Telegram API credentials.

- `EASYGRAM_TG_API_ID`
- `EASYGRAM_TG_API_HASH`
- `EASYGRAM_GITHUB_OWNER`
- `EASYGRAM_GITHUB_REPO`

Legacy `TELEDESK_*` variables are still accepted for compatibility during the rename transition.

## Development notes

### Python

The project targets Python 3.12+.

> Note: some desktop dependencies such as `wxPython` may lag behind the newest CPython release on Windows. If dependency installation becomes grumpy, prefer Python 3.12 or 3.13 for day-to-day development.

### TDLib

This repo expects TDLib runtime files to be provided separately during development and bundled during packaging.

Planned default layout:

- runtime libraries under `vendor/tdlib/`
- writable TDLib data under the user profile

## Quick start

1. Create and activate a virtual environment.
2. Install the project with development dependencies.
3. Copy `.env.example` to `.env`.
4. Fill in Telegram API credentials from `https://my.telegram.org`.
5. Start the app.

## Portable build

The project intentionally uses **PyInstaller one-folder mode** instead of `--onefile`.

Why:

- easier debugging
- better fit for portable distribution
- cleaner update flow for downloaded release zips
- no temp extraction dance on every launch

## Planned release flow

1. Tag a version.
2. GitHub Actions builds the Windows portable bundle.
3. The workflow zips the `dist/easygram/` folder.
4. Checksums and metadata are generated.
5. Assets are attached to a GitHub Release.
6. Easygram checks the latest release and prompts users to update.

## Testing goals

- keyboard-first navigation
- predictable focus restoration
- screen-reader announcement quality
- version comparison and release parsing
- updater decision logic and asset selection

## License

MIT
