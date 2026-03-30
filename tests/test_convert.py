import pytest
from pytest_httpx import HTTPXMock
from unweb import UnWebClient

@pytest.fixture
def client():
    return UnWebClient(api_key="unweb_test", base_url="http://test.local")

def test_paste_returns_conversion_result(client, httpx_mock: HTTPXMock):
    httpx_mock.add_response(url="http://test.local/api/convert/paste", json={"markdown": "# Hello", "warnings": [], "qualityScore": 100})
    result = client.convert.paste("<h1>Hello</h1>")
    assert result.markdown == "# Hello"
    assert result.quality_score == 100

def test_paste_sends_api_key(client, httpx_mock: HTTPXMock):
    httpx_mock.add_response(url="http://test.local/api/convert/paste", json={"markdown": "ok", "warnings": [], "qualityScore": 95})
    client.convert.paste("<p>Test</p>")
    request = httpx_mock.get_request()
    assert request.headers["X-API-Key"] == "unweb_test"
    import json
    assert json.loads(request.content)["html"] == "<p>Test</p>"

def test_url_conversion(client, httpx_mock: HTTPXMock):
    httpx_mock.add_response(url="http://test.local/api/convert/url", json={"markdown": "# Page", "warnings": [], "qualityScore": 80})
    result = client.convert.url("https://example.com")
    assert result.markdown == "# Page"
    assert result.quality_score == 80

def test_upload(client, httpx_mock: HTTPXMock, tmp_path):
    httpx_mock.add_response(url="http://test.local/api/convert/upload", json={"markdown": "# File", "warnings": [], "qualityScore": 100})
    f = tmp_path / "test.html"
    f.write_text("<h1>File</h1>")
    result = client.convert.upload(str(f))
    assert result.markdown == "# File"
