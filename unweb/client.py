"""Main UnWeb client."""
from __future__ import annotations
import httpx
from unweb.exceptions import AuthError, NotFoundError, QuotaExceededError, UnWebError, ValidationError
from unweb.resources.auth import AuthResource
from unweb.resources.convert import ConvertResource
from unweb.resources.crawl import CrawlResource
from unweb.resources.keys import KeysResource
from unweb.resources.subscription import SubscriptionResource
from unweb.resources.usage import UsageResource

_DEFAULT_BASE_URL = "https://api.unweb.info"


class UnWebClient:
    """Client for the UnWeb API."""

    def __init__(self, api_key: str | None = None, base_url: str = _DEFAULT_BASE_URL, timeout: float = 30.0):
        self._api_key = api_key
        self._base_url = base_url.rstrip("/")
        self._jwt_token: str | None = None
        self._http = httpx.Client(timeout=timeout)
        self.convert = ConvertResource(self)
        self.crawl = CrawlResource(self)
        self.auth = AuthResource(self)
        self.keys = KeysResource(self)
        self.usage = UsageResource(self)
        self.subscription = SubscriptionResource(self)

    def _request(self, method: str, path: str, *, json: dict | None = None, data: dict | None = None, files: dict | None = None, params: dict | None = None, auth_mode: str = "api_key") -> dict:
        url = f"{self._base_url}{path}"
        headers: dict[str, str] = {}
        if auth_mode == "api_key" and self._api_key:
            headers["X-API-Key"] = self._api_key
        elif auth_mode == "jwt" and self._jwt_token:
            headers["Authorization"] = f"Bearer {self._jwt_token}"

        response = self._http.request(method, url, headers=headers, json=json, data=data, files=files, params=params)

        if response.status_code == 204:
            return {}
        body = response.json() if response.content else {}
        if response.is_success:
            return body

        msg = body.get("detail") or body.get("error") or body.get("title") or str(body)
        if response.status_code == 400:
            errors = body.get("errors")
            if errors:
                msg = "; ".join(errors) if isinstance(errors, list) else str(errors)
            raise ValidationError(msg, response.status_code, body)
        if response.status_code == 401:
            raise AuthError(msg, response.status_code, body)
        if response.status_code == 403:
            raise AuthError(msg, response.status_code, body)
        if response.status_code == 404:
            raise NotFoundError(msg, response.status_code, body)
        if response.status_code == 429:
            raise QuotaExceededError(msg, response.status_code, body)
        raise UnWebError(msg, response.status_code, body)

    def close(self) -> None:
        self._http.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
