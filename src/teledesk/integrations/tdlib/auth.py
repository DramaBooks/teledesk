"""TDLib authorization helpers."""

from __future__ import annotations

from teledesk.domain.models import AuthorizationState


def initial_authorization_state() -> AuthorizationState:
    return AuthorizationState(stage="wait_tdlib_parameters", hint="Configure TDLib parameters.")


def build_tdlib_parameters_query(
    *,
    api_id: int,
    api_hash: str,
    database_directory: str,
    files_directory: str,
    device_model: str = "Teledesk",
    system_language_code: str = "en",
    application_version: str = "0.1.0",
) -> dict[str, object]:
    return {
        "@type": "setTdlibParameters",
        "parameters": {
            "use_test_dc": False,
            "database_directory": database_directory,
            "files_directory": files_directory,
            "use_file_database": True,
            "use_chat_info_database": True,
            "use_message_database": True,
            "use_secret_chats": True,
            "api_id": api_id,
            "api_hash": api_hash,
            "system_language_code": system_language_code,
            "device_model": device_model,
            "application_version": application_version,
        },
    }


def build_phone_number_query(phone_number: str) -> dict[str, object]:
    return {"@type": "setAuthenticationPhoneNumber", "phone_number": phone_number}


def build_auth_code_query(code: str) -> dict[str, object]:
    return {"@type": "checkAuthenticationCode", "code": code}


def build_password_query(password: str) -> dict[str, object]:
    return {"@type": "checkAuthenticationPassword", "password": password}
