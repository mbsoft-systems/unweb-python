# UnWeb Python SDK

Python SDK for the [UnWeb API](https://unweb.info) — convert HTML to clean, LLM-ready Markdown.

## Installation

```bash
pip install unweb
```

## Quick Start

```python
from unweb import UnWebClient

client = UnWebClient(api_key="unweb_your_key_here")

# Convert HTML to Markdown
result = client.convert.paste("<h1>Hello World</h1>")
print(result.markdown)
print(f"Quality: {result.quality_score}/100")

# Convert a URL
result = client.convert.url("https://example.com")

# Crawl a documentation site
job = client.crawl.start("https://docs.example.com", allowed_path="/docs/", max_pages=50)
```

## License

MIT
