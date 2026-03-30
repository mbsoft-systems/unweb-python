"""Subscription resource."""
from __future__ import annotations
from typing import TYPE_CHECKING
from unweb.models import Subscription

if TYPE_CHECKING:
    from unweb.client import UnWebClient


class SubscriptionResource:
    def __init__(self, client: UnWebClient):
        self._client = client

    def get(self) -> Subscription:
        data = self._client._request("GET", "/api/subscription", auth_mode="jwt")
        return Subscription(tier=data.get("tier", "Free"), status=data.get("status", ""), monthly_credits=data.get("monthlyCredits", 0), credits_used=data.get("creditsUsed", 0), allows_overage=data.get("allowsOverage", False))

    def checkout(self, tier: str) -> str:
        data = self._client._request("POST", "/api/subscription/checkout", json={"tier": tier}, auth_mode="jwt")
        return data.get("checkoutUrl", "")

    def cancel(self) -> None:
        self._client._request("POST", "/api/subscription/cancel", auth_mode="jwt")
