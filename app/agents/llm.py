
from app.config import settings


def get_chat_model(temperature=0.2):
    if settings.provider == "groq":
        from langchain_groq import ChatGroq

        if not settings.groq_api_key:
            raise ValueError(
                "GROQ_API_KEY is missing. Add it to your .env file."
            )

        return ChatGroq(
            model=settings.groq_model,
            api_key=settings.groq_api_key,
            temperature=temperature,
            timeout=120,
            max_tokens=5000,
        )

    if settings.provider == "ollama":
        from langchain_ollama import ChatOllama

        return ChatOllama(
            model=settings.ollama_model,
            base_url=settings.ollama_base_url,
            temperature=temperature,
            timeout=600,
            keep_alive="10m",
            num_predict=2500,
        )

    if settings.provider == "openai":
        from langchain_openai import ChatOpenAI

        return ChatOpenAI(
            model=settings.openai_model,
            temperature=temperature,
            timeout=120,
        )

    raise ValueError(
        "LLM_PROVIDER must be 'groq', 'openai', or 'ollama'."
    )
