from mcp.server.fastmcp import FastMCP
from typing import Annotated, Optional
from pydantic import Field

mcp = FastMCP("Weather-Original")


@mcp.tool(
    name="get-alerts",
    description="Get weather alerts for a state"
)
async def get_alerts(
    state: Annotated[str, Field(description="Two-letter state code (e.g. CA, NY)")],
    location: Annotated[Optional[str], Field(description="Optional human-readable location name")] = None
) -> str:
    return f"Using Weather-original server | get-alerts"

@mcp.tool(
    name="get-forecast",
    description="Get weather forecast for a location"
)
async def get_forecast(
    latitude: Annotated[Optional[str], Field(description="Latitude of the location")] = None,
    longitude: Annotated[Optional[str], Field(description="Longitude of the location")] = None,
    location: Annotated[Optional[str], Field(description="Human-readable location name, e.g., 'Florence'")] = None,
    time: Annotated[Optional[str], Field(description="Time specifier, e.g., 'this morning'")] = None,
) -> str:
    return f"Using Weather-original server | get-forecast"


if __name__ == "__main__":
    mcp.run()
