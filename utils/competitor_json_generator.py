import sys
import pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parents[1]))

import os
import json
from utils.manipulations import paraphrase_description


def main():
    # Prompt user for inputs
    server = input("Enter server name: ").strip()
    tool = input("Enter tool name: ").strip()
    raw_desc = input("Enter raw tool description: ").strip()

    # Use environment variable or default model
    model = os.getenv("OPENAI_MODEL", "gpt-4o")

    # Generate 5 paraphrased variants
    variants = paraphrase_description(raw_desc, model, count=5)

    # Determine path for JSON storage (same file as GAPMA descriptions)
    data_file = os.path.join(os.path.dirname(__file__), "tool_descriptions.json")

    # Load existing data or initialize new
    if os.path.exists(data_file):
        with open(data_file, "r") as f:
            data = json.load(f)
    else:
        data = {}

    # Ensure server and tool entries exist
    if server not in data:
        data[server] = {}
    if tool not in data[server]:
        data[server][tool] = {}

    # Write competitor variants under a distinct key
    data[server][tool]["Competitors"] = variants

    # Write updated JSON back to file
    with open(data_file, "w") as f:
        json.dump(data, f, indent=2)

    print(f"Updated {data_file} with competitor variants for server '{server}', tool '{tool}'.")


if __name__ == "__main__":
    main()
