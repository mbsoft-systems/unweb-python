"""Crawl a documentation site and download the results."""
import time
from unweb import UnWebClient

client = UnWebClient(api_key="unweb_your_key_here")

job = client.crawl.start("https://docs.example.com", allowed_path="/docs/", max_pages=50)
print(f"Crawl started: job {job.job_id}")

while not job.is_complete:
    time.sleep(5)
    job = client.crawl.status(job.job_id)
    print(f"  Status: {job.status} — {job.pages_crawled} pages crawled")

if job.status == "Completed":
    download = client.crawl.download(job.job_id)
    print(f"\nDownload: {download.download_url}")
else:
    print(f"\nCrawl failed: {job.error_message}")
