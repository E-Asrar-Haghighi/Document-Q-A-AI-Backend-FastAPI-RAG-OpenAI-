from pydantic import BaseModel
from typing import List


class DocumentChunk(BaseModel):
    """
    Represents one chunk of an ingested document.

    Now this model also stores an embedding-like representation.

    In a real system, `embedding` would be a dense numeric vector
    created by an embedding model.

    For this learning step, we use a simplified numeric representation
    so we can understand the architecture without adding a real vector DB yet.
    """

    # Unique identifier for the chunk
    chunk_id: str

    # Parent document identifier
    document_id: str

    # Actual chunk text
    text: str

    # Numeric embedding-like representation of the chunk.
    # Later this could be a real embedding from OpenAI or another model.
    embedding: List[float]