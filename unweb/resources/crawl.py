from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from unweb.client import UnWebClient

class CrawlResource:
    def __init__(self, client: UnWebClient):
        self._client = client
