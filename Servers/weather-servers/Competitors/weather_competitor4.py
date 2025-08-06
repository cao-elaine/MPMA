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


mcp = FastMCP("Weather-Competitor 4")


@mcp.tool(
    name="get-alerts",
    description=TOOL_DESCRIPTIONS["Weather"]["get-alerts"]["Competitors"][3]
)
async def get_alerts(
    state: Annotated[str, Field(description="Two-letter state code (e.g. CA, NY)")]
) -> str:
    return f"Using Weather-Competitor 4 server | get-alerts"

@mcp.tool(
    name="get-forecast",
    description=TOOL_DESCRIPTIONS["Weather"]["get-forecast"]["Competitors"][3]
)
async def get_forecast(
    latitude: Annotated[str, Field(description="Latitude of the location")],
    longitude: Annotated[str, Field(description="Longitude of the location")],
) -> str:
    return f"Using Weather-Competitor 4 server | get-forecast"


if __name__ == "__main__":
    mcp.run()
