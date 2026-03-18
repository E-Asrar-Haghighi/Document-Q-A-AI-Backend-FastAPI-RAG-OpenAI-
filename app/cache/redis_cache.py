import hashlib
import json
import redis
from app.core.config import settings
from app.schemas.ask_schema import AskResponse


class RedisCache:
    """
    Thin wrapper around Redis for caching question-answer results.

    Responsibilities:
    - create a stable cache key from the user question
    - read cached AskResponse data
    - write AskResponse data with expiration

    Important:
    We cache the final API response shape, not just the raw answer text.
    That means both:
    - answer
    - sources
    can be reused.
    """

    def __init__(self) -> None:
        self.client = redis.Redis(
            host=settings.redis_host,
            port=settings.redis_port,
            decode_responses=True
        )
        self.ttl_seconds = settings.cache_ttl_seconds

    def _make_key(self, question: str) -> str:
        """
        Create a stable Redis key for a question.

        We hash the question so:
        - keys stay short
        - special characters are not a problem
        - key format is consistent
        """
        question_hash = hashlib.md5(question.strip().lower().encode("utf-8")).hexdigest()
        return f"ask_cache:{question_hash}"

    def get(self, question: str) -> AskResponse | None:
        """
        Return cached AskResponse if present, otherwise None.
        """
        key = self._make_key(question)
        cached_json = self.client.get(key)

        if not cached_json:
            return None

        cached_data = json.loads(cached_json)

        # Reconstruct the AskResponse object from cached JSON.
        return AskResponse(**cached_data)

    def set(self, question: str, response: AskResponse) -> None:
        """
        Store an AskResponse in Redis with expiration.
        """
        key = self._make_key(question)

        # Convert the Pydantic response model into a JSON string.
        payload = response.model_dump()

        self.client.set(
            key,
            json.dumps(payload),
            ex=self.ttl_seconds
        )