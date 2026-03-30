"""API key management resource."""
from __future__ import annotations
from typing import TYPE_CHECKING
from unweb.models import ApiKey, ApiKeyCreated

if TYPE_CHECKING:
    from unweb.client import UnWebClient


class KeysResource:
    def __init__(self, client: UnWebClient):
        self._client = client

    def list(self) -> list[ApiKey]:
        data = self._client._request("GET", "/api/keys", auth_mode="jwt")
        return [ApiKey(id=k.get("id", ""), name=k.get("name", ""), key_prefix=k.get("keyPrefix", ""), created_at=k.get("createdAt"), last_used_at=k.get("lastUsedAt"), is_revoked=k.get("isRevoked", False)) for k in data]

    def create(self, name: str) -> ApiKeyCreated:
        data = self._client._request("POST", "/api/keys", json={"name": name}, auth_mode="jwt")
        return ApiKeyCreated(id=data.get("id", ""), name=data.get("name", ""), key=data.get("key", ""), key_prefix=data.get("keyPrefix", ""))

    def revoke(self, key_id: str) -> None:
        self._client._request("DELETE", f"/api/keys/{key_id}", auth_mode="jwt")
