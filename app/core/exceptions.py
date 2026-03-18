class AppException(Exception):
    """
    Base application exception.

    Use this for errors we expect and want to return cleanly.
    """

    def __init__(self, code: str, message: str, status_code: int = 400) -> None:
        self.code = code
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class UpstreamLLMError(AppException):
    """
    Error raised when the LLM provider fails.
    """

    def __init__(self, message: str = "Failed to generate answer from language model.") -> None:
        super().__init__(
            code="UPSTREAM_LLM_ERROR",
            message=message,
            status_code=502
        )


class EmbeddingProviderError(AppException):
    """
    Error raised when the embedding provider fails.
    """

    def __init__(self, message: str = "Failed to generate embeddings.") -> None:
        super().__init__(
            code="EMBEDDING_PROVIDER_ERROR",
            message=message,
            status_code=502
        )


class RetrievalError(AppException):
    """
    Error raised when retrieval fails.
    """

    def __init__(self, message: str = "Failed to retrieve relevant document chunks.") -> None:
        super().__init__(
            code="RETRIEVAL_ERROR",
            message=message,
            status_code=500
        )