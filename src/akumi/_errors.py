# AUTO-GENERATED runtime, copied by akumi/codegen. Do not edit by hand.
from __future__ import annotations

from typing import Any


class AkumiError(Exception):
    """Base class for every error raised by the SDK."""


class ApiError(AkumiError):
    """An error returned by the API. Carries the HTTP status and decoded body."""

    def __init__(
        self, message: str, status: int, body: dict[str, Any] | None = None
    ) -> None:
        super().__init__(message)
        self.status = status
        self.body: dict[str, Any] = body if body is not None else {}


class AuthenticationError(ApiError):
    """Raised on a 401 or 403 response."""


class RateLimitError(ApiError):
    """Raised on a 429 response."""


class InvalidRequestError(ApiError):
    """Raised on a 4xx response that is not 401, 403, or 429."""


def _message_for(status: int, body: dict[str, Any]) -> str:
    error = body.get("error")
    if isinstance(error, dict):
        message = error.get("message")
        if isinstance(message, str):
            return message
    return f"HTTP {status}"


def map_error(status: int, body: dict[str, Any]) -> ApiError:
    """Map an HTTP status and decoded body onto the matching typed exception."""
    message = _message_for(status, body)
    if status in (401, 403):
        return AuthenticationError(message, status, body)
    if status == 429:
        return RateLimitError(message, status, body)
    if 400 <= status < 500:
        return InvalidRequestError(message, status, body)
    return ApiError(message, status, body)
