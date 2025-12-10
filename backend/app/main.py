from __future__ import annotations

import json
import logging
import os
import uuid
from typing import Any, List, Optional

import psycopg
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings

from .rag import answer_with_retrieval
from . import agents, auth

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class Settings(BaseSettings):
    qdrant_url: str = Field(..., env="QDRANT_URL")
    qdrant_api_key: Optional[str] = Field(None, env="QDRANT_API_KEY")
    collection_name: str = Field("humanoid_ai_book", env="COLLECTION_NAME")
    cohere_api_key: Optional[str] = Field(None, env="COHERE_API_KEY")
    embed_model: str = Field("embed-english-v3.0", env="EMBED_MODEL")
    max_chars: int = Field(1200, env="MAX_CHARS")
    llm_model: Optional[str] = Field("gpt-4o-mini", env="LLM_MODEL")
    neon_database_url: Optional[str] = Field(None, env="NEON_DATABASE_URL")
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

app = FastAPI(title="Physical AI RAG Chatbot", version="0.2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Data models ---
class ChatRequest(BaseModel):
    question: str
    session_id: Optional[str] = None
    selected_text: Optional[str] = None


class Citation(BaseModel):
    chapter: str = ""
    anchor: str = ""
    url: str


class ChatResponse(BaseModel):
    answer: str
    citations: List[Citation] = []
    refused: bool = False
    session_id: str


class FeedbackRequest(BaseModel):
    question: str
    answer: str
    chunk_ids: List[str] = []
    sentiment: str = Field(..., pattern="^(up|down)$")
    session_id: Optional[str] = None


class AgentRequest(BaseModel):
    skill: str = Field(..., pattern="^(code_explain|summary)$")
    code: Optional[str] = None
    chapter_text: Optional[str] = None
    question: Optional[str] = None
    locale: Optional[str] = None
    session_id: Optional[str] = None


class AgentResponse(BaseModel):
    session_id: str
    skill: str
    answer: str
    citations: List[Citation] = []
    refused: bool = False


class SignupRequest(auth.SignupPayload):
    ...


class SigninRequest(auth.SigninPayload):
    ...


class AuthResponse(BaseModel):
    user_id: str
    email: str
    software_background: Optional[str] = None
    hardware_background: Optional[str] = None
    experience_level: Optional[str] = None
    preferred_language: Optional[str] = None


# --- Neon helpers ---
_tables_ready = False


def get_db_conn():
    if not settings.neon_database_url:
        return None
    try:
        return psycopg.connect(settings.neon_database_url, autocommit=True)
    except Exception as exc:
        logger.warning("Could not connect to Neon: %s", exc)
        return None


def ensure_tables(conn):
    global _tables_ready
    if _tables_ready or conn is None:
        return
    with conn.cursor() as cur:
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS sessions (
                id UUID PRIMARY KEY,
                created_at TIMESTAMPTZ DEFAULT now()
            );
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS messages (
                id UUID PRIMARY KEY,
                session_id UUID REFERENCES sessions(id),
                role TEXT,
                content TEXT,
                citations JSONB,
                created_at TIMESTAMPTZ DEFAULT now()
            );
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS highlights (
                id UUID PRIMARY KEY,
                session_id UUID REFERENCES sessions(id),
                raw_text TEXT,
                created_at TIMESTAMPTZ DEFAULT now()
            );
            """
        )
    _tables_ready = True


def upsert_session(conn, session_id: str):
    if conn is None:
        return
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO sessions (id) VALUES (%s) ON CONFLICT (id) DO NOTHING",
            (session_id,),
        )


def log_message(conn, session_id: str, role: str, content: str, citations: Optional[List[dict]] = None):
    if conn is None:
        return
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO messages (id, session_id, role, content, citations) VALUES (%s, %s, %s, %s, %s)",
            (str(uuid.uuid4()), session_id, role, content, json.dumps(citations or [])),
        )


def log_highlight(conn, session_id: str, raw_text: str):
    if conn is None or not raw_text:
        return
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO highlights (id, session_id, raw_text) VALUES (%s, %s, %s)",
            (str(uuid.uuid4()), session_id, raw_text),
        )


# --- Routes ---
@app.get("/health")
def health() -> dict[str, Any]:
    return {"status": "ok", "env": os.getenv("ENV", "local")}


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest) -> ChatResponse:
    if not req.question.strip():
        raise HTTPException(status_code=400, detail="Question is required")

    session_id = req.session_id or str(uuid.uuid4())

    db = get_db_conn()
    ensure_tables(db)
    upsert_session(db, session_id)
    if req.selected_text:
        log_highlight(db, session_id, req.selected_text)

    result = answer_with_retrieval(req.question, selected_text=req.selected_text)

    citations = [
        Citation(chapter="", anchor="", url=c.get("url", "")) for c in result.get("citations", [])
    ]

    log_message(db, session_id, "user", req.question)
    log_message(db, session_id, "assistant", result.get("answer", ""), result.get("citations"))

    if db:
        db.close()

    return ChatResponse(
        session_id=session_id,
        answer=result.get("answer", ""),
        citations=citations,
        refused=bool(result.get("refused", False)),
    )


@app.post("/feedback")
def feedback(req: FeedbackRequest) -> dict[str, str]:
    db = get_db_conn()
    ensure_tables(db)
    session_id = req.session_id or str(uuid.uuid4())
    upsert_session(db, session_id)
    log_message(db, session_id, "feedback", json.dumps(req.dict()), [])
    if db:
        db.close()
    return {"status": "received"}


@app.post("/agent", response_model=AgentResponse)
def agent(req: AgentRequest) -> AgentResponse:
    session_id = req.session_id or str(uuid.uuid4())
    skill = req.skill
    result = {"answer": "Skill not implemented", "citations": [], "refused": True}

    if skill == "code_explain":
        if not req.code:
            raise HTTPException(status_code=400, detail="code is required for code_explain")
        result = agents.explain_code(req.code, req.question, req.locale)
    elif skill == "summary":
        if not req.chapter_text:
            raise HTTPException(status_code=400, detail="chapter_text is required for summary")
        result = agents.summarize_text(req.chapter_text, req.locale)

    return AgentResponse(
        session_id=session_id,
        skill=skill,
        answer=result.get("answer", ""),
        citations=[
            Citation(url=c.get("url", ""), chapter=c.get("chapter", ""), anchor=c.get("anchor", ""))
            for c in result.get("citations", [])
        ],
        refused=bool(result.get("refused", False)),
    )


@app.post("/auth/signup", response_model=AuthResponse)
def auth_signup(req: SignupRequest) -> AuthResponse:
    try:
        profile = auth.signup(req)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    return AuthResponse(**profile.dict())


@app.post("/auth/signin", response_model=AuthResponse)
def auth_signin(req: SigninRequest) -> AuthResponse:
    try:
        profile = auth.signin(req)
    except ValueError as exc:
        raise HTTPException(status_code=401, detail=str(exc))
    return AuthResponse(**profile.dict())
