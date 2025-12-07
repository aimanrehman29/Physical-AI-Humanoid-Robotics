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

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class Settings(BaseSettings):
    qdrant_url: str = Field(..., env="QDRANT_URL")
    qdrant_api_key: Optional[str] = Field(None, env="QDRANT_API_KEY")
    postgres_url: str = Field(..., env="POSTGRES_URL")  # Neon
    embed_model: str = Field("all-MiniLM-L6-v2", env="EMBED_MODEL")
    llm_model: str = Field("gpt-4o-mini", env="LLM_MODEL")
    allowed_origins: List[str] = Field(default_factory=lambda: ["*"], env="ALLOWED_ORIGINS")

    class Config:
        env_file = ".env"


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
    sentiment: str = Field(..., regex="^(up|down)$")
    session_id: Optional[str] = None


@app.get("/health")
def health() -> dict[str, Any]:
    return {"status": "ok", "env": os.getenv("ENV", "local")}


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest) -> ChatResponse:
    if not req.question.strip():
        raise HTTPException(status_code=400, detail="Question is required")
    # Placeholder: integrate retrieval + LLM. For now, refuse gracefully.
    return ChatResponse(
        answer="This chatbot answers from the textbook content. The backend RAG pipeline is not wired yet.",
        citations=[],
        refused=True,
    )


@app.post("/feedback")
def feedback(req: FeedbackRequest) -> dict[str, str]:
    # Placeholder: insert into Neon Postgres.
    logger.info("Feedback received: %s", req.dict())
    return {"status": "received"}
