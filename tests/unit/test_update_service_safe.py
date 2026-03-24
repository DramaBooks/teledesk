import requests

from teledesk.domain.updates import ReleaseInfo
from teledesk.services.update_service import UpdateService


class FailingClient:
    def latest_release(self) -> ReleaseInfo:
        raise requests.RequestException("boom")


def test_safe_update_check_returns_reason_on_request_failure() -> None:
    service = UpdateService(FailingClient())

    result = service.check_for_updates_safely()

    assert result.update_available is False
    assert "Update check failed" in result.reason
