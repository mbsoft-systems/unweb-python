import json
import pytest
from pytest_httpx import HTTPXMock
from unweb import UnWebClient

@pytest.fixture
def client():
    return UnWebClient(api_key="unweb_test", base_url="http://test.local")

def test_login_stores_jwt(client, httpx_mock: HTTPXMock):
    httpx_mock.add_response(url="http://test.local/api/auth/login", json={"token": "jwt_abc123", "userId": "u1", "email": "user@test.com"})
    result = client.auth.login("user@test.com", "password123")
    assert result.token == "jwt_abc123"
    assert client._jwt_token == "jwt_abc123"

def test_register(client, httpx_mock: HTTPXMock):
    httpx_mock.add_response(url="http://test.local/api/auth/register", json={"token": "jwt_new", "userId": "u2", "email": "new@test.com"})
    result = client.auth.register("new@test.com", "pass123!", "First", "Last")
    assert result.token == "jwt_new"
    assert client._jwt_token == "jwt_new"

def test_me_uses_jwt(client, httpx_mock: HTTPXMock):
    client._jwt_token = "jwt_test"
    httpx_mock.add_response(url="http://test.local/api/auth/me", json={"id": "u1", "email": "user@test.com", "firstName": "Test", "lastName": "User", "role": "User"})
    profile = client.auth.me()
    assert profile.email == "user@test.com"
    assert httpx_mock.get_request().headers["Authorization"] == "Bearer jwt_test"

def test_change_password(client, httpx_mock: HTTPXMock):
    client._jwt_token = "jwt_test"
    httpx_mock.add_response(url="http://test.local/api/auth/change-password", json={})
    client.auth.change_password("old_pass", "new_pass")
    body = json.loads(httpx_mock.get_request().content)
    assert body["currentPassword"] == "old_pass"
