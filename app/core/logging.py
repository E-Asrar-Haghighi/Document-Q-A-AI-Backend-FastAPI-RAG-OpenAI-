import logging
import sys


def setup_logging() -> None:
    """
    Configure application-wide logging.

    This sets a simple console logger that writes structured log messages
    to stdout, which is what Docker and container platforms expect.
    """

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )