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


mcp = FastMCP("Time-GAPMA Em")

@mcp.tool(
    name="current_time",
    description=TOOL_DESCRIPTIONS["Time"]["current_time"]["Em"]
)
async def current_time(
    format: Annotated[str, Field(description="The format of the time, default is empty string")],
    timezone: Annotated[str, Field(description="The timezone of the time, IANA timezone name, e.g. Asia/Shanghai")]
) -> str:
    return f"Using Time-GAPMA Em server | current_time"

@mcp.tool(
    name="relative_time",
    description=TOOL_DESCRIPTIONS["Time"]["relative_time"]["Em"]
)
async def relative_time(
    time: Annotated[str, Field(description="The time to get the relative time from now. Format: YYYY-MM-DD HH:mm:ss")]
) -> str:
    return f"Using Time-GAPMA Em server | relative_time"

@mcp.tool(
    name="days_in_month",
    description=TOOL_DESCRIPTIONS["Time"]["days_in_month"]["Em"]
)
async def days_in_month(
    date: Annotated[str, Field(description="The date to get the days in month. Format: YYYY-MM-DD")]
) -> str:
    return f"Using Time-GAPMA Em server | days_in_month"

@mcp.tool(
    name="get_timestamp",
    description=TOOL_DESCRIPTIONS["Time"]["get_timestamp"]["Em"]
)
async def get_timestamp(
    time: Annotated[str, Field(description="The time to get the timestamp. Format: YYYY-MM-DD HH:mm:ss")]
) -> str:
    return f"Using Time-GAPMA Em server | get_timestamp"

@mcp.tool(
    name="convert_time",
    description=TOOL_DESCRIPTIONS["Time"]["convert_time"]["Em"]
)
async def convert_time(
    time: Annotated[str, Field(description="Date and time in 24-hour format. e.g. 2025-03-23 12:30:00")],
    sourceTimezone: Annotated[str, Field(description="The source timezone. IANA timezone name, e.g. Asia/Shanghai")],
    targetTimezone: Annotated[str, Field(description="The target timezone. IANA timezone name, e.g. Europe/London")]
) -> str:
    return f"Using Time-GAPMA Em server | convert_time"


if __name__ == "__main__":
    mcp.run()
