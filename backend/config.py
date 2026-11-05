import os
from pathlib import Path
from pydantic import BaseModel

BASE_DIR = Path(__file__).resolve().parent.parent

class AppConfig(BaseModel):
    app_name: str = "AI-Based Personalized Career Content Generator"
    version: str = "1.0.0"
    api_prefix: str = "/api/v1"
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    default_model: str = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    host: str = os.getenv("HOST", "127.0.0.1")
    port: int = int(os.getenv("PORT", 8000))
    debug: bool = os.getenv("DEBUG", "false").lower() in ("true", "1", "t")

config = AppConfig()

