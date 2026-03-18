import logging
from collections.abc import Generator
from app.schemas.ask_schema import AskRequest, AskResponse
from app.providers.openai_client import OpenAIClient
from app.cache.redis_cache import RedisCache

logger = logging.getLogger(__name__)


class AskService:
    """
    Service responsible for answering user questions.
    """

    def __init__(
        self,
        retriever,
        openai_client: OpenAIClient,
        cache: RedisCache,
    ) -> None:
        self.retriever = retriever
        self.openai_client = openai_client
        self.cache = cache

    def ask(self, request: AskRequest) -> AskResponse:
        """
        Normal non-streaming answer flow.
        """

        logger.info("Incoming question received")

        cached_response = self.cache.get(request.question)
        if cached_response:
            logger.info("Cache hit for question")
            return cached_response

        logger.info("Cache miss for question")

        matched_sources = self.retriever.retrieve(request.question)
        logger.info("Retriever returned %d filtered source chunk(s)", len(matched_sources))

        if not matched_sources:
            logger.warning("No relevant sources found for question")

            response = AskResponse(
                answer="I could not find relevant information in the ingested documents.",
                sources=[]
            )

            logger.info("Caching negative response")
            self.cache.set(request.question, response)
            return response

        matched_sources.sort(key=lambda source: source.score, reverse=True)

        context = "\n\n".join(
            f"[Document: {source.document_id} | Score: {source.score:.4f}] {source.text}"
            for source in matched_sources
        )

        logger.info("Built context for OpenAI")
        logger.info("Calling OpenAI for grounded answer generation")

        answer = self.openai_client.generate_answer(
            question=request.question,
            context=context
        )

        logger.info("OpenAI returned answer successfully")

        response = AskResponse(
            answer=answer,
            sources=matched_sources
        )

        logger.info("Caching final response")
        self.cache.set(request.question, response)

        logger.info("Returning final response")
        return response

    def ask_stream(self, request: AskRequest) -> Generator[str, None, None]:
        """
        Streaming answer flow.

        Notes:
        - for simplicity, this does not use Redis caching
        - it retrieves relevant chunks and streams the LLM answer
        - later you could capture the full streamed text and cache it
        """

        logger.info("Incoming streaming question received")

        matched_sources = self.retriever.retrieve(request.question)
        logger.info("Retriever returned %d filtered source chunk(s) for streaming", len(matched_sources))

        if not matched_sources:
            logger.warning("No relevant sources found for streaming question")
            yield "I could not find relevant information in the ingested documents."
            return

        matched_sources.sort(key=lambda source: source.score, reverse=True)

        context = "\n\n".join(
            f"[Document: {source.document_id} | Score: {source.score:.4f}] {source.text}"
            for source in matched_sources
        )

        logger.info("Built context for streaming OpenAI call")

        for token in self.openai_client.stream_answer(
            question=request.question,
            context=context
        ):
            yield token