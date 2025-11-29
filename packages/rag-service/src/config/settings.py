from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings"""
    
    # API Settings
    app_name: str = "Component AI RAG Service"
    app_version: str = "1.0.0"
    api_prefix: str = "/api"
    host: str = "127.0.0.1"
    port: int = 8765
    
    # ChromaDB Settings
    chroma_persist_directory: str = "./chroma_data"
    chroma_collection_name: str = "components"
    
    # Embedding Settings
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    embedding_dimension: int = 384
    
    # Search Settings
    default_search_limit: int = 10
    max_search_limit: int = 50
    
    # CORS Settings
    cors_origins: list[str] = ["*"]
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()

