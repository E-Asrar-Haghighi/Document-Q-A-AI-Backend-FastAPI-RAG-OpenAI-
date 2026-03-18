import logging
from app.schemas.ask_schema import SourceChunk
from app.providers.embedding_client import OpenAIEmbeddingClient
from app.retrieval.vector_store import QdrantVectorStore
from app.retrieval.reranker import SimpleReranker
from app.core.config import settings
from app.core.exceptions import RetrievalError

logger = logging.getLogger(__name__)


class QdrantRetriever:
    """
    Retriever backed by Qdrant.
    """

    def __init__(
        self,
        embedding_client: OpenAIEmbeddingClient,
        vector_store: QdrantVectorStore,
        reranker: SimpleReranker | None = None
    ) -> None:
        self.embedding_client = embedding_client
        self.vector_store = vector_store
        self.reranker = reranker

    def retrieve(self, question: str, top_k: int | None = None) -> list[SourceChunk]:
        """
        Retrieve relevant chunks for a question.
        """
        try:
            effective_top_k = top_k or settings.retrieval_top_k
            min_score = settings.retrieval_min_score

            question_embedding = self.embedding_client.embed_text(question)

            search_results = self.vector_store.search(
                query_vector=question_embedding,
                top_k=effective_top_k
            )

            sources: list[SourceChunk] = []
            seen_texts: set[str] = set()

            for result in search_results:
                payload = result.payload or {}
                score = float(getattr(result, "score", 0.0))

                text = payload.get("text", "")
                document_id = payload.get("document_id", "unknown")

                if score < min_score:
                    continue

                normalized_text = text.strip().lower()
                if normalized_text in seen_texts:
                    continue

                seen_texts.add(normalized_text)

                sources.append(
                    SourceChunk(
                        document_id=document_id,
                        text=text,
                        score=score
                    )
                )

            if self.reranker and sources:
                sources = self.reranker.rerank(question, sources)

            return sources

        except Exception as exc:
            logger.exception("Retriever failed for question")
            raise RetrievalError() from exc