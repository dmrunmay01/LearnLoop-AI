
from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()


class Settings(BaseModel):
    provider: str = os.getenv("LLM_PROVIDER", "groq").lower()

    # Groq
    groq_api_key: str = os.getenv("GROQ_API_KEY", "")
    groq_model: str = os.getenv(
        "GROQ_MODEL", "openai/gpt-oss-20b"
    )

    # OpenAI
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    # Ollama
    ollama_model: str = os.getenv("OLLAMA_MODEL", "phi3:latest")
    ollama_base_url: str = os.getenv(
        "OLLAMA_BASE_URL", "http://localhost:11434"
    )

    # Application
    database_path: str = os.getenv("DATABASE_PATH", "data/learnloop.db")
    max_retries: int = min(
        max(int(os.getenv("MAX_RETRIES", "2")), 0), 2
    )


settings = Settings()
