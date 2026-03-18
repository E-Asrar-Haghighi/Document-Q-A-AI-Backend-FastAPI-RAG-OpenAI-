import logging
from openai import OpenAI
from app.core.config import settings
from app.core.exceptions import EmbeddingProviderError
from app.core.retry import run_with_retries

logger = logging.getLogger(__name__)


class OpenAIEmbeddingClient:
    """
    Real embedding provider using the OpenAI embeddings API.
    """

    def __init__(self) -> None:
        if not settings.openai_api_key:
            raise ValueError("OPENAI_API_KEY is missing. Check your .env file.")

        self.client = OpenAI(api_key=settings.openai_api_key)
        self.model = settings.openai_embedding_model
        self.timeout_seconds = settings.provider_timeout_seconds

    def embed_text(self, text: str) -> list[float]:
        """
        Generate a real embedding vector for the given text.
        Applies timeout + retry logic for resilience.
        """

        def _call_embedding() -> list[float]:
            response = self.client.embeddings.create(
                model=self.model,
                input=text,
                timeout=self.timeout_seconds,
            )

            return response.data[0].embedding

        try:
            return run_with_retries(
                operation_name="openai_embed_text",
                func=_call_embedding
            )

        except Exception as exc:
            logger.exception("OpenAI embedding generation failed after retries")
            raise EmbeddingProviderError() from exc