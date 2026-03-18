from pydantic import BaseModel, Field


class IngestRequest(BaseModel):
    """
    Request body for document ingestion.
    """

    document_id: str = Field(..., min_length=1, max_length=100)
    text: str = Field(..., min_length=10)


class IngestResponse(BaseModel):
    """
    Response returned after synchronous ingestion.
    """

    message: str
    document_id: str
    chunks_indexed: int


class BackgroundIngestResponse(BaseModel):
    """
    Response returned when ingestion is accepted for background processing.

    Important:
    This response means:
    - the request was accepted
    - the ingestion job was started in the background

    It does NOT guarantee ingestion already finished.
    """

    message: str
    document_id: str
    status: str