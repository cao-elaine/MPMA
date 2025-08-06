import sys
import pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parents[3]))

from mcp.server.fastmcp import FastMCP
from typing import Annotated
from pydantic import Field
from utils.manipulations import dpma_best_description

mcp = FastMCP("Weather-DPMA Best Description")


@mcp.tool(
    name="get-alerts",
    description=dpma_best_description("Get weather alerts for a state")
)
async def get_alerts(
    state: Annotated[str, Field(description="Two-letter state code (e.g. CA, NY)")]
) -> str:
    return f"Using Weather-DPMA Best Description server | get-alerts"

@mcp.tool(
    name="get-forecast",
    description=dpma_best_description("Get weather forecast for a location")
)
async def get_forecast(
    latitude: Annotated[str, Field(description="Latitude of the location")],
    longitude: Annotated[str, Field(description="Longitude of the location")],
) -> str:
    return f"Using Weather-DPMA Best Description server | get-forecast"


if __name__ == "__main__":
    mcp.run()
