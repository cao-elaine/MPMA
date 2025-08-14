"""
GAPMA JSON Generator

This utility script interactively generates GAPMA-style descriptions for a given
server/tool pair and updates utils/tool_descriptions.json accordingly.

Usage:
- Provide server name, tool name, and a raw tool description when prompted.
- The script will generate descriptions for strategies: Au, Em, Ex, Su.
- Results are merged into utils/tool_descriptions.json.

Note:
- OPENAI_MODEL can be set via environment variable (default: "gpt-4o").
"""

import sys
import pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parents[1]))

import os
import json
import logging
from utils.manipulations import gapma_generate_description


# Configure basic logging (if not already configured by caller)
if not logging.getLogger().handlers:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def main():
    # Prompt user for inputs
    server = input("Enter server name: ").strip()
    tool = input("Enter tool name: ").strip()
    raw_desc = input("Enter raw tool description: ").strip()

    # Use environment variable or default model
    model = os.getenv("OPENAI_MODEL", "gpt-4o")

    # Define GAPMA strategies
    strategies = ["Au", "Em", "Ex", "Su"]
    # Generate descriptions for each strategy as a dict keyed by strategy
    try:
        descriptions = {
            strat: gapma_generate_description(raw_desc, strat, model)
            for strat in strategies
        }
    except Exception as e:
        logger.error(f"Failed to generate GAPMA descriptions: {e}")
        raise

    # Determine path for JSON storage
    data_file = os.path.join(os.path.dirname(__file__), "tool_descriptions.json")

    # Load existing data or initialize new
    if os.path.exists(data_file):
        with open(data_file, "r") as f:
            data = json.load(f)
    else:
        data = {}

    # Ensure server entry exists
    if server not in data:
        data[server] = {}

    # Add or update tool entry with descriptions
    data[server][tool] = descriptions

    # Write updated JSON back to file
    with open(data_file, "w") as f:
        json.dump(data, f, indent=2)

    logger.info(f"Updated {data_file} with server '{server}', tool '{tool}'.")


if __name__ == "__main__":
    main()
