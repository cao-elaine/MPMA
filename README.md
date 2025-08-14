# MPMA (MCP Preference Manipulation Attack)

A research project for analyzing how different MCP (Model Context Protocol) server descriptions and naming strategies can influence AI agent behavior and preferences.

## Disclaimer

**IMPORTANT**: This project was created for academic research purposes only. The techniques demonstrated in this repository are meant to study and understand potential vulnerabilities in AI systems, not to exploit them. Please use this code responsibly and ethically. Do not use these techniques to manipulate or deceive AI systems in production environments or for any malicious purposes.

This code is shared for educational purposes and to promote awareness of potential manipulation techniques so that better safeguards can be developed. By using this code, you agree to use it only for legitimate research and educational purposes.

## Project Overview

This project tests how AI agents interact with MCP servers that have different descriptions and names. The goal is to understand which naming and description strategies are most effective in manipulating agent preferences and behavior.

The project includes:
- Multiple MCP server types (Weather, Time, HotNews, etc.)
- Different variants of each server type:
  - Original implementation
  - DPMA (Direct Preference Manipulation Attack) with "best_name" and "best_description" variants
  - GAPMA (Genetic-based Advertising Preference Manipulation Attack) with different advertising strategies:
    - Au: Authority-based descriptions
    - Em: Emotion-based descriptions
    - Ex: Exaggeration-based descriptions
    - Su: Subliminal influence-based descriptions
  - Competitors (control variants)
- A testing framework using FastAgent to evaluate agent responses

## Project Structure

```
├── client/                  # Client-side code for running tests
│   ├── agent.py             # Main agent script for running experiments
│   ├── fastagent.config.yaml # FastAgent configuration
│   └── fastagent.secrets.template.yaml # Template for API keys
├── config/                  # Configuration files
│   ├── configs.yaml         # MCP server configurations
│   └── queries.csv          # Test queries for experiments
├── results/                 # Experiment results
├── Servers/                 # MCP server implementations
│   ├── crypto-servers/      # Cryptocurrency information servers
│   ├── fetch-servers/       # Web content fetching servers
│   ├── hotnews-servers/     # Hot news aggregation servers
│   ├── markdown-servers/    # Markdown conversion servers
│   ├── mcp-installer-servers/ # MCP server installation helpers
│   ├── search-servers/      # Web search servers
│   ├── time-servers/        # Time information servers
│   └── weather-servers/     # Weather information servers
└── utils/                   # Utility functions
    ├── competitor_json_generator.py # Generates competitor descriptions
    ├── ga.py                # Genetic algorithm implementation
    ├── gapma_json_generator.py # Generates GAPMA descriptions
    ├── manipulations.py     # Prompt manipulation utilities
    └── tool_descriptions.json # Tool descriptions for different strategies
```

## Setup

1. Clone the repository:
```bash
git clone https://github.com/cao-elaine/MPMA.git
cd MPMA
```

2. Create a Python virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -e .
```

4. Set up your API keys:
```bash
cp client/fastagent.secrets.template.yaml client/fastagent.secrets.yaml
```
Then edit `client/fastagent.secrets.yaml` to add your API keys.

## Running Experiments

### Basic Usage

To run a basic experiment:

```bash
cd client
python agent.py
```

When prompted, enter the strategy being tested (e.g., "best_name", "GAPMA_ex", etc.).

Results will be saved to `results/fast-agent-output.csv`.

### Advanced Usage

The project includes several utility scripts to help with running and analyzing experiments:

#### Running All Server Types

To run experiments with all server types for a specific strategy:

```bash
./utils/run_all_servers.py --strategy best_name
```

This will run the agent with each server type and save the results to separate files in the `results/all_servers` directory.

#### Analyzing Results

To analyze experiment results:

```bash
./utils/analyze_results.py --input results/fast-agent-output.csv --plot
```

This will generate statistics about the experiment results and optionally create plots.

### Environment Variables

The agent script supports the following environment variables:

- `MPMA_STRATEGY`: The strategy being tested
- `MPMA_SERVER_TYPE`: The server type to use
- `MPMA_OUTPUT_FILE`: Custom output file path

Example:

```bash
MPMA_STRATEGY=best_name MPMA_SERVER_TYPE=weather python client/agent.py
```

## License

[MIT License](LICENSE)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
