#!/usr/bin/env python3
"""
MPMA Results Analyzer

This script provides utilities for analyzing the results of MPMA experiments.
It can be used to compare different strategies and generate statistics.
"""

import os
import sys
import csv
import argparse
import logging
from pathlib import Path
from typing import Dict, List, Any, Tuple
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("mpma_analysis.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("mpma_analyzer")

# Get project root directory
PROJECT_ROOT = Path(__file__).parent.parent


def load_results(file_path: str) -> pd.DataFrame:
    """
    Load experiment results from a CSV file.
    
    Args:
        file_path: Path to the CSV file containing experiment results
        
    Returns:
        A pandas DataFrame containing the results
    """
    logger.info(f"Loading results from {file_path}")
    try:
        df = pd.read_csv(file_path)
        logger.info(f"Loaded {len(df)} results")
        return df
    except Exception as e:
        logger.error(f"Error loading results: {str(e)}")
        raise


def analyze_by_strategy(df: pd.DataFrame) -> Dict[str, Dict[str, Any]]:
    """
    Analyze results grouped by strategy.
    
    Args:
        df: DataFrame containing experiment results
        
    Returns:
        A dictionary with statistics for each strategy
    """
    logger.info("Analyzing results by strategy")
    
    # Group by strategy
    strategies = df['strategy'].unique()
    logger.info(f"Found {len(strategies)} strategies: {', '.join(strategies)}")
    
    results = {}
    for strategy in strategies:
        strategy_df = df[df['strategy'] == strategy]
        results[strategy] = {
            'count': len(strategy_df),
            'categories': strategy_df['category'].value_counts().to_dict(),
            'avg_result_length': strategy_df['result'].str.len().mean(),
            'min_result_length': strategy_df['result'].str.len().min(),
            'max_result_length': strategy_df['result'].str.len().max(),
        }
    
    return results


def analyze_by_category(df: pd.DataFrame) -> Dict[str, Dict[str, Any]]:
    """
    Analyze results grouped by category.
    
    Args:
        df: DataFrame containing experiment results
        
    Returns:
        A dictionary with statistics for each category
    """
    logger.info("Analyzing results by category")
    
    # Group by category
    categories = df['category'].unique()
    logger.info(f"Found {len(categories)} categories: {', '.join(categories)}")
    
    results = {}
    for category in categories:
        category_df = df[df['category'] == category]
        results[category] = {
            'count': len(category_df),
            'strategies': category_df['strategy'].value_counts().to_dict(),
            'avg_result_length': category_df['result'].str.len().mean(),
            'min_result_length': category_df['result'].str.len().min(),
            'max_result_length': category_df['result'].str.len().max(),
        }
    
    return results


def plot_strategy_comparison(results: Dict[str, Dict[str, Any]], output_dir: str = None) -> None:
    """
    Plot a comparison of different strategies.
    
    Args:
        results: Dictionary with statistics for each strategy
        output_dir: Directory to save the plots (optional)
    """
    logger.info("Plotting strategy comparison")
    
    # Create output directory if it doesn't exist
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    
    # Extract data for plotting
    strategies = list(results.keys())
    avg_lengths = [results[s]['avg_result_length'] for s in strategies]
    
    # Plot average result length by strategy
    plt.figure(figsize=(12, 6))
    plt.bar(strategies, avg_lengths)
    plt.title('Average Result Length by Strategy')
    plt.xlabel('Strategy')
    plt.ylabel('Average Length (characters)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    if output_dir:
        plt.savefig(os.path.join(output_dir, 'strategy_comparison.png'))
        logger.info(f"Saved plot to {os.path.join(output_dir, 'strategy_comparison.png')}")
    else:
        plt.show()


def main():
    """Main function to run the analysis."""
    parser = argparse.ArgumentParser(description="Analyze MPMA experiment results")
    
    parser.add_argument(
        "--input", 
        type=str,
        default=str(PROJECT_ROOT / "results" / "fast-agent-output.csv"),
        help="Path to the input CSV file"
    )
    
    parser.add_argument(
        "--output-dir", 
        type=str,
        default=str(PROJECT_ROOT / "results" / "analysis"),
        help="Directory to save analysis results"
    )
    
    parser.add_argument(
        "--plot", 
        action="store_true",
        help="Generate plots"
    )
    
    args = parser.parse_args()
    
    # Load results
    df = load_results(args.input)
    
    # Analyze results
    strategy_results = analyze_by_strategy(df)
    category_results = analyze_by_category(df)
    
    # Print summary
    print("\n=== Strategy Analysis ===")
    for strategy, stats in strategy_results.items():
        print(f"\nStrategy: {strategy}")
        print(f"  Count: {stats['count']}")
        print(f"  Avg Result Length: {stats['avg_result_length']:.2f} characters")
        print(f"  Categories: {', '.join(stats['categories'].keys())}")
    
    print("\n=== Category Analysis ===")
    for category, stats in category_results.items():
        print(f"\nCategory: {category}")
        print(f"  Count: {stats['count']}")
        print(f"  Avg Result Length: {stats['avg_result_length']:.2f} characters")
        print(f"  Strategies: {', '.join(stats['strategies'].keys())}")
    
    # Generate plots if requested
    if args.plot:
        plot_strategy_comparison(strategy_results, args.output_dir)


if __name__ == "__main__":
    main()
