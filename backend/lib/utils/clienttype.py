"""Device client type"""
from typing import Literal


ClientType = Literal["web", "admin-web", "partner-web", "mobile"]

ALLOWED_CLIENT_TYPES: set[str] = {"web", "admin-web", "partner-web", "mobile"}


def validate_client_type(raw_type: str) -> ClientType:
    """Valid device/client type"""
    if raw_type not in ALLOWED_CLIENT_TYPES:
        raise ValueError("Invalid client type")
    return raw_type  # type: ignore  # safe after validation
