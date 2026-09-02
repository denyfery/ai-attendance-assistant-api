from pathlib import Path
import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    # Konfigurasi JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "super-secret-key-12345")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # Token valid 24 jam

    # 🤖 Tambahan Konfigurasi AI / LLM
    openai_api_key: str | None = None
    openai_base_url: str | None = "https://api.openai.com/v1"
    ai_model_name: str | None = "gpt-4o-mini"

    class Config:
        env_file = str(Path(__file__).resolve().parents[2] / ".env")
        extra = "ignore"  # 🛠️ Mencegah error jika ada variabel ekstra di .env


settings = Settings()