from teledesk.config.version import AppVersion


def test_version_comparison_detects_newer_release() -> None:
    assert AppVersion("0.2.0").is_newer_than(AppVersion("0.1.0"))


def test_version_comparison_rejects_same_version() -> None:
    assert not AppVersion("0.1.0").is_newer_than(AppVersion("0.1.0"))
