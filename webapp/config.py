"""Database configuration — reads DATABASE_URL or falls back to individual env vars."""
import os
import sys
from urllib.parse import urlparse

from dotenv import load_dotenv

# Ensure the repo root (parent of webapp/) is on sys.path so that `modules.*` imports work
_repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _repo_root not in sys.path:
    sys.path.insert(0, _repo_root)

# Load .env only when not running on Render (local development).
# When running locally, override=True ensures REPO .env values win over
# any system-level DB_* vars (e.g. Supabase) that may already be set.
_env_path = os.path.join(_repo_root, ".env")
_has_render_env = bool(os.getenv("DATABASE_URL"))
if not _has_render_env and os.path.isfile(_env_path):
    load_dotenv(dotenv_path=_env_path, override=True)


def _build_db_config() -> dict:
    """Return a psycopg2-compatible dict taken from DATABASE_URL or individual env vars."""
    raw = os.getenv("DATABASE_URL", "")

    if raw:
        # Accept both 'postgres://' and 'postgresql://' schemes
        if raw.startswith("postgres://"):
            raw = raw.replace("postgres://", "postgresql://", 1)
        parsed = urlparse(raw)
        return {
            "host":     parsed.hostname or "localhost",
            "database": parsed.path.lstrip("/") or "payroll",
            "user":     parsed.username or "postgres",
            "password": parsed.password or "admin",
            "port":     str(parsed.port or 5432),
        }

    return {
        "host":     os.getenv("DB_HOST", "localhost"),
        "database": os.getenv("DB_NAME", "payroll"),
        "user":     os.getenv("DB_USER", "postgres"),
        "password": os.getenv("DB_PASSWORD", "admin"),
        "port":     os.getenv("DB_PORT", "5432"),
    }


DB_CONFIG = _build_db_config()


def get_connection():
    # Local import avoids circular issues during app factory setup
    import psycopg2
    return psycopg2.connect(**DB_CONFIG)
