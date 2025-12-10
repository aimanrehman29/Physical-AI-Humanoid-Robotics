"""
Ingest the textbook content into Qdrant using Cohere embeddings.
Usage:
  python scripts/ingest.py

Required env:
  SITEMAP_URL              - e.g., https://physicalhumanoidaitextbook.vercel.app/sitemap.xml
  QDRANT_URL               - Qdrant endpoint
  QDRANT_API_KEY           - Qdrant API key (if needed)
  COHERE_API_KEY           - Cohere API key
Optional env:
  COLLECTION_NAME          - defaults to "humanoid_ai_book"
  EMBED_MODEL              - defaults to "embed-english-v3.0"
  MAX_CHARS                - chunk size (default 1200)
"""

from __future__ import annotations

import os
import xml.etree.ElementTree as ET
from typing import List
from urllib.parse import urlparse, urlunparse

import requests
import trafilatura
from cohere import Client as CohereClient
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

load_dotenv()

SITEMAP_URL = os.getenv("SITEMAP_URL")
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
COLLECTION = os.getenv("COLLECTION_NAME", "humanoid_ai_book")
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
EMBED_MODEL = os.getenv("EMBED_MODEL", "embed-english-v3.0")
MAX_CHARS = int(os.getenv("MAX_CHARS", "1200"))


def require_env(name: str) -> str:
    val = os.getenv(name)
    if not val:
        raise SystemExit(f"Missing required env var: {name}")
    return val


def get_all_urls(sitemap_url: str) -> List[str]:
    resp = requests.get(sitemap_url, timeout=30)
    resp.raise_for_status()
    root = ET.fromstring(resp.text)
    urls: List[str] = []
    for child in root:
        loc_tag = child.find("{http://www.sitemaps.org/schemas/sitemap/0.9}loc")
        if loc_tag is not None and loc_tag.text:
            urls.append(loc_tag.text)
    return urls


def normalize_urls(urls: List[str], sitemap_url: str) -> List[str]:
    """Replace placeholder domains with the sitemap host and drop duplicates."""
    if not urls:
        return urls
    parsed = urlparse(sitemap_url)
    host = parsed.netloc
    scheme = parsed.scheme or "https"
    fixed: List[str] = []
    for u in urls:
        up = urlparse(u)
        if "example.com" in up.netloc or not up.netloc:
            up = up._replace(netloc=host, scheme=scheme)
        # our sitemap uses /docs/chapters/*, but the site routes are /docs/*
        if up.path.startswith("/docs/chapters/"):
            up = up._replace(path=up.path.replace("/docs/chapters/", "/docs/", 1))
        fixed.append(urlunparse(up))
    # remove duplicates while preserving order
    seen = set()
    deduped: List[str] = []
    for u in fixed:
        if u in seen:
            continue
        seen.add(u)
        deduped.append(u)
    return deduped


def extract_text_from_url(url: str) -> str:
    html = requests.get(url, timeout=30).text
    text = trafilatura.extract(html) or ""
    return text.strip()


def chunk_text(text: str, max_chars: int) -> List[str]:
    chunks: List[str] = []
    remaining = text
    while len(remaining) > max_chars:
        split_pos = remaining[:max_chars].rfind(". ")
        if split_pos == -1:
            split_pos = max_chars
        chunks.append(remaining[:split_pos].strip())
        remaining = remaining[split_pos:].strip()
    if remaining:
        chunks.append(remaining)
    return [c for c in chunks if c]


def embed(client: CohereClient, text: str) -> List[float]:
    resp = client.embed(model=EMBED_MODEL, input_type="search_query", texts=[text])
    return resp.embeddings[0]


def recreate_collection(qdrant: QdrantClient, vector_size: int = 1024) -> None:
    qdrant.recreate_collection(
        collection_name=COLLECTION,
        vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
    )


def ingest() -> None:
    require_env("SITEMAP_URL")
    require_env("QDRANT_URL")
    require_env("COHERE_API_KEY")

    cohere_client = CohereClient(COHERE_API_KEY)
    qdrant = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)

    print(f"[ingest] Fetching URLs from sitemap: {SITEMAP_URL}")
    urls_raw = get_all_urls(SITEMAP_URL)
    urls = normalize_urls(urls_raw, SITEMAP_URL)
    print(f"[ingest] Found {len(urls)} URLs after normalization")

    if not urls:
        base = urlparse(SITEMAP_URL)
        base_root = f"{base.scheme or 'https'}://{base.netloc}"
        urls = [
            f"{base_root}/docs/intro",
            f"{base_root}/docs/physical-ai",
            f"{base_root}/docs/humanoid-basics",
            f"{base_root}/docs/ros2-fundamentals",
            f"{base_root}/docs/digital-twin",
            f"{base_root}/docs/vision-language-action",
            f"{base_root}/docs/capstone",
        ]
        print(f"[ingest] Fallback URLs: {urls}")

    print(f"[ingest] Recreating collection '{COLLECTION}'")
    recreate_collection(qdrant, vector_size=1024)  # Cohere v3 English has 1024 dims

    chunk_id = 1
    for url in urls:
        print(f"[ingest] Processing {url}")
        text = extract_text_from_url(url)
        if not text:
            print("[warn] No text extracted; skipping.")
            continue
        chunks = chunk_text(text, MAX_CHARS)
        for ch in chunks:
            vector = embed(cohere_client, ch)
            qdrant.upsert(
                collection_name=COLLECTION,
                points=[
                    PointStruct(
                        id=chunk_id,
                        vector=vector,
                        payload={
                            "url": url,
                            "text": ch,
                            "chunk_id": chunk_id,
                        },
                    )
                ],
            )
            chunk_id += 1
        print(f"[ingest] Stored {len(chunks)} chunks from {url}")

    print(f"[done] Total chunks stored: {chunk_id - 1}")


if __name__ == "__main__":
    ingest()
