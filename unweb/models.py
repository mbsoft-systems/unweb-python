"""Response models for the UnWeb API."""
from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class ConversionResult:
    markdown: str
    warnings: list[str] = field(default_factory=list)
    quality_score: int = 100


@dataclass
class CrawlJob:
    job_id: str
    status: str
    pages_crawled: int = 0
    pages_queued: int = 0
    start_url: str = ""
    allowed_path: str = ""
    max_pages: int = 0
    export_format: str = ""
    error_message: str | None = None
    created_at: str | None = None
    started_at: str | None = None
    completed_at: str | None = None
    duration_seconds: float | None = None
    output_size_bytes: int | None = None

    @property
    def is_complete(self) -> bool:
        return self.status in ("Completed", "Failed", "Cancelled")


@dataclass
class CrawlJobList:
    jobs: list[CrawlJob] = field(default_factory=list)
    total_count: int = 0


@dataclass
class CrawlDownload:
    download_url: str
    expires_at: str | None = None
    size_bytes: int | None = None
    content_type: str = "application/zip"
    file_name: str = ""


@dataclass
class AuthToken:
    token: str
    user_id: str = ""
    email: str = ""


@dataclass
class UserProfile:
    id: str
    email: str
    first_name: str = ""
    last_name: str = ""
    role: str = ""


@dataclass
class ApiKey:
    id: str
    name: str
    key_prefix: str = ""
    created_at: str | None = None
    last_used_at: str | None = None
    is_revoked: bool = False


@dataclass
class ApiKeyCreated:
    id: str
    name: str
    key: str
    key_prefix: str = ""


@dataclass
class UsageCurrent:
    credits_used: int = 0
    credits_limit: int = 0
    overage_credits_used: int = 0
    billing_cycle_start: str | None = None
    billing_cycle_end: str | None = None


@dataclass
class Subscription:
    tier: str = "Free"
    status: str = ""
    monthly_credits: int = 0
    credits_used: int = 0
    allows_overage: bool = False
