import sys
import pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parents[1]))

import os
import json
from utils.manipulations import gapma_generate_description


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
    descriptions = {
        strat: gapma_generate_description(raw_desc, strat, model)
        for strat in strategies
    }

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

    print(f"Updated {data_file} with server '{server}', tool '{tool}'.")


if __name__ == "__main__":
    main()
