import logging
import os
from typing import List, Optional, Sequence

import cohere
from openai import OpenAI
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


def get_openai_client() -> Optional[OpenAI]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None
    return OpenAI(api_key=api_key)


def get_qdrant_client() -> Optional[QdrantClient]:
    url = os.getenv("QDRANT_URL")
    if not url:
        return None
    return QdrantClient(url=url, api_key=os.getenv("QDRANT_API_KEY"))


def embed_text(text: str) -> Optional[List[float]]:
    # Prefer OpenAI embeddings if available; fallback to Cohere
    oa_client = get_openai_client()
    if oa_client:
        try:
            resp = oa_client.embeddings.create(
                model=os.getenv("EMBED_MODEL", "text-embedding-3-small"),
                input=text,
            )
            return resp.data[0].embedding
        except Exception as exc:
            logger.warning("OpenAI embed failed, falling back to Cohere: %s", exc)

    co_client = get_cohere_client()
    if co_client is None:
        logger.warning("No embedding provider configured.")
        return None
    resp = co_client.embed(
        model=os.getenv("EMBED_MODEL", "embed-english-v3.0"),
        input_type="search_query",
        texts=[text],
    )
    return resp.embeddings[0]


def retrieve(query: str, top_k: int = 5, selected_text: Optional[str] = None) -> Sequence[RetrievalResult]:
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
    if selected_text:
        # Treat the user-selected text as a high-priority pseudo-result
        out.append(
            RetrievalResult(
                text=selected_text,
                url="user-selection",
                score=1.0,
            )
        )
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


def answer_with_retrieval(question: str, selected_text: Optional[str] = None) -> dict:
    hits = retrieve(question, top_k=5, selected_text=selected_text)
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

    answer_text: Optional[str] = None

    # Prefer OpenAI if available
    oa_client = get_openai_client()
    if oa_client:
        try:
            model_name = os.getenv("LLM_MODEL", "gpt-4o-mini")
            resp = oa_client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": "Answer only from the provided context. If not found, say 'I don't know'."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.2,
            )
            answer_text = resp.choices[0].message.content
        except Exception as exc:
            logger.warning("OpenAI call failed, falling back to Gemini/stitched: %s", exc, exc_info=True)

    # Gemini fallback (legacy LLM_MODEL holds Gemini key)
    if not answer_text:
        llm_api_key = os.getenv("LLM_MODEL")
        gemini_model = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
        if llm_api_key:
            try:
                endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/{gemini_model}:generateContent"
                resp = requests.post(
                    endpoint,
                    params={"key": llm_api_key},
                    json={"contents": [{"parts": [{"text": prompt}]}]},
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
