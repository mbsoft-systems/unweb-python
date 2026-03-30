"""Crawler resource — start, status, download, list, cancel endpoints."""
from __future__ import annotations
from typing import TYPE_CHECKING
from unweb.models import CrawlDownload, CrawlJob, CrawlJobList

if TYPE_CHECKING:
    from unweb.client import UnWebClient


class CrawlResource:
    def __init__(self, client: UnWebClient):
        self._client = client

    def start(self, start_url: str, *, allowed_path: str = "/", max_pages: int = 100, export_format: str = "raw-md", ignore_robots_txt: bool = False, webhook_url: str | None = None) -> CrawlJob:
        """Start a new crawl job."""
        body: dict = {"startUrl": start_url, "allowedPath": allowed_path, "maxPages": max_pages, "exportFormat": export_format, "ignoreRobotsTxt": ignore_robots_txt}
        if webhook_url:
            body["webhookUrl"] = webhook_url
        data = self._client._request("POST", "/api/crawl", json=body)
        return _to_job(data)

    def status(self, job_id: str) -> CrawlJob:
        """Get the status of a crawl job."""
        data = self._client._request("GET", f"/api/crawl/{job_id}/status")
        return _to_job(data)

    def list(self, *, status: str | None = None, skip: int = 0, take: int = 20) -> CrawlJobList:
        """List crawl jobs."""
        params: dict = {"skip": skip, "take": take}
        if status:
            params["status"] = status
        data = self._client._request("GET", "/api/crawl", params=params)
        return CrawlJobList(jobs=[_to_job(j) for j in data.get("jobs", [])], total_count=data.get("totalCount", 0))

    def download(self, job_id: str) -> CrawlDownload:
        """Get download info for a completed crawl."""
        data = self._client._request("GET", f"/api/crawl/{job_id}/download")
        return CrawlDownload(download_url=data.get("downloadUrl", ""), expires_at=data.get("expiresAt"), size_bytes=data.get("sizeBytes"), content_type=data.get("contentType", "application/zip"), file_name=data.get("fileName", ""))

    def cancel(self, job_id: str) -> None:
        """Cancel a running or queued crawl job."""
        self._client._request("DELETE", f"/api/crawl/{job_id}")


def _to_job(data: dict) -> CrawlJob:
    return CrawlJob(job_id=data.get("jobId", ""), status=data.get("status", ""), pages_crawled=data.get("pagesCrawled", 0), pages_queued=data.get("pagesQueued", 0), start_url=data.get("startUrl", ""), allowed_path=data.get("allowedPath", ""), max_pages=data.get("maxPages", 0), export_format=data.get("exportFormat", ""), error_message=data.get("errorMessage"), created_at=data.get("createdAt"), started_at=data.get("startedAt"), completed_at=data.get("completedAt"), duration_seconds=data.get("durationSeconds"), output_size_bytes=data.get("outputSizeBytes"))
