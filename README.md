# UnWeb Python SDK

[![CI](https://github.com/mbsoft-systems/unweb-python/actions/workflows/ci.yml/badge.svg)](https://github.com/mbsoft-systems/unweb-python/actions/workflows/ci.yml)
[![PyPI version](https://img.shields.io/pypi/v/unweb.svg)](https://pypi.org/project/unweb/)
[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

Python SDK for the [UnWeb API](https://unweb.info) — convert HTML to clean, LLM-ready Markdown for RAG pipelines, AI agents, and documentation ingestion.

## Installation

```bash
pip install unweb
```

## Quick Start

```python
from unweb import UnWebClient

client = UnWebClient(api_key="unweb_your_key_here")

# Convert HTML to Markdown
result = client.convert.paste("<h1>Hello World</h1><p>Clean markdown output.</p>")
print(result.markdown)       # "# Hello World\n\nClean markdown output."
print(result.quality_score)  # 100

# Convert a webpage
result = client.convert.url("https://example.com/article")
print(result.markdown)

# Upload an HTML file
result = client.convert.upload("page.html")
print(result.markdown)
```

Get your free API key at [app.unweb.info](https://app.unweb.info) (500 credits/month, no credit card required).

## Features

- **Conversions** - Paste HTML, fetch URLs, or upload files. Returns clean CommonMark with quality scores.
- **Web Crawler** - Crawl entire documentation sites with BFS traversal. Export as raw Markdown, LangChain JSONL, or LlamaIndex JSON.
- **Webhook Notifications** - Get notified when crawl jobs complete via HTTPS webhooks.
- **Dashboard Access** - Manage API keys, view usage, and handle subscriptions programmatically.
- **Quality Scores** - Every conversion returns a 0-100 quality score detecting JS-rendered pages and content extraction issues.

## API Reference

### Conversions

All conversion methods return a `ConversionResult` with `markdown`, `warnings`, and `quality_score`.

```python
from unweb import UnWebClient

client = UnWebClient(api_key="unweb_...")

# Paste raw HTML
result = client.convert.paste("<h1>Title</h1><p>Content</p>")
result.markdown       # "# Title\n\nContent"
result.quality_score  # 0-100
result.warnings       # ["Content auto-detected using: <main> element"]

# Convert from URL (fetches and converts server-side)
result = client.convert.url("https://docs.python.org/3/tutorial/index.html")

# Upload an HTML file
result = client.convert.upload("./downloaded-page.html")
```

### Web Crawler

Crawl documentation sites and download results as a ZIP archive.

```python
import time

# Start a crawl job
job = client.crawl.start(
    "https://docs.example.com",
    allowed_path="/docs/",      # Only crawl URLs under this path
    max_pages=100,               # Page limit
    export_format="raw-md",      # "raw-md", "langchain", or "llamaindex"
    webhook_url="https://your-app.com/hooks/crawl",  # Optional completion webhook
)
print(f"Job started: {job.job_id}")  # Job ID for polling

# Poll until complete
while not job.is_complete:
    time.sleep(5)
    job = client.crawl.status(job.job_id)
    print(f"  {job.status}: {job.pages_crawled} pages crawled")

# Download results
if job.status == "Completed":
    download = client.crawl.download(job.job_id)
    print(f"Download ZIP: {download.download_url}")
    print(f"Size: {download.size_bytes} bytes")

# List all your crawl jobs
jobs = client.crawl.list(status="Completed")
for j in jobs.jobs:
    print(f"  {j.job_id}: {j.pages_crawled} pages")

# Cancel a running job
client.crawl.cancel(job.job_id)
```

**Export formats:**
| Format | Output | Use case |
|--------|--------|----------|
| `raw-md` | ZIP with `.md` files + manifest | General purpose |
| `langchain` | JSONL compatible with LangChain document loaders | RAG with LangChain |
| `llamaindex` | JSON compatible with LlamaIndex readers | RAG with LlamaIndex |

### Authentication

The SDK uses **API keys** for conversion and crawler endpoints (set once in the constructor). For dashboard endpoints (usage, keys, subscription), authenticate with email/password to get a JWT:

```python
# API key auth (conversions + crawler) - set in constructor
client = UnWebClient(api_key="unweb_...")

# JWT auth (dashboard endpoints) - login first
client.auth.login("you@example.com", "your-password")

# Now dashboard endpoints work
usage = client.usage.current()
keys = client.keys.list()
```

```python
# Register a new account
token = client.auth.register("new@example.com", "password", "First", "Last")

# Get current user profile
profile = client.auth.me()
print(f"{profile.first_name} ({profile.email})")

# Update profile
client.auth.update_profile(first_name="NewName")

# Change password
client.auth.change_password("old-password", "new-password")
```

### API Key Management

Requires JWT auth (`client.auth.login(...)` first).

```python
# List API keys
keys = client.keys.list()
for key in keys:
    print(f"  {key.name}: {key.key_prefix}...")

# Create a new API key (full key only shown once)
new_key = client.keys.create("Production Key")
print(f"Key: {new_key.key}")  # Save this — not retrievable later

# Revoke an API key
client.keys.revoke(key_id="...")
```

### Usage Tracking

Requires JWT auth.

```python
usage = client.usage.current()
print(f"Credits used: {usage.credits_used}/{usage.credits_limit}")
print(f"Overage: {usage.overage_credits_used}")
print(f"Billing cycle: {usage.billing_cycle_start} - {usage.billing_cycle_end}")

# Detailed stats and history (returns raw dict)
stats = client.usage.stats()
history = client.usage.history()
```

### Subscription

Requires JWT auth.

```python
sub = client.subscription.get()
print(f"Tier: {sub.tier}")            # Free, Starter, Pro, Scale
print(f"Credits: {sub.credits_used}/{sub.monthly_credits}")
print(f"Overage: {sub.allows_overage}")

# Get a checkout URL to upgrade
url = client.subscription.checkout("Pro")
print(f"Upgrade: {url}")

# Cancel subscription
client.subscription.cancel()
```

## Error Handling

The SDK raises typed exceptions for API errors:

```python
from unweb import UnWebClient, UnWebError, AuthError, QuotaExceededError, ValidationError, NotFoundError

client = UnWebClient(api_key="unweb_...")

try:
    result = client.convert.paste("")
except ValidationError as e:
    print(f"Bad request: {e}")           # 400
except AuthError as e:
    print(f"Auth failed: {e}")           # 401/403
except QuotaExceededError as e:
    print(f"Quota exceeded: {e}")        # 429
except NotFoundError as e:
    print(f"Not found: {e}")             # 404
except UnWebError as e:
    print(f"API error ({e.status_code}): {e}")

# All exceptions have:
# e.status_code  - HTTP status code
# e.response     - Raw response body dict
```

## Configuration

```python
client = UnWebClient(
    api_key="unweb_...",                       # API key for conversions/crawler
    base_url="https://api.unweb.info",         # Default API URL
    timeout=30.0,                              # Request timeout in seconds
)

# Use as context manager for automatic cleanup
with UnWebClient(api_key="unweb_...") as client:
    result = client.convert.paste("<h1>Hello</h1>")
```

## Pricing

| Tier | Credits/month | Price |
|------|--------------|-------|
| Free | 500 | $0 |
| Starter | 2,000 | $12/mo |
| Pro | 15,000 | $39/mo |
| Scale | 60,000 | $99/mo |

Different operations cost different credits. Paid plans include overage billing so your pipelines never stop. See [unweb.info](https://unweb.info) for details.

## Links

- [UnWeb Homepage](https://unweb.info)
- [API Documentation](https://docs.unweb.info)
- [Dashboard](https://app.unweb.info) (get your API key)
- [Report Issues](https://github.com/mbsoft-systems/unweb-python/issues)

## License

MIT - see [LICENSE](LICENSE) for details.
