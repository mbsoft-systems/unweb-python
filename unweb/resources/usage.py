"""Usage resource."""
from __future__ import annotations
from typing import TYPE_CHECKING
from unweb.models import UsageCurrent

if TYPE_CHECKING:
    from unweb.client import UnWebClient


class UsageResource:
    def __init__(self, client: UnWebClient):
        self._client = client

    def current(self) -> UsageCurrent:
        data = self._client._request("GET", "/api/usage/current", auth_mode="jwt")
        return UsageCurrent(credits_used=data.get("creditsUsed", 0), credits_limit=data.get("creditsLimit", 0), overage_credits_used=data.get("overageCreditsUsed", 0), billing_cycle_start=data.get("billingCycleStart"), billing_cycle_end=data.get("billingCycleEnd"))

    def stats(self) -> dict:
        return self._client._request("GET", "/api/usage/stats", auth_mode="jwt")

    def history(self) -> dict:
        return self._client._request("GET", "/api/usage/history", auth_mode="jwt")
