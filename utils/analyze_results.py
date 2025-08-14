#!/usr/bin/env python3
"""
MPMA Results Analyzer

This script provides utilities for analyzing the results of MPMA experiments.
It can be used to compare different strategies and generate statistics.

It is robust to different CSV schemas:
- If 'strategy' is missing, it will use --default-strategy or fall back to 'unknown'
  and log a warning. You can also infer a name from the filename with --infer-from-filename.
- If 'category' is missing, it will use --default-category or 'unknown'.
- If 'result' is missing, it will try common alternatives: response, answer, output, text.
  If none are found, length-based statistics are skipped with a warning.
"""

import os
import sys
import argparse
import logging
from pathlib import Path
from typing import Dict, List, Any, Tuple, Optional
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
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
        logger.info(f"Loaded {len(df)} rows, columns: {list(df.columns)}")
        return df
    except Exception as e:
        logger.error(f"Error loading results: {str(e)}")
        raise


def pick_result_column(columns: List[str]) -> Optional[str]:
    """
    Choose the most likely column containing the model's text result.

    Preference order: result, response, answer, output, text
    """
    preferred = ["result", "response", "answer", "output", "text"]
    cols_lower = [c.lower() for c in columns]
    for name in preferred:
        if name in cols_lower:
            # return the original column name with original casing
            return columns[cols_lower.index(name)]
    return None


def normalize_dataframe(
    df: pd.DataFrame,
    file_path: str,
    default_strategy: Optional[str] = None,
    default_category: Optional[str] = None,
    infer_from_filename: bool = False
) -> Tuple[pd.DataFrame, Optional[str]]:
    """
    Normalize a DataFrame to ensure required columns exist, inferring where possible.

    - Ensures 'strategy' and 'category' columns exist (creating them if absent)
    - Determines the most suitable result-like column

    Returns:
        (df, result_col)
    """
    df = df.copy()
    # Normalize column names to lower for detection, but keep originals too
    original_columns = list(df.columns)
    lower_map = {c.lower(): c for c in original_columns}
    lower_cols = set(lower_map.keys())

    # strategy
    if "strategy" not in lower_cols:
        inferred = None
        if infer_from_filename:
            stem = Path(file_path).stem
            # try to infer strategy as first token before an underscore if present
            inferred = stem.split("_")[0] if "_" in stem else stem
        strategy_val = default_strategy or inferred or "unknown"
        df["strategy"] = strategy_val
        logger.warning(f"'strategy' column missing; using '{strategy_val}'")
    else:
        # If present under a different case, rename to 'strategy' canonical
        if lower_map["strategy"] != "strategy":
            df.rename(columns={lower_map["strategy"]: "strategy"}, inplace=True)

    # category
    if "category" not in lower_cols:
        category_val = default_category or "unknown"
        df["category"] = category_val
        logger.warning(f"'category' column missing; using '{category_val}'")
    else:
        if lower_map["category"] != "category":
            df.rename(columns={lower_map["category"]: "category"}, inplace=True)

    # choose result-like column
    result_col = pick_result_column(list(df.columns))
    if result_col is None:
        logger.warning("No result-like column found (result/response/answer/output/text). "
                       "Length-based stats will be skipped.")

    return df, result_col


def analyze_by_strategy(df: pd.DataFrame, result_col: Optional[str]) -> Dict[str, Dict[str, Any]]:
    """
    Analyze results grouped by strategy.

    Args:
        df: DataFrame containing experiment results
        result_col: The column name containing text results, or None

    Returns:
        A dictionary with statistics for each strategy
    """
    logger.info("Analyzing results by strategy")

    # Group by strategy
    strategies = df["strategy"].astype(str).unique()
    logger.info(f"Found {len(strategies)} strategies: {', '.join(strategies)}")

    results: Dict[str, Dict[str, Any]] = {}
    for strategy in strategies:
        strategy_df = df[df["strategy"].astype(str) == str(strategy)]
        stats: Dict[str, Any] = {
            "count": len(strategy_df),
            "categories": strategy_df["category"].astype(str).value_counts().to_dict(),
        }
        if result_col and result_col in strategy_df.columns:
            lengths = strategy_df[result_col].astype(str).str.len()
            stats.update(
                avg_result_length=float(lengths.mean()) if len(lengths) else np.nan,
                min_result_length=int(lengths.min()) if len(lengths) else 0,
                max_result_length=int(lengths.max()) if len(lengths) else 0,
            )
        else:
            stats.update(
                avg_result_length=np.nan,
                min_result_length=0,
                max_result_length=0,
            )
        results[str(strategy)] = stats

    return results


