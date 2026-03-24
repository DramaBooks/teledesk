from easygram.domain.updates import ReleaseAsset, ReleaseInfo
from easygram.services.update_service import UpdateService


class DummyClient:
    def latest_release(self) -> ReleaseInfo:  # pragma: no cover - not used in these tests
        raise NotImplementedError


def test_select_portable_asset_prefers_portable_zip() -> None:
    release = ReleaseInfo(
        tag_name="v0.2.0",
        name="v0.2.0",
        html_url="https://example.invalid/release",
        body="",
        prerelease=False,
        assets=[
            ReleaseAsset(
                name="easygram-symbols.zip",
                download_url="https://example.invalid/symbols",
                size=10,
                content_type="application/zip",
            ),
            ReleaseAsset(
                name="easygram-portable-v0.2.0-windows-x64.zip",
                download_url="https://example.invalid/portable",
                size=100,
                content_type="application/zip",
            ),
        ],
    )
    service = UpdateService(DummyClient())

    asset = service.select_portable_asset(release)

    assert asset is not None
    assert asset.download_url == "https://example.invalid/portable"
