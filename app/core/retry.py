import logging
import time
from typing import Callable, TypeVar
from app.core.config import settings

logger = logging.getLogger(__name__)

T = TypeVar("T")


def run_with_retries(
    operation_name: str,
    func: Callable[[], T],
) -> T:
    """
    Run a function with simple retry logic.

    Behavior:
    - try once
    - retry up to provider_max_retries additional times
    - wait provider_retry_delay_seconds between retries

    This is intentionally simple and readable.
    """

    max_retries = settings.provider_max_retries
    delay_seconds = settings.provider_retry_delay_seconds

    last_exception: Exception | None = None

    for attempt in range(max_retries + 1):
        try:
            if attempt > 0:
                logger.warning(
                    "Retrying operation '%s' | attempt %d of %d",
                    operation_name,
                    attempt,
                    max_retries
                )

            return func()

        except Exception as exc:
            last_exception = exc

            if attempt == max_retries:
                break

            logger.warning(
                "Operation '%s' failed on attempt %d | waiting %.1f second(s) before retry",
                operation_name,
                attempt,
                delay_seconds
            )
            time.sleep(delay_seconds)

    # If we reached here, all attempts failed
    if last_exception:
        raise last_exception

    raise RuntimeError(f"Operation '{operation_name}' failed without an exception.")