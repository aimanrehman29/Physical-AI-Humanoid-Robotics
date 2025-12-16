"""
Vercel serverless entrypoint for the backend.
Place this repository root to the backend folder when deploying only the API.
"""

from app.main import app  # FastAPI application
