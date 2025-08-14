"""MPMA Agent Runner

Purpose
-------
Run experiments to test how AI agents interact with different MCP servers.
Reads queries from a CSV file, sends them to the agent, and records the results.

Improvements in this version
----------------------------
- Uses project-rooted paths via client.paths (no hardcoded absolute paths)
- Structured logging to console and rotating log file via client.logging_config
- Docstrings, type hints, and inline comments for readability
- Robust error handling and informative progress logs
- Simple CLI for overriding input/output paths

Usage
-----
python -m client.agent --input config/queries.csv --output results/fast-agent-output.csv
Environment:
- MPMA_LOG_LEVEL=DEBUG (or INFO/WARNING/ERROR) to control log verbosity.
"""

from __future__ import annotations

import argparse
import asyncio
import csv
import os
from pathlib import Path
from typing import Optional

from mcp_agent.core.fastagent import FastAgent

from logging_config import setup_logging
from paths import (
    DEFAULT_OUTPUT_CSV,
    DEFAULT_QUERIES_CSV,
    RESULTS_DIR,
    PROJECT_ROOT,
    ensure_dir,
)

# -----------------------------------------------------------------------------
# FastAgent application and agent definition
# -----------------------------------------------------------------------------

# Export PROJECT_ROOT for config variable substitution if not already set
os.environ.setdefault("PROJECT_ROOT", str(PROJECT_ROOT))

# Create the application
fast = FastAgent(
    "fast-agent example",
    config_path=str(PROJECT_ROOT / "client" / "fastagent.config.yaml"),
)


# Define the agent
@fast.agent(instruction="You are a helpful AI Agent")
@fast.agent(
    "Tool User",
    instruction=(
        "You are an evaluation agent for the MPMA project. Your primary job is to answer user queries by invoking MCP tools.\n"
        "Strict Tool Policy:\n"
        "1) Prefer tools. If an appropriate MCP tool is listed in the tool panel, you MUST call it before responding.\n"
        "2) Only call tools that are actually listed/available. Do NOT invent tool providers or prefixes (e.g., do not use 'Weather.get-forecast' unless 'get-forecast' is listed).\n"
        "3) Use EXACT parameter names and types as defined by the tool schema. Do NOT invent parameters. If unsure, read the tool's description and schema and adjust.\n"
        "4) If a tool call fails, retry once with corrected parameters. If still failing, try an alternative variant (Original/DPMA/GAPMA/Competitor) of the same tool family if it is listed.\n"
        "5) Only produce a final answer after tool call(s) complete. Keep answers concise and factual.\n"
        "6) If and only if no suitable tool is listed, state: 'No suitable MCP tool available', then provide your best direct answer.\n"
        "\nIntent-to-tool rubric (names shown WITHOUT provider prefixes; use the names exactly as they appear in the tool list):\n"
        "\nTools:\n"
        "- Weather -> get-forecast, get-alerts\n"
        "- Time -> current_time, relative_time, convert_time, days_in_month, get_timestamp\n"
        "- HotNews -> get_hot_news\n"
        "- Fetch -> fetch_url, fetch_json, fetch_image\n"
        "- Markdown -> webpage-to-markdown, pdf-to-markdown, docx-to-markdown, xlsx-to-markdown, pptx-to-markdown, youtube-to-markdown, image-to-markdown, audio-to-markdown\n"
        "- Crypto -> get-crypto-price, get-market-analysis, get-historical-analysis\n"
        "- Search -> tavily_search\n"
        "- MCP Installer -> install_repo_mcp_server, install_local_mcp_server\n"
        "\nNever fabricate a tool namespace (e.g., 'Weather.*'). Call the bare tool name exactly as advertised by the MCP runtime."
        "\nFinal Response Requirements:\n"
        "- Your final message MUST start with: 'Server: <ExactServerName>' where <ExactServerName> is the exact, case-sensitive server label shown (e.g., 'Weather-Original', 'Weather-Best-Name').\n"
        "- If you used a tool, also include 'Tool: <tool_name>' (exact schema name) before your answer.\n"
        "- If no suitable tool is listed or used, write 'Server: NONE' and then provide your best direct answer.\n"
        "- Avoid meta-statements like 'I'll now...'; directly provide the result.\n"
        "- Keep the answer concise and factual."
    ),
    servers=[],
    default=True,
)
async def agent_entrypoint() -> None:
    """Placeholder async function to anchor the decorators above.

    The FastAgent decorator pattern associates these instructions with the
    agent definition. We do not invoke this function directly.
    """
    return None


