"""Basic HTML-to-Markdown conversion examples."""
from unweb import UnWebClient

client = UnWebClient(api_key="unweb_your_key_here")

# Convert HTML string
result = client.convert.paste("""
<html><body>
    <h1>Getting Started</h1>
    <p>This is a <strong>quick start</strong> guide for the UnWeb API.</p>
    <ul>
        <li>Convert HTML to Markdown</li>
        <li>Crawl documentation sites</li>
        <li>Feed clean text to your LLM</li>
    </ul>
</body></html>
""")
print("=== Paste Conversion ===")
print(result.markdown)
print(f"Quality Score: {result.quality_score}/100")

# Convert from a URL
print("\n=== URL Conversion ===")
result = client.convert.url("https://example.com")
print(result.markdown[:200])
