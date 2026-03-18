from fastapi import APIRouter

# Create a router object.
# A router groups related endpoints together.
# This is the FastAPI equivalent of a controller group.
router = APIRouter()


@router.get("/health")
def health_check():
    """
    Basic health endpoint.

    Purpose:
    - quickly verify the API is running
    - useful for Docker, monitoring, and debugging
    - often used by load balancers and orchestration systems

    This endpoint should stay simple and reliable.
    It should not depend on OpenAI or other external systems.
    """
    return {
        "status": "ok",
        "message": "Document Q&A AI backend is running."
    }