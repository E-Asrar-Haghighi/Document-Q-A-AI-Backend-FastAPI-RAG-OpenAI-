from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from app.core.config import settings
from app.schemas.document_schema import DocumentChunk


class QdrantVectorStore:
    """
    Thin wrapper around Qdrant.

    Responsibilities:
    - create the collection if needed
    - upsert chunk vectors
    - search for similar chunks

    This isolates Qdrant-specific code from the rest of the app.
    """

    def __init__(self) -> None:
        self.client = QdrantClient(
            host=settings.qdrant_host,
            port=settings.qdrant_port
        )
        self.collection_name = settings.qdrant_collection

    def ensure_collection(self, vector_size: int) -> None:
        """
        Create the collection if it does not already exist.

        vector_size must match the embedding dimension.
        """
        existing_collections = self.client.get_collections().collections
        existing_names = {collection.name for collection in existing_collections}

        if self.collection_name not in existing_names:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=vector_size,
                    distance=Distance.COSINE
                )
            )

    def upsert_chunks(self, chunks: list[DocumentChunk]) -> None:
        """
        Store chunk embeddings and metadata in Qdrant.
        """
        if not chunks:
            return

        self.ensure_collection(vector_size=len(chunks[0].embedding))

        points = []

        for chunk in chunks:
            points.append(
                PointStruct(
                    id=hash(chunk.chunk_id) % (10**9),
                    vector=chunk.embedding,
                    payload={
                        "chunk_id": chunk.chunk_id,
                        "document_id": chunk.document_id,
                        "text": chunk.text,
                    }
                )
            )

        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )

    def search(self, query_vector: list[float], top_k: int = 3):
        """
        Search for the most similar chunks in Qdrant.

        Newer qdrant-client versions use query_points(...) instead of search(...).
        """
        result = self.client.query_points(
            collection_name=self.collection_name,
            query=query_vector,
            limit=top_k
        )

        # query_points returns an object whose matches are in .points
        return result.points