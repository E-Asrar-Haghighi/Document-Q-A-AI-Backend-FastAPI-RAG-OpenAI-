from fastapi import Header
from app.core.config import settings
from app.core.exceptions import AppException


def require_api_key(x_api_key: str | None = Header(default=None)) -> None:
    """
    Simple API key authentication dependency.

    The client must send:
        X-API-Key: <your-secret-key>

    If the key is missing or incorrect, raise a clean application error.

    Why use a FastAPI dependency?
    - reusable across endpoints
    - keeps auth logic out of route functions
    - easy to replace later with JWT or OAuth
    """

    # If the app itself is misconfigured, fail safely.
    if not settings.app_api_key:
        raise AppException(
            code="AUTH_CONFIGURATION_ERROR",
            message="API authentication is not configured correctly.",
            status_code=500
        )

    # Reject missing or incorrect keys.
    if x_api_key != settings.app_api_key:
        raise AppException(
            code="UNAUTHORIZED",
            message="Invalid or missing API key.",
            status_code=401
        )