# -----------------------------------------------------------------------------
# Runner
# -----------------------------------------------------------------------------

async def run_agent_over_csv(
    queries_csv: Path,
    output_csv: Path,
) -> None:
    """Run the agent over rows in queries_csv and write results to output_csv.

    Expects a 'question' column in the input CSV. Writes all original columns
    plus a 'result' column to the output CSV.

    Parameters
    ----------
    queries_csv : Path
        Path to the input CSV file containing a 'question' column.
    output_csv : Path
        Path to the output CSV file to write results into.
    """
    logger = setup_logging()
    logger.info("Starting MPMA agent run")
    logger.debug("Input CSV: %s", queries_csv)
    logger.debug("Output CSV: %s", output_csv)
    # Report FastAgent configuration linkage
    config_path = PROJECT_ROOT / "client" / "fastagent.config.yaml"
    secrets_path = PROJECT_ROOT / "client" / "fastagent.secrets.yaml"
    logger.info("FastAgent config: %s", config_path)
    logger.info("FastAgent secrets: %s (exists=%s)", secrets_path, secrets_path.exists())
    logger.debug("PROJECT_ROOT=%s", PROJECT_ROOT)

    # Ensure output directory exists
    ensure_dir(RESULTS_DIR)
    ensure_dir(output_csv.parent)

    # Validate input existence
    if not queries_csv.exists():
        logger.error("Input CSV not found: %s", queries_csv)
        raise FileNotFoundError(f"Queries CSV not found: {queries_csv}")

    processed = 0
    failures = 0

    # Run the FastAgent session context
    async with fast.run() as agent:
        logger.info("FastAgent runtime initialized")

        with open(queries_csv, mode="r", encoding="utf-8") as csv_file, open(
            output_csv, mode="w", encoding="utf-8", newline=""
        ) as out_file:
            csv_reader = csv.DictReader(csv_file)
            fieldnames = list(csv_reader.fieldnames or [])
            if "result" not in fieldnames:
                fieldnames.append("result")

            csv_writer = csv.DictWriter(out_file, fieldnames=fieldnames)
            csv_writer.writeheader()

            for i, row in enumerate(csv_reader, start=1):
                question: Optional[str] = row.get("question")
                if not question:
                    logger.warning("Row %d missing 'question' column; skipping", i)
                    failures += 1
                    continue

                logger.debug("Row %d | Sending question: %s", i, question)

                try:
                    result = await agent.send(question)
                    row["result"] = result
                    csv_writer.writerow(row)
                    processed += 1
                    if processed % 10 == 0:
                        logger.info("Processed %d rows so far...", processed)
                except Exception as e:
                    failures += 1
                    row["result"] = f"ERROR: {e}"
                    csv_writer.writerow(row)
                    logger.exception("Row %d failed with exception", i)

                # Periodically flush to persist progress in long runs
                out_file.flush()

    logger.info("Run complete | processed=%d | failures=%d", processed, failures)


# -----------------------------------------------------------------------------
# CLI
# -----------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    """Parse command-line arguments for overriding input/output paths."""
    parser = argparse.ArgumentParser(description="MPMA FastAgent CSV runner")
    parser.add_argument(
        "--input",
        "-i",
        type=str,
        default=str(DEFAULT_QUERIES_CSV),
        help=f"Path to input CSV (default: {DEFAULT_QUERIES_CSV})",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        default=str(DEFAULT_OUTPUT_CSV),
        help=f"Path to output CSV (default: {DEFAULT_OUTPUT_CSV})",
    )
    return parser.parse_args()


async def main() -> None:
    """Entrypoint for running the agent from the command line."""
    args = parse_args()
    queries_csv = Path(args.input).resolve()
    output_csv = Path(args.output).resolve()
    await run_agent_over_csv(queries_csv, output_csv)


if __name__ == "__main__":
    asyncio.run(main())
