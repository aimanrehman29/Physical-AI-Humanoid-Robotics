import sys
from pathlib import Path

# Ensure the backend package is on the path when running as a Vercel function
BACKEND_DIR = Path(__file__).resolve().parents[1] / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.append(str(BACKEND_DIR))

# Re-export the existing FastAPI app
from app.main import app  # noqa: E402

