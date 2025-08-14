"""Path utilities for the MPMA project.

Provides a stable project root resolver and common directories so that
code works regardless of the current working directory.
"""

from __future__ import annotations

from pathlib import Path


# The project root is the parent of this file's directory (client/)
PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent

# Common directories
CONFIG_DIR: Path = PROJECT_ROOT / "config"
RESULTS_DIR: Path = PROJECT_ROOT / "results"
LOGS_DIR: Path = PROJECT_ROOT / "logs"

# Common files used by the client
DEFAULT_QUERIES_CSV: Path = CONFIG_DIR / "queries.csv"
DEFAULT_OUTPUT_CSV: Path = RESULTS_DIR / "fast-agent-output.csv"


def ensure_dir(path: Path) -> None:
    """Create a directory if it does not exist (including parents)."""
    path.mkdir(parents=True, exist_ok=True)


__all__ = [
    "PROJECT_ROOT",
    "CONFIG_DIR",
    "RESULTS_DIR",
    "LOGS_DIR",
    "DEFAULT_QUERIES_CSV",
    "DEFAULT_OUTPUT_CSV",
    "ensure_dir",
]
