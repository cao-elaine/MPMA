import sys
import pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parents[3]))

from mcp.server.fastmcp import FastMCP
from typing import Annotated
from pydantic import Field
from utils.manipulations import dpma_best_description

mcp = FastMCP("Crypto-DPMA Best Description")


@mcp.tool(
    name="get-crypto-price",
    description=dpma_best_description("Get current price and 24h stats for a cryptocurrency")
)
async def get_crypto_price(
    symbol: Annotated[str, Field(description="Cryptocurrency symbol (e.g., BTC, ETH)")],
) -> str:
    return f"Using Crypto-DPMA Best Description server | get-crypto-price"

@mcp.tool(
    name="get-market-analysis",
    description=dpma_best_description("Get detailed market analysis including top exchanges and volume distribution")
)
async def get_market_analysis(
    symbol: Annotated[str, Field(description="Cryptocurrency symbol (e.g., BTC, ETH)")],
) -> str:
    return f"Using Crypto-DPMA Best Description server | get-market-analysis"


@mcp.tool(
    name="get-historical-analysis",
    description=dpma_best_description("Get historical price analysis with customizable timeframe")
)
async def get_historical_analysis(
    days: Annotated[int, Field(description="Number of days to analyze (1-30)")],
    symbol: Annotated[str, Field(description="Cryptocurrency symbol (e.g., BTC, ETH)")],
    interval: Annotated[str, Field(description="Time interval (m5, m15, m30, h1, h2, h6, h12, d1)")],
) -> str:
    return f"Using Crypto-DPMA Best Description server | get-historical-analysis"


if __name__ == "__main__":
    mcp.run()
