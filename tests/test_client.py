import pytest
from unweb import UnWebClient


def test_client_requires_api_key():
    client = UnWebClient(api_key="unweb_test123")
    assert client._api_key == "unweb_test123"


def test_client_default_base_url():
    client = UnWebClient(api_key="unweb_test")
    assert client._base_url == "https://api.unweb.info"


def test_client_custom_base_url():
    client = UnWebClient(api_key="unweb_test", base_url="http://localhost:5000")
    assert client._base_url == "http://localhost:5000"


def test_client_has_resource_accessors():
    client = UnWebClient(api_key="unweb_test")
    assert hasattr(client, "convert")
    assert hasattr(client, "crawl")
    assert hasattr(client, "auth")
    assert hasattr(client, "keys")
    assert hasattr(client, "usage")
    assert hasattr(client, "subscription")


def test_client_strips_trailing_slash():
    client = UnWebClient(api_key="unweb_test", base_url="http://localhost:5000/")
    assert client._base_url == "http://localhost:5000"
