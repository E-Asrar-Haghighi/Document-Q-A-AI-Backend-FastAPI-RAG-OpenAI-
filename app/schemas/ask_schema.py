from pydantic import BaseModel, Field
from typing import List


class SourceChunk(BaseModel):
    """
    Represents one chunk of document text used to answer the question.

    We now include a retrieval score so:
    - debugging is easier
    - ranking is visible
    - future reranking can use it
    """
    document_id: str
    text: str
    score: float


class AskRequest(BaseModel):
    """
    Request body for asking a question.
    """
    question: str = Field(..., min_length=3, max_length=500)


class AskResponse(BaseModel):
    """
    Final answer response.
    """
    answer: str
    sources: List[SourceChunk]