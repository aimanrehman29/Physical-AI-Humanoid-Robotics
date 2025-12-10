import os
import logging
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from anthropic import Anthropic

logger = logging.getLogger(__name__)

ANTHROPIC_KEY = os.getenv("ANTHROPIC_API_KEY")
CLAUDE_MODEL = os.getenv("CLAUDE_MODEL", "claude-3-5-sonnet-latest")
CLAUDE_CODE_MODEL = os.getenv("CLAUDE_CODE_MODEL", CLAUDE_MODEL)


class AgentResult(BaseModel):
    answer: str
    citations: List[Dict[str, Any]] = []
    refused: bool = False


def _client() -> Optional[Anthropic]:
    if not ANTHROPIC_KEY:
        logger.warning("ANTHROPIC_API_KEY missing; returning stubbed response")
        return None
    return Anthropic(api_key=ANTHROPIC_KEY)


def _build_messages(prompt: str, content: str, locale: Optional[str] = None):
    system = (
        "You are a concise tutor for the Physical AI & Humanoid Robotics textbook. "
        "Answer briefly, cite source labels when given, and say 'I don't know' when unsure."
    )
    if locale == "ur":
        system += " Respond in Urdu."
    return dict(
        model=CLAUDE_MODEL,
        max_tokens=400,
        system=system,
        messages=[{"role": "user", "content": f"{prompt}\n\n{content}"}],
    )


def explain_code(code: str, question: Optional[str] = None, locale: Optional[str] = None) -> Dict[str, Any]:
    cli = _client()
    question_part = f"Question: {question}\n\n" if question else ""
    if not cli:
        return AgentResult(answer="Claude unavailable; please configure ANTHROPIC_API_KEY.", refused=True).dict()
    try:
        resp = cli.messages.create(
            **_build_messages(
                prompt="Explain the following code for a robotics learner.",
                content=f"{question_part}Code:\n{code}",
                locale=locale,
            )
        )
        text = resp.content[0].text if resp.content else ""
        return AgentResult(answer=text).dict()
    except Exception as exc:
        logger.warning("Claude code_explain failed: %s", exc)
        return AgentResult(answer="I don't know.", refused=True).dict()


def summarize_text(text: str, locale: Optional[str] = None) -> Dict[str, Any]:
    cli = _client()
    if not cli:
        return AgentResult(answer="Claude unavailable; please configure ANTHROPIC_API_KEY.", refused=True).dict()
    try:
        resp = cli.messages.create(
            **_build_messages(
                prompt="Summarize this textbook passage in 5 bullet points.",
                content=text,
                locale=locale,
            )
        )
        summary = resp.content[0].text if resp.content else ""
        return AgentResult(answer=summary).dict()
    except Exception as exc:
        logger.warning("Claude summary failed: %s", exc)
        return AgentResult(answer="I don't know.", refused=True).dict()
