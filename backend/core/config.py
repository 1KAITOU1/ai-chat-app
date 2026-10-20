from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Chat App"
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    DEFAULT_MODEL: str = "qwen3.5:4b"
    CORS_ORIGINS: list[str] = ["http://localhost:5173", "http://localhost"]

settings = Settings()
