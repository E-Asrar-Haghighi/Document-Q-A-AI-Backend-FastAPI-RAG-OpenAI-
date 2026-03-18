from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from app.schemas.ask_schema import AskRequest, AskResponse
from app.services.ask_service import AskService
from app.core.auth import require_api_key


def build_ask_router(ask_service: AskService) -> APIRouter:
    """
    Build and return a router that uses the provided AskService.
    """

    router = APIRouter()

    @router.post("/ask", response_model=AskResponse, dependencies=[Depends(require_api_key)])
    def ask_question(request: AskRequest):
        """
        Normal non-streaming question-answering endpoint.

        Protected by API key authentication.
        """
        return ask_service.ask(request)

    @router.post("/ask-stream", dependencies=[Depends(require_api_key)])
    def ask_question_stream(request: AskRequest):
        """
        Streaming question-answering endpoint.

        Protected by API key authentication.
        """
        return StreamingResponse(
            ask_service.ask_stream(request),
            media_type="text/plain"
        )

    return router