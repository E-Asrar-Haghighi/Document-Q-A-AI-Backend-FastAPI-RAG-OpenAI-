import re
from app.schemas.ask_schema import SourceChunk
from app.services.document_store import InMemoryChunkStore


class SimpleKeywordRetriever:
    """
    Very simple retriever that works over structured document chunks.

    This is retrieval-ready architecture because later this class can be replaced
    by a vector retriever without changing the ask service.
    """

    def __init__(self, document_store: InMemoryChunkStore) -> None:
        self.document_store = document_store

    def _tokenize(self, text: str) -> set[str]:
        """
        Lowercase and tokenize text into words, removing punctuation.
        """
        return set(re.findall(r"\b\w+\b", text.lower()))

    def retrieve(self, question: str) -> list[SourceChunk]:
        """
        Retrieve relevant source chunks using simple keyword overlap.
        """

        if not self.document_store.has_documents():
            return []

        question_words = self._tokenize(question)
        matched_sources: list[SourceChunk] = []

        # Iterate over structured chunk records.
        for chunk in self.document_store.get_all_chunks():
            chunk_words = self._tokenize(chunk.text)

            if question_words & chunk_words:
                matched_sources.append(
                    SourceChunk(
                        document_id=chunk.document_id,
                        text=chunk.text
                    )
                )

        return matched_sources