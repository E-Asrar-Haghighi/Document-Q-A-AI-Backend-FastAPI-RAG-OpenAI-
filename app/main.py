import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.routers.health_router import router as health_router
from app.api.routers.ingest_router import build_ingest_router
from app.api.routers.ask_router import build_ask_router
from app.services.ingest_service import IngestService
from app.services.ask_service import AskService
from app.providers.embedding_client import OpenAIEmbeddingClient
from app.retrieval.vector_retriever import QdrantRetriever
from app.retrieval.vector_store import QdrantVectorStore
from app.retrieval.reranker import SimpleReranker
from app.providers.openai_client import OpenAIClient
from app.cache.redis_cache import RedisCache
from app.core.logging import setup_logging
from app.core.exceptions import AppException
from app.schemas.error_schema import ErrorResponse, ErrorDetail

# Initialize logging before creating app/services
setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Document Q&A AI Backend",
    description="A production-style FastAPI backend for document ingestion and question answering.",
    version="1.0.0"
)

# Shared infrastructure objects
embedding_client = OpenAIEmbeddingClient()
vector_store = QdrantVectorStore()
reranker = SimpleReranker()
openai_client = OpenAIClient()
redis_cache = RedisCache()

# Services
ingest_service = IngestService(
    embedding_client=embedding_client,
    vector_store=vector_store
)

retriever = QdrantRetriever(
    embedding_client=embedding_client,
    vector_store=vector_store,
    reranker=reranker
)

ask_service = AskService(
    retriever=retriever,
    openai_client=openai_client,
    cache=redis_cache
)


@app.exception_handler(AppException)
async def handle_app_exception(request: Request, exc: AppException):
    """
    Handle known application errors with a clean structured response.
    """
    logger.warning("Handled application exception: %s | %s", exc.code, exc.message)

    error_response = ErrorResponse(
        error=ErrorDetail(
            code=exc.code,
            message=exc.message
        )
    )

    return JSONResponse(
        status_code=exc.status_code,
        content=error_response.model_dump()
    )


@app.exception_handler(Exception)
async def handle_unexpected_exception(request: Request, exc: Exception):
    """
    Catch all unexpected errors and return a safe generic response.
    """
    logger.exception("Unhandled exception occurred")

    error_response = ErrorResponse(
        error=ErrorDetail(
            code="INTERNAL_ERROR",
            message="An unexpected error occurred."
        )
    )

    return JSONResponse(
        status_code=500,
        content=error_response.model_dump()
    )


@app.get("/")
def root():
    return {
        "message": "Document Q&A AI Backend is running. Go to /docs for API documentation."
    }


app.include_router(health_router)
app.include_router(build_ingest_router(ingest_service))
app.include_router(build_ask_router(ask_service))