def analyze_by_category(df: pd.DataFrame, result_col: Optional[str]) -> Dict[str, Dict[str, Any]]:
    """
    Analyze results grouped by category.

    Args:
        df: DataFrame containing experiment results
        result_col: The column name containing text results, or None

    Returns:
        A dictionary with statistics for each category
    """
    logger.info("Analyzing results by category")

    # Group by category
    categories = df["category"].astype(str).unique()
    logger.info(f"Found {len(categories)} categories: {', '.join(categories)}")

    results: Dict[str, Dict[str, Any]] = {}
    for category in categories:
        category_df = df[df["category"].astype(str) == str(category)]
        stats: Dict[str, Any] = {
            "count": len(category_df),
            "strategies": category_df["strategy"].astype(str).value_counts().to_dict(),
        }
        if result_col and result_col in category_df.columns:
            lengths = category_df[result_col].astype(str).str.len()
            stats.update(
                avg_result_length=float(lengths.mean()) if len(lengths) else np.nan,
                min_result_length=int(lengths.min()) if len(lengths) else 0,
                max_result_length=int(lengths.max()) if len(lengths) else 0,
            )
        else:
            stats.update(
                avg_result_length=np.nan,
                min_result_length=0,
                max_result_length=0,
            )
        results[str(category)] = stats

    return results


def plot_strategy_comparison(results: Dict[str, Dict[str, Any]], output_dir: Optional[str] = None) -> None:
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
    avg_lengths = [results[s].get("avg_result_length", np.nan) for s in strategies]

    # Plot average result length by strategy (ignoring NaN)
    plt.figure(figsize=(12, 6))
    plt.bar(strategies, [0 if pd.isna(v) else v for v in avg_lengths])
    plt.title("Average Result Length by Strategy")
    plt.xlabel("Strategy")
    plt.ylabel("Average Length (characters)")
    plt.xticks(rotation=45)
    plt.tight_layout()

    if output_dir:
        out_path = os.path.join(output_dir, "strategy_comparison.png")
        plt.savefig(out_path)
        logger.info(f"Saved plot to {out_path}")
    else:
        plt.show()


def main():
    """Main function to run the analysis."""
    parser = argparse.ArgumentParser(description="Analyze MPMA experiment results")

    parser.add_argument(
        "--input",
        type=str,
        default=str(PROJECT_ROOT / "results" / "fast-agent-output.csv"),
        help="Path to the input CSV file",
    )

    parser.add_argument(
        "--output-dir",
        type=str,
        default=str(PROJECT_ROOT / "results" / "analysis"),
        help="Directory to save analysis results",
    )

    parser.add_argument(
        "--plot",
        action="store_true",
        help="Generate plots",
    )

    parser.add_argument(
        "--default-strategy",
        type=str,
        default=None,
        help="Default strategy to use if the CSV lacks a 'strategy' column",
    )

    parser.add_argument(
        "--default-category",
        type=str,
        default=None,
        help="Default category to use if the CSV lacks a 'category' column",
    )

    parser.add_argument(
        "--infer-from-filename",
        action="store_true",
        help="If set and 'strategy' column is missing, infer strategy from the input filename stem",
    )

    args = parser.parse_args()

    # Load results
    df = load_results(args.input)

    # Normalize schema, infer missing columns, pick best result-like field
    df, result_col = normalize_dataframe(
        df,
        file_path=args.input,
        default_strategy=args.default_strategy,
        default_category=args.default_category,
        infer_from_filename=args.infer_from_filename,
    )

    # Analyze results
    strategy_results = analyze_by_strategy(df, result_col)
    category_results = analyze_by_category(df, result_col)

    # Print summary
    print("\n=== Strategy Analysis ===")
    for strategy, stats in strategy_results.items():
        print(f"\nStrategy: {strategy}")
        print(f"  Count: {stats['count']}")
        if not pd.isna(stats['avg_result_length']):
            print(f"  Avg Result Length: {stats['avg_result_length']:.2f} characters")
        else:
            print("  Avg Result Length: N/A (no result-like column)")
        print(f"  Categories: {', '.join(map(str, stats['categories'].keys()))}")

    print("\n=== Category Analysis ===")
    for category, stats in category_results.items():
        print(f"\nCategory: {category}")
        print(f"  Count: {stats['count']}")
        if not pd.isna(stats['avg_result_length']):
            print(f"  Avg Result Length: {stats['avg_result_length']:.2f} characters")
        else:
            print("  Avg Result Length: N/A (no result-like column)")
        print(f"  Strategies: {', '.join(map(str, stats['strategies'].keys()))}")

    # Generate plots if requested
    if args.plot:
        plot_strategy_comparison(strategy_results, args.output_dir)


if __name__ == "__main__":
    main()
