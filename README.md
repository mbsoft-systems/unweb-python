# UnWeb Python SDK

[![CI](https://github.com/mbsoft-systems/unweb-python/actions/workflows/ci.yml/badge.svg)](https://github.com/mbsoft-systems/unweb-python/actions/workflows/ci.yml)
[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

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
