"""UnWeb Python SDK — Convert HTML to Markdown for AI pipelines."""
from unweb.client import UnWebClient
from unweb.exceptions import AuthError, NotFoundError, QuotaExceededError, UnWebError, ValidationError

__all__ = ["UnWebClient", "UnWebError", "AuthError", "QuotaExceededError", "NotFoundError", "ValidationError"]
__version__ = "0.1.0"
