"""Use UnWeb with LangChain for RAG — crawl docs and load into a vector store."""
import time
from unweb import UnWebClient

client = UnWebClient(api_key="unweb_your_key_here")

# Crawl with LangChain export format
job = client.crawl.start("https://docs.example.com", allowed_path="/docs/", max_pages=100, export_format="langchain")
print(f"Crawl started: {job.job_id}")

while not job.is_complete:
    time.sleep(5)
    job = client.crawl.status(job.job_id)

if job.status != "Completed":
    print(f"Crawl failed: {job.error_message}")
    exit(1)

download = client.crawl.download(job.job_id)
print(f"Download JSONL: {download.download_url}")
print("\nTo use with LangChain:")
print("1. Download the JSONL file from the URL above")
print("2. Use langchain JSONLoader to load documents")
print("3. Create a vector store (FAISS, Chroma, etc.)")
print("4. Query with a retriever")
