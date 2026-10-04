import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings:
    app_name = os.getenv("APP_NAME", "LegalEase")

    gemini_api_key = os.getenv("GEMINI_API_KEY", "")

    gemini_model = os.getenv(
        "GEMINI_MODEL",
        "gemini-3.8-flash"
    )

    demo_mode = os.getenv(
        "DEMO_MODE",
        "false"
    ).lower() in {"1", "true", "yes"}

    backend_url = os.getenv(
        "BACKEND_URL",
        "http://127.0.0.1:8000"
    )

    logo_path = BASE_DIR / "assets" / "logo.png"


settings = Settings()