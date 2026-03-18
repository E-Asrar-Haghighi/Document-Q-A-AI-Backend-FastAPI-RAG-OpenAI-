from app.schemas.ingest_schema import IngestRequest, IngestResponse
from app.schemas.document_schema import DocumentChunk
from app.providers.embedding_client import OpenAIEmbeddingClient
from app.retrieval.vector_store import QdrantVectorStore


class IngestService:
    """
    Service responsible for document ingestion logic.

    Updated flow:
    1. split text into chunks
    2. create real embeddings
    3. store chunk vectors in Qdrant
    """

    def __init__(
        self,
        embedding_client: OpenAIEmbeddingClient,
        vector_store: QdrantVectorStore
    ) -> None:
        self.embedding_client = embedding_client
        self.vector_store = vector_store

    def ingest(self, request: IngestRequest) -> IngestResponse:
        raw_chunks = request.text.split(".")
        cleaned_chunks = [chunk.strip() for chunk in raw_chunks if chunk.strip()]

        chunk_objects: list[DocumentChunk] = []

        for index, chunk_text in enumerate(cleaned_chunks, start=1):
            chunk_embedding = self.embedding_client.embed_text(chunk_text)

            chunk_objects.append(
                DocumentChunk(
                    chunk_id=f"{request.document_id}-chunk-{index}",
                    document_id=request.document_id,
                    text=chunk_text,
                    embedding=chunk_embedding
                )
            )

        self.vector_store.upsert_chunks(chunk_objects)

        return IngestResponse(
            message="Document ingested successfully.",
            document_id=request.document_id,
            chunks_indexed=len(chunk_objects)
        )