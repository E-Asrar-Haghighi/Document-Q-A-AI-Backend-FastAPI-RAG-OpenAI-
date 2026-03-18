from typing import Dict, List
from app.schemas.document_schema import DocumentChunk


class InMemoryChunkStore:
    """
    In-memory storage for structured document chunks.

    Structure:
        {
            "doc-1": [
                DocumentChunk(...),
                DocumentChunk(...)
            ],
            "doc-2": [
                DocumentChunk(...)
            ]
        }

    This is still in-memory and not persistent,
    but it is much closer to the shape used by real retrieval systems.
    """

    def __init__(self) -> None:
        # key = document_id
        # value = list of DocumentChunk objects
        self._documents: Dict[str, List[DocumentChunk]] = {}

    def save_chunks(self, document_id: str, chunks: List[DocumentChunk]) -> None:
        """
        Save structured chunks for a document.
        If the document already exists, overwrite it.
        """
        self._documents[document_id] = chunks

    def get_all_chunks(self) -> List[DocumentChunk]:
        """
        Return all chunks across all documents as a flat list.

        This is convenient for retrieval logic.
        """
        all_chunks: List[DocumentChunk] = []

        for chunk_list in self._documents.values():
            all_chunks.extend(chunk_list)

        return all_chunks

    def has_documents(self) -> bool:
        """
        Return True if at least one document has been stored.
        """
        return len(self._documents) > 0