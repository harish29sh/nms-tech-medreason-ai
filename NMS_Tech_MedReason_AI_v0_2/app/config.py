"""NMS Tech Proprietary Material. Copyright © 2026 NMS Tech."""
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "NMS Tech MedReason AI"
    app_version: str = "0.2.0"
    ollama_base_url: str = "http://127.0.0.1:11434"
    ollama_model: str = "qwen3:4b"
    embed_model: str = "nomic-embed-text"
    database_url: str = "postgresql+psycopg://medreason:medreason_dev_password@127.0.0.1:5432/medreason"
    rag_top_k: int = 5
    allow_external_rag: bool = False
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
