"""TDLib authorization helpers."""

from __future__ import annotations

from teledesk.domain.models import AuthorizationState


def initial_authorization_state() -> AuthorizationState:
    return AuthorizationState(stage="wait_tdlib_parameters", hint="Configure TDLib parameters.")
