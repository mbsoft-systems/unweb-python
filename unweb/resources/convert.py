"""Conversion resource — paste, upload, url endpoints."""
from __future__ import annotations
from pathlib import Path
from typing import TYPE_CHECKING
from unweb.models import ConversionResult

if TYPE_CHECKING:
    from unweb.client import UnWebClient


class ConvertResource:
    def __init__(self, client: UnWebClient):
        self._client = client

    def paste(self, html: str) -> ConversionResult:
        """Convert HTML string to Markdown."""
        data = self._client._request("POST", "/api/convert/paste", json={"html": html})
        return _to_result(data)

    def url(self, url: str) -> ConversionResult:
        """Fetch a URL and convert its HTML to Markdown."""
        data = self._client._request("POST", "/api/convert/url", json={"url": url})
        return _to_result(data)

    def upload(self, file_path: str) -> ConversionResult:
        """Upload an HTML file and convert to Markdown."""
        path = Path(file_path)
        with open(path, "rb") as f:
            data = self._client._request("POST", "/api/convert/upload", files={"file": (path.name, f, "text/html")})
        return _to_result(data)


def _to_result(data: dict) -> ConversionResult:
    return ConversionResult(
        markdown=data.get("markdown", ""),
        warnings=data.get("warnings", []),
        quality_score=data.get("qualityScore", 100),
    )
