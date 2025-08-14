"""Logging configuration for the MPMA client.

Provides a single setup function to configure structured console and rotating
file logging rooted at the project logs directory.
"""

from __future__ import annotations

import logging
import os
from logging import Logger
from logging.handlers import RotatingFileHandler

from paths import LOGS_DIR, ensure_dir


def setup_logging(name: str = "mpma.client", level: str | None = None) -> Logger:
    """Configure and return a namespaced logger.

    - Level can be controlled via the MPMA_LOG_LEVEL environment variable
      (e.g., DEBUG, INFO, WARNING, ERROR) or passed explicitly.
    - Logs are emitted to both console (stdout) and a rotating file under logs/.

    Parameters
    ----------
    name : str
        Logger name to create/use (default: "mpma.client").
    level : str | None
        Optional explicit level override. If None, uses MPMA_LOG_LEVEL env var
        or defaults to INFO.

    Returns
    -------
    logging.Logger
        The configured logger instance.
    """
    level_str = (level or os.getenv("MPMA_LOG_LEVEL", "INFO")).upper()
    level_val = getattr(logging, level_str, logging.INFO)

    logger = logging.getLogger(name)
    logger.setLevel(level_val)

    # Avoid adding duplicate handlers if setup_logging is called multiple times
    if logger.handlers:
        return logger

    # Common formatter: timestamp | LEVEL | logger | message
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console handler
    sh = logging.StreamHandler()
    sh.setLevel(level_val)
    sh.setFormatter(formatter)
    logger.addHandler(sh)

    # File handler (rotating)
    try:
        ensure_dir(LOGS_DIR)
        fh = RotatingFileHandler(
            LOGS_DIR / "client.log",
            maxBytes=1_000_000,  # ~1MB
            backupCount=3,
            encoding="utf-8",
        )
        fh.setLevel(level_val)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    except Exception as e:  # If file logging fails, keep console logging only
        logger.warning("File logging not available: %s", e)

    logger.debug("Logger '%s' initialized at level %s", name, level_str)
    return logger


__all__ = ["setup_logging"]
