import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """
    Central configuration object for the application.
    """

    def __init__(self) -> None:
        # OpenAI chat model configuration
        self.openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
        self.openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

        # OpenAI embedding model configuration
        self.openai_embedding_model: str = os.getenv(
            "OPENAI_EMBEDDING_MODEL",
            "text-embedding-3-small"
        )

        # Redis configuration
        self.redis_host: str = os.getenv("REDIS_HOST", "localhost")
        self.redis_port: int = int(os.getenv("REDIS_PORT", "6379"))
        self.cache_ttl_seconds: int = int(os.getenv("CACHE_TTL_SECONDS", "3600"))

        # Qdrant configuration
        self.qdrant_host: str = os.getenv("QDRANT_HOST", "localhost")
        self.qdrant_port: int = int(os.getenv("QDRANT_PORT", "6333"))
        self.qdrant_collection: str = os.getenv("QDRANT_COLLECTION", "document_chunks")

        # Retrieval tuning
        self.retrieval_top_k: int = int(os.getenv("RETRIEVAL_TOP_K", "3"))
        self.retrieval_min_score: float = float(os.getenv("RETRIEVAL_MIN_SCORE", "0.20"))

        # Retry / timeout settings
        self.provider_timeout_seconds: float = float(os.getenv("PROVIDER_TIMEOUT_SECONDS", "20"))
        self.provider_max_retries: int = int(os.getenv("PROVIDER_MAX_RETRIES", "2"))
        self.provider_retry_delay_seconds: float = float(os.getenv("PROVIDER_RETRY_DELAY_SECONDS", "1.0"))

        # Simple API key auth
        self.app_api_key: str = os.getenv("APP_API_KEY", "")


settings = Settings()