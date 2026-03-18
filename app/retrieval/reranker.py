import re
from app.schemas.ask_schema import SourceChunk


class SimpleReranker:
    """
    Lightweight reranker for retrieved chunks.

    Purpose:
    - improve the ordering of already-retrieved chunks
    - reward chunks that have stronger lexical overlap with the question
    - combine lexical relevance with vector similarity score

    This is NOT a true ML reranker.
    It is a practical intermediate step that improves quality
    and teaches the correct architecture.

    Later, this could be replaced by:
    - a cross-encoder reranker
    - an LLM-based reranker
    - a provider-based reranking API
    """

    def _tokenize(self, text: str) -> set[str]:
        """
        Lowercase and tokenize text into words.
        """
        return set(re.findall(r"\b\w+\b", text.lower()))

    def rerank(self, question: str, sources: list[SourceChunk]) -> list[SourceChunk]:
        """
        Re-rank retrieved chunks using a simple heuristic score.

        Scoring idea:
        - start with the vector similarity score
        - add bonus for lexical overlap with the question
        - add a small bonus if the full normalized question appears in the chunk text

        Returns:
            list of SourceChunk objects sorted best-first
        """

        question_tokens = self._tokenize(question)
        normalized_question = " ".join(re.findall(r"\b\w+\b", question.lower()))

        scored_sources: list[tuple[float, SourceChunk]] = []

        for source in sources:
            chunk_tokens = self._tokenize(source.text)

            # Count overlapping words between question and chunk
            overlap_count = len(question_tokens & chunk_tokens)

            # Bonus if the normalized question string appears inside the chunk text
            chunk_normalized = " ".join(re.findall(r"\b\w+\b", source.text.lower()))
            phrase_bonus = 0.25 if normalized_question and normalized_question in chunk_normalized else 0.0

            # Final rerank score:
            # base vector score + overlap bonus + phrase bonus
            final_score = source.score + (0.10 * overlap_count) + phrase_bonus

            scored_sources.append((final_score, source))

        # Sort descending by final rerank score
        scored_sources.sort(key=lambda item: item[0], reverse=True)

        # Return reordered sources
        return [source for _, source in scored_sources]