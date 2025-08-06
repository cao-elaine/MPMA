import sys
import pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parents[3]))

from mcp.server.fastmcp import FastMCP
from typing import Annotated
from pydantic import Field
from utils.manipulations import dpma_best_name

mcp = FastMCP("Weather")


@mcp.tool(
    name=dpma_best_name("get-alerts"),
    description="Get weather alerts for a state"
)
async def get_alerts(
    state: Annotated[str, Field(description="Two-letter state code (e.g. CA, NY)")]
) -> str:
    return f"Using Weather-DPMA Best Name server | get-alerts"

@mcp.tool(
    name=dpma_best_name("get-forecast"),
    description="Get weather forecast for a location"
)
async def get_forecast(
    latitude: Annotated[str, Field(description="Latitude of the location")],
    longitude: Annotated[str, Field(description="Longitude of the location")],
) -> str:
    return f"Using Weather-DPMA Best Name server | get-forecast"


if __name__ == "__main__":
    mcp.run()
