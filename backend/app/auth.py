"""
Lightweight auth stubs to simulate Better Auth flows for signup/signin and profile capture.
Replace with real Better Auth integration (JWT verification) in production.
"""

from __future__ import annotations

import uuid
from typing import Dict, Optional

from pydantic import BaseModel, EmailStr


class SignupPayload(BaseModel):
    email: EmailStr
    password: str
    software_background: Optional[str] = None
    hardware_background: Optional[str] = None
    experience_level: Optional[str] = None
    preferred_language: Optional[str] = None


class SigninPayload(BaseModel):
    email: EmailStr
    password: str


class Profile(BaseModel):
    user_id: str
    email: EmailStr
    software_background: Optional[str] = None
    hardware_background: Optional[str] = None
    experience_level: Optional[str] = None
    preferred_language: Optional[str] = None


# In-memory store (demo only; replace with Neon)
_users: Dict[str, Profile] = {}
_passwords: Dict[str, str] = {}


def signup(payload: SignupPayload) -> Profile:
    if payload.email in _users:
        raise ValueError("User already exists")
    user_id = str(uuid.uuid4())
    profile = Profile(
        user_id=user_id,
        email=payload.email,
        software_background=payload.software_background,
        hardware_background=payload.hardware_background,
        experience_level=payload.experience_level,
        preferred_language=payload.preferred_language,
    )
    _users[payload.email] = profile
    _passwords[payload.email] = payload.password
    return profile


def signin(payload: SigninPayload) -> Profile:
    if payload.email not in _users:
        raise ValueError("Invalid credentials")
    if _passwords.get(payload.email) != payload.password:
        raise ValueError("Invalid credentials")
    return _users[payload.email]
