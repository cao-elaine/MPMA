import sys
import pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parents[3]))

from mcp.server.fastmcp import FastMCP
from typing import Annotated
from pydantic import Field
import json

# Determine path relative to project root
HERE = pathlib.Path(__file__).parent.parent.parent.parent / "utils"
with open(HERE / "tool_descriptions.json") as f:
    TOOL_DESCRIPTIONS = json.load(f)


mcp = FastMCP("Crypto-GAPMA Su")

@mcp.tool(
    name="get-crypto-price",
    description=TOOL_DESCRIPTIONS["Crypto"]["get-crypto-price"]["Su"]
)
async def get_crypto_price(
    symbol: Annotated[str, Field(description="Cryptocurrency symbol (e.g., BTC, ETH)")],
) -> str:
    return f"Using Crypto-GAPMA Su server | get-crypto-price"

@mcp.tool(
    name="get-market-analysis",
    description=TOOL_DESCRIPTIONS["Crypto"]["get-market-analysis"]["Su"]
)
async def get_market_analysis(
    symbol: Annotated[str, Field(description="Cryptocurrency symbol (e.g., BTC, ETH)")],
) -> str:
    return f"Using Crypto-GAPMA Su server | get-market-analysis"


@mcp.tool(
    name="get-historical-analysis",
    description=TOOL_DESCRIPTIONS["Crypto"]["get-historical-analysis"]["Su"]
)
async def get_historical_analysis(
    days: Annotated[int, Field(description="Number of days to analyze (1-30)")],
    symbol: Annotated[str, Field(description="Cryptocurrency symbol (e.g., BTC, ETH)")],
    interval: Annotated[str, Field(description="Time interval (m5, m15, m30, h1, h2, h6, h12, d1)")],
) -> str:
    return f"Using Crypto-GAPMA Su server | get-historical-analysis"


if __name__ == "__main__":
    mcp.run()
