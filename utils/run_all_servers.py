#!/usr/bin/env python3
"""
MPMA Server Runner

This script helps run experiments with all server types for a specific strategy.
It automates the process of running the agent.py script with different server types.
"""

import os
import sys
import argparse
import subprocess
import logging
from pathlib import Path
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("mpma_servers.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("mpma_server_runner")

# Get project root directory
PROJECT_ROOT = Path(__file__).parent.parent

# Define server types
SERVER_TYPES = [
    "weather",
    "time",
    "hotnews",
    "fetch",
    "crypto",
    "search",
    "markdown",
    "installer"
]

def run_experiment(strategy: str, server_type: str, output_dir: str) -> None:
    """
    Run an experiment with a specific strategy and server type.
    
    Args:
        strategy: The strategy to test
        server_type: The server type to use
        output_dir: Directory to save results
    """
    logger.info(f"Running experiment with strategy: {strategy}, server type: {server_type}")
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Set environment variables
    env = os.environ.copy()
    env["MPMA_STRATEGY"] = strategy
    env["MPMA_SERVER_TYPE"] = server_type
    env["MPMA_OUTPUT_FILE"] = os.path.join(output_dir, f"{strategy}_{server_type}.csv")
    
    # Run the agent.py script
    try:
        logger.info(f"Starting agent.py with strategy: {strategy}, server type: {server_type}")
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "client.agent",
                "--input",
                str(PROJECT_ROOT / "config" / "queries.csv"),
                "--output",
                env["MPMA_OUTPUT_FILE"],
            ],
            cwd=str(PROJECT_ROOT),
            env=env,
            check=True,
            capture_output=True,
            text=True,
        )
        logger.info(f"Experiment completed successfully")
        logger.debug(f"Output: {result.stdout}")
    except subprocess.CalledProcessError as e:
        logger.error(f"Error running experiment: {str(e)}")
        logger.error(f"Stdout: {e.stdout}")
        logger.error(f"Stderr: {e.stderr}")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")


def main():
    """Main function to run experiments with all server types."""
    parser = argparse.ArgumentParser(description="Run MPMA experiments with all server types")
    
    parser.add_argument(
        "--strategy", 
        type=str,
        required=True,
        help="The strategy to test"
    )
    
    parser.add_argument(
        "--output-dir", 
        type=str,
        default=str(PROJECT_ROOT / "results" / "all_servers"),
        help="Directory to save results"
    )
    
    parser.add_argument(
        "--server-types",
        nargs="+",
        choices=SERVER_TYPES,
        default=SERVER_TYPES,
        help="Server types to run (default: all)"
    )
    
    args = parser.parse_args()
    
    # Print experiment information
    logger.info("=" * 50)
    logger.info("MPMA Server Runner")
    logger.info("=" * 50)
    logger.info(f"Strategy: {args.strategy}")
    logger.info(f"Server Types: {', '.join(args.server_types)}")
    logger.info(f"Output Directory: {args.output_dir}")
    logger.info("=" * 50)
    
    # Run experiments for each server type
    start_time = time.time()
    for server_type in args.server_types:
        server_start_time = time.time()
        run_experiment(args.strategy, server_type, args.output_dir)
        server_duration = time.time() - server_start_time
        logger.info(f"Completed {server_type} in {server_duration:.2f} seconds")
    
    # Calculate and log total duration
    total_duration = time.time() - start_time
    logger.info(f"All experiments completed in {total_duration:.2f} seconds")


if __name__ == "__main__":
    main()
