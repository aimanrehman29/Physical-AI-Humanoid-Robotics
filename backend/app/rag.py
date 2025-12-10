import logging
import os
import logging
import os
from typing import List, Optional, Sequence

import cohere
from pydantic import BaseModel
from qdrant_client import QdrantClient
from dotenv import load_dotenv
import requests

load_dotenv()

logger = logging.getLogger(__name__)


class RetrievalResult(BaseModel):
    text: str
    url: str
    score: float


def get_cohere_client() -> Optional[cohere.Client]:
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        return None
    return cohere.Client(api_key)


def get_qdrant_client() -> Optional[QdrantClient]:
    url = os.getenv("QDRANT_URL")
    if not url:
        return None
    return QdrantClient(url=url, api_key=os.getenv("QDRANT_API_KEY"))


def embed_text(text: str) -> Optional[List[float]]:
    client = get_cohere_client()
    if client is None:
        logger.warning("COHERE_API_KEY not set; cannot embed text.")
        return None
    resp = client.embed(
        model=os.getenv("EMBED_MODEL", "embed-english-v3.0"),
        input_type="search_query",
        texts=[text],
    )
    return resp.embeddings[0]


def retrieve(query: str, top_k: int = 5) -> Sequence[RetrievalResult]:
    vec = embed_text(query)
    if vec is None:
        return []
    qdrant = get_qdrant_client()
    if qdrant is None:
        logger.warning("QDRANT_URL not set; cannot retrieve.")
        return []
    collection = os.getenv("COLLECTION_NAME", "humanoid_ai_book")
    res = qdrant.query_points(collection_name=collection, query=vec, limit=top_k)
    out: List[RetrievalResult] = []
    for point in res.points:
        payload = point.payload or {}
        out.append(
            RetrievalResult(
                text=payload.get("text", ""),
                url=payload.get("url", ""),
                score=point.score or 0.0,
            )
        )
    return out


def answer_with_retrieval(question: str) -> dict:
    hits = retrieve(question, top_k=5)
    if not hits:
        return {
            "answer": "RAG backend is not fully configured (missing Qdrant and/or Cohere).",
            "citations": [],
            "refused": True,
        }

    snippets = [h.text for h in hits[:3]]
    context_block = "\n\n".join(
        [f"- Source {i+1} ({hit.url or 'unknown'}): {hit.text}" for i, hit in enumerate(hits[:3])]
    )
    prompt = (
        "You are an AI tutor for the Physical AI & Humanoid Robotics textbook.\n"
        "Answer concisely in 3-6 sentences using ONLY the context provided.\n"
        "If the answer is not in the context, reply: 'I don't know'.\n\n"
        f"Question: {question}\n\n"
        f"Context:\n{context_block}"
    )

    llm_api_key = os.getenv("LLM_MODEL")  # user stores the Gemini key here
    gemini_model = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
    answer_text: Optional[str] = None

    if llm_api_key:
        try:
            endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/{gemini_model}:generateContent"
            resp = requests.post(
                endpoint,
                params={"key": llm_api_key},
                json={
                    "contents": [
                        {
                            "parts": [{"text": prompt}]
                        }
                    ]
                },
                timeout=20,
            )
            resp.raise_for_status()
            data = resp.json()
            answer_text = (
                data.get("candidates", [{}])[0]
                .get("content", {})
                .get("parts", [{}])[0]
                .get("text")
            )
        except Exception as exc:  # pragma: no cover - best effort logging
            logger.warning("Gemini call failed, falling back to stitched answer: %s", exc, exc_info=True)

    if not answer_text:
        answer_text = "Here is a stitched answer from retrieved content:\n" + "\n---\n".join(snippets)

    citations = [{"url": h.url, "score": h.score} for h in hits[:3] if h.url]
    return {"answer": answer_text, "citations": citations, "refused": False}
