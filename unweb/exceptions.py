"""UnWeb SDK exceptions."""
from __future__ import annotations


class UnWebError(Exception):
    """Base exception for UnWeb SDK errors."""
    def __init__(self, message: str, status_code: int | None = None, response: dict | None = None):
        super().__init__(message)
        self.status_code = status_code
        self.response = response


class AuthError(UnWebError):
    """Authentication or authorization error (401/403)."""


class QuotaExceededError(UnWebError):
    """Usage quota exceeded (429)."""


class NotFoundError(UnWebError):
    """Resource not found (404)."""


class ValidationError(UnWebError):
    """Request validation error (400)."""
