import json
import pytest
from pytest_httpx import HTTPXMock
from unweb import UnWebClient

@pytest.fixture
def client():
    c = UnWebClient(api_key="unweb_test", base_url="http://test.local")
    c._jwt_token = "jwt_test"
    return c

def test_keys_list(client, httpx_mock: HTTPXMock):
    httpx_mock.add_response(url="http://test.local/api/keys", json=[{"id": "k1", "name": "My Key", "keyPrefix": "unweb_abc", "isRevoked": False}])
    keys = client.keys.list()
    assert len(keys) == 1
    assert keys[0].name == "My Key"

def test_keys_create(client, httpx_mock: HTTPXMock):
    httpx_mock.add_response(url="http://test.local/api/keys", method="POST", json={"id": "k2", "name": "New Key", "key": "unweb_full_key", "keyPrefix": "unweb_ful"})
    key = client.keys.create("New Key")
    assert key.key == "unweb_full_key"

def test_keys_revoke(client, httpx_mock: HTTPXMock):
    httpx_mock.add_response(url="http://test.local/api/keys/k1", method="DELETE", status_code=204)
    client.keys.revoke("k1")

def test_usage_current(client, httpx_mock: HTTPXMock):
    httpx_mock.add_response(url="http://test.local/api/usage/current", json={"creditsUsed": 150, "creditsLimit": 500, "overageCreditsUsed": 0})
    usage = client.usage.current()
    assert usage.credits_used == 150
    assert usage.credits_limit == 500

def test_subscription_get(client, httpx_mock: HTTPXMock):
    httpx_mock.add_response(url="http://test.local/api/subscription", json={"tier": "Pro", "status": "Active", "monthlyCredits": 15000, "creditsUsed": 500, "allowsOverage": True})
    sub = client.subscription.get()
    assert sub.tier == "Pro"
    assert sub.monthly_credits == 15000
    assert sub.allows_overage is True
