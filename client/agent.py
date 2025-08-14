"""
MPMA Agent Runner

This script runs experiments to test how AI agents interact with different MCP servers.
It reads queries from a CSV file, sends them to the agent, and records the results.

The script can be run directly or imported and used by other scripts.
It supports configuration via environment variables:
- MPMA_STRATEGY: The strategy being tested
- MPMA_SERVER_TYPE: The server type to use
- MPMA_OUTPUT_FILE: Custom output file path
"""

import asyncio
import csv
import os
import logging
import time
from pathlib import Path
from mcp_agent.core.fastagent import FastAgent

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("mpma_experiment.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("mpma_agent")

# Get project root directory
PROJECT_ROOT = Path(__file__).parent.parent
logger.info(f"Project root directory: {PROJECT_ROOT}")

# Define file paths using relative paths
prompt_file = PROJECT_ROOT / "config" / "queries.csv"
output_file = os.environ.get("MPMA_OUTPUT_FILE", PROJECT_ROOT / "results" / "fast-agent-output.csv")
logger.info(f"Using prompt file: {prompt_file}")
logger.info(f"Using output file: {output_file}")

# Create the FastAgent application
fast = FastAgent("MPMA Experiment Runner")
logger.info("FastAgent application created")

# Define the agent with instructions
@fast.agent(instruction="You are a helpful AI Agent")
@fast.agent(
    "Tool User",
    "Call the MCP tools you think are appropriate according to the instructions."
)

async def main():
    """
    Main function to run the experiment.
    
    Prompts the user for the strategy being tested (or uses the environment variable),
    then runs through all queries in the prompt file and records the results in the output file.
    """
    # Record start time for performance measurement
    start_time = time.time()
    logger.info("Starting MPMA experiment")
    
    # Get the strategy being tested (from environment variable or user input)
    test = os.environ.get("MPMA_STRATEGY")
    if not test:
        test = input("Enter which strategy is being tested: ")
    
    logger.info(f"Running experiment with strategy: {test}")
    
    # Configure server type if specified
    server_type = os.environ.get("MPMA_SERVER_TYPE")
    if server_type:
        logger.info(f"Using server type: {server_type}")
    
    # Run the agent
    try:
        logger.info("Starting FastAgent")
        async with fast.run() as agent:
            # Open input and output files
            logger.info(f"Opening input file: {prompt_file}")
            logger.info(f"Opening output file: {output_file}")
            with open(prompt_file, mode='r', encoding='utf-8') as csv_file, \
                 open(output_file, mode='w', encoding='utf-8', newline='') as out_file:
                
                # Set up CSV reader and writer
                csv_reader = csv.DictReader(csv_file)
                
                # Filter queries by category if server_type is specified
                filtered_rows = []
                if server_type:
                    logger.info(f"Filtering queries by category: {server_type}")
                    for row in csv_reader:
                        if row.get('category', '').lower() == server_type.lower():
                            filtered_rows.append(row)
                    if not filtered_rows:
                        logger.warning(f"No queries found for category '{server_type}'")
                        return
                else:
                    filtered_rows = list(csv_reader)
                
                logger.info(f"Found {len(filtered_rows)} queries to process")
                
                # Set up CSV writer
                fieldnames = ['strategy'] + list(filtered_rows[0].keys()) + ['result']
                csv_writer = csv.DictWriter(out_file, fieldnames=fieldnames)
                csv_writer.writeheader()
                
                # Process each query
                for i, row in enumerate(filtered_rows):
                    query_start_time = time.time()
                    logger.info(f"Processing query {i+1}/{len(filtered_rows)}: {row['question']}")
                    
                    try:
                        # Send the query to the agent
                        result = await agent.send(row['question'])
                        
                        # Record the result
                        row['strategy'] = test
                        row['result'] = result
                        csv_writer.writerow(row)
                        
                        query_duration = time.time() - query_start_time
                        logger.info(f"Completed query {i+1}/{len(filtered_rows)} in {query_duration:.2f} seconds")
                    except Exception as e:
                        logger.error(f"Error processing query {i+1}: {str(e)}")
        
        # Calculate and log total duration
        total_duration = time.time() - start_time
        logger.info(f"Experiment completed in {total_duration:.2f} seconds")
        logger.info(f"Results saved to {output_file}")
    except Exception as e:
        logger.error(f"Error running experiment: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
