"""
FastAPI skeleton for the Physical AI & Humanoid Robotics RAG chatbot.
This is a minimal starting point: wiring for config, health, chat, and feedback.
RAG plumbing (ingestion, retrieval, LLM calls) should be added in app/services.
"""

from __future__ import annotations

import logging
import os
from typing import Any, List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings

from app.rag import answer_with_retrieval

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class Settings(BaseSettings):
    qdrant_url: str = Field(..., env="QDRANT_URL")
    qdrant_api_key: Optional[str] = Field(None, env="QDRANT_API_KEY")
    collection_name: str = Field("humanoid_ai_book", env="COLLECTION_NAME")
    cohere_api_key: Optional[str] = Field(None, env="COHERE_API_KEY")
    embed_model: str = Field("embed-english-v3.0", env="EMBED_MODEL")
    max_chars: int = Field(1200, env="MAX_CHARS")
    llm_model: Optional[str] = Field(None, env="LLM_MODEL")  # not used yet
    allowed_origins_raw: Optional[str] = Field(None, env="ALLOWED_ORIGINS")

    @property
    def allowed_origins(self) -> List[str]:
        if not self.allowed_origins_raw:
            return ["*"]
        return [o.strip() for o in self.allowed_origins_raw.split(",") if o.strip()]

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()

app = FastAPI(title="Physical AI RAG Chatbot", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    question: str
    session_id: Optional[str] = None


class Citation(BaseModel):
    chapter: str
    anchor: str
    url: str


class ChatResponse(BaseModel):
    answer: str
    citations: List[Citation] = []
    refused: bool = False


class FeedbackRequest(BaseModel):
    question: str
    answer: str
    chunk_ids: List[str] = []
    sentiment: str = Field(..., pattern="^(up|down)$")
    session_id: Optional[str] = None


@app.get("/health")
def health() -> dict[str, Any]:
    return {"status": "ok", "env": os.getenv("ENV", "local")}


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest) -> ChatResponse:
    if not req.question.strip():
        raise HTTPException(status_code=400, detail="Question is required")
    result = answer_with_retrieval(req.question)
    return ChatResponse(
        answer=result.get("answer", ""),
        citations=[
          Citation(chapter="", anchor="", url=c.get("url", "")) for c in result.get("citations", [])
        ],
        refused=bool(result.get("refused", False)),
    )


@app.post("/feedback")
def feedback(req: FeedbackRequest) -> dict[str, str]:
    # Placeholder: insert into Neon Postgres.
    logger.info("Feedback received: %s", req.dict())
    return {"status": "received"}
