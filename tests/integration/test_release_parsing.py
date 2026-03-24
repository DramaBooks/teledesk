from easygram.integrations.github.releases_client import GitHubReleasesClient


def test_parse_release_maps_assets() -> None:
    client = GitHubReleasesClient(owner="Germano", repo="easygram")
    payload = {
        "tag_name": "v0.2.0",
        "name": "v0.2.0",
        "html_url": "https://example.invalid/release",
        "body": "notes",
        "prerelease": False,
        "assets": [
            {
                "name": "easygram-portable-v0.2.0-windows-x64.zip",
                "browser_download_url": "https://example.invalid/portable.zip",
                "size": 42,
                "content_type": "application/zip",
                "digest": "sha256:abcd",
            }
        ],
    }

    release = client._parse_release(payload)

    assert release.tag_name == "v0.2.0"
    assert release.assets[0].is_portable_bundle
    assert release.assets[0].digest == "sha256:abcd"
