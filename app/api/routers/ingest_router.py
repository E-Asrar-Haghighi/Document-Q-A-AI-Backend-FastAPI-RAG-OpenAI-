import logging
from fastapi import APIRouter, Depends, BackgroundTasks
from app.schemas.ingest_schema import (
    IngestRequest,
    IngestResponse,
    BackgroundIngestResponse,
)
from app.services.ingest_service import IngestService
from app.core.auth import require_api_key

logger = logging.getLogger(__name__)


def build_ingest_router(ingest_service: IngestService) -> APIRouter:
    """
    Build and return an ingest router using the provided IngestService.

    This router supports:
    - synchronous ingestion
    - background ingestion
    """

    router = APIRouter()

    @router.post("/ingest", response_model=IngestResponse, dependencies=[Depends(require_api_key)])
    def ingest_document(request: IngestRequest):
        """
        Synchronous ingestion endpoint.

        The request waits until ingestion is fully complete.
        Useful for:
        - small documents
        - debugging
        - simple workflows
        """
        return ingest_service.ingest(request)

    def run_background_ingestion(request: IngestRequest) -> None:
        """
        Background ingestion job.

        This function runs after the HTTP response has already been returned.

        Important:
        Since this runs in the background, any errors should be logged.
        The client will not automatically see them in the original response.
        """
        try:
            logger.info(
                "Background ingestion started | document_id=%s",
                request.document_id
            )

            result = ingest_service.ingest(request)

            logger.info(
                "Background ingestion completed | document_id=%s | chunks_indexed=%d",
                result.document_id,
                result.chunks_indexed
            )

        except Exception:
            logger.exception(
                "Background ingestion failed | document_id=%s",
                request.document_id
            )

    @router.post(
        "/ingest-background",
        response_model=BackgroundIngestResponse,
        dependencies=[Depends(require_api_key)]
    )
    def ingest_document_background(
        request: IngestRequest,
        background_tasks: BackgroundTasks
    ):
        """
        Background ingestion endpoint.

        The API returns immediately and ingestion continues in the background.

        Useful for:
        - larger documents
        - better UX
        - avoiding long request wait times
        """
        background_tasks.add_task(run_background_ingestion, request)

        return BackgroundIngestResponse(
            message="Document ingestion started in background.",
            document_id=request.document_id,
            status="accepted"
        )

    return router