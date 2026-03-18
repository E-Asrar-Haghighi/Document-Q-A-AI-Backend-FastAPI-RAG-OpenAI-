from pydantic import BaseModel


class ErrorDetail(BaseModel):
    """
    Inner error object.

    Example:
    {
      "code": "INTERNAL_ERROR",
      "message": "An unexpected error occurred."
    }
    """
    code: str
    message: str


class ErrorResponse(BaseModel):
    """
    Standardized top-level error response.

    Example:
    {
      "error": {
        "code": "INTERNAL_ERROR",
        "message": "An unexpected error occurred."
      }
    }
    """
    error: ErrorDetail