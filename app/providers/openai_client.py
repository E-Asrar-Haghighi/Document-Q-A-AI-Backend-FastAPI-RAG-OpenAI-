import logging
from collections.abc import Generator
from openai import OpenAI
from app.core.config import settings
from app.core.exceptions import UpstreamLLMError
from app.core.retry import run_with_retries

logger = logging.getLogger(__name__)


class OpenAIClient:
    """
    Thin wrapper around the OpenAI SDK.
    """

    def __init__(self) -> None:
        if not settings.openai_api_key:
            raise ValueError("OPENAI_API_KEY is missing. Check your .env file.")

        self.client = OpenAI(api_key=settings.openai_api_key)
        self.model = settings.openai_model
        self.timeout_seconds = settings.provider_timeout_seconds

    def generate_answer(self, question: str, context: str) -> str:
        """
        Non-streaming answer generation.
        """

        def _call_openai() -> str:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a helpful document question-answering assistant. "
                            "Answer only using the provided context. "
                            "If the answer is not in the context, say you cannot find it in the documents."
                        ),
                    },
                    {
                        "role": "user",
                        "content": (
                            f"Context:\n{context}\n\n"
                            f"Question:\n{question}"
                        ),
                    },
                ],
                temperature=0.2,
                timeout=self.timeout_seconds,
            )

            return response.choices[0].message.content or ""

        try:
            return run_with_retries(
                operation_name="openai_generate_answer",
                func=_call_openai
            )

        except Exception as exc:
            logger.exception("OpenAI answer generation failed after retries")
            raise UpstreamLLMError() from exc

    def stream_answer(self, question: str, context: str) -> Generator[str, None, None]:
        """
        Streaming answer generation.

        Yields text chunks as they arrive from OpenAI.
        """

        try:
            stream = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a helpful document question-answering assistant. "
                            "Answer only using the provided context. "
                            "If the answer is not in the context, say you cannot find it in the documents."
                        ),
                    },
                    {
                        "role": "user",
                        "content": (
                            f"Context:\n{context}\n\n"
                            f"Question:\n{question}"
                        ),
                    },
                ],
                temperature=0.2,
                timeout=self.timeout_seconds,
                stream=True,
            )

            for chunk in stream:
                delta = chunk.choices[0].delta.content
                if delta:
                    yield delta

        except Exception as exc:
            logger.exception("OpenAI streaming failed")
            raise UpstreamLLMError("Failed to stream answer from language model.") from exc