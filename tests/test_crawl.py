import json
import pytest
from pytest_httpx import HTTPXMock
from unweb import UnWebClient

@pytest.fixture
def client():
    return UnWebClient(api_key="unweb_test", base_url="http://test.local")

def test_start_crawl(client, httpx_mock: HTTPXMock):
    httpx_mock.add_response(url="http://test.local/api/crawl", method="POST", json={"jobId": "abc-123", "status": "Queued", "pagesCrawled": 0, "pagesQueued": 0, "startUrl": "https://docs.example.com", "allowedPath": "/docs/", "maxPages": 50, "exportFormat": "raw-md"}, status_code=202)
    job = client.crawl.start("https://docs.example.com", allowed_path="/docs/", max_pages=50)
    assert job.job_id == "abc-123"
    assert job.status == "Queued"

def test_start_crawl_with_webhook(client, httpx_mock: HTTPXMock):
    httpx_mock.add_response(url="http://test.local/api/crawl", method="POST", json={"jobId": "abc-123", "status": "Queued"}, status_code=202)
    client.crawl.start("https://example.com", webhook_url="https://myapp.com/hooks/crawl")
    body = json.loads(httpx_mock.get_request().content)
    assert body["webhookUrl"] == "https://myapp.com/hooks/crawl"

def test_status(client, httpx_mock: HTTPXMock):
    httpx_mock.add_response(url="http://test.local/api/crawl/abc-123/status", json={"jobId": "abc-123", "status": "Running", "pagesCrawled": 5, "pagesQueued": 10})
    job = client.crawl.status("abc-123")
    assert job.status == "Running"
    assert job.pages_crawled == 5

def test_list_jobs(client, httpx_mock: HTTPXMock):
    httpx_mock.add_response(url="http://test.local/api/crawl?skip=0&take=20", method="GET", json={"jobs": [{"jobId": "j1", "status": "Completed"}, {"jobId": "j2", "status": "Running"}], "totalCount": 2, "skip": 0, "take": 20})
    result = client.crawl.list()
    assert result.total_count == 2
    assert len(result.jobs) == 2

def test_download(client, httpx_mock: HTTPXMock):
    httpx_mock.add_response(url="http://test.local/api/crawl/abc-123/download", json={"downloadUrl": "https://blob.azure.net/crawls/abc.zip", "sizeBytes": 1024, "contentType": "application/zip", "fileName": "crawl.zip"})
    dl = client.crawl.download("abc-123")
    assert dl.size_bytes == 1024

def test_cancel(client, httpx_mock: HTTPXMock):
    httpx_mock.add_response(url="http://test.local/api/crawl/abc-123", method="DELETE", status_code=204)
    client.crawl.cancel("abc-123")
