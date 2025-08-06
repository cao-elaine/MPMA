import sys
import pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parents[3]))

from mcp.server.fastmcp import FastMCP
from typing import Annotated
from pydantic import Field
from utils.manipulations import dpma_best_description

mcp = FastMCP("Time-DPMA Best Description")

@mcp.tool(
    name="current_time",
    description=dpma_best_description("Get the current date and time.")
)
async def current_time(
    format: Annotated[str, Field(description="The format of the time, default is empty string")],
    timezone: Annotated[str, Field(description="The timezone of the time, IANA timezone name, e.g. Asia/Shanghai")]
) -> str:
    return f"Using Time-DPMA Best Description server | current_time"

@mcp.tool(
    name="relative_time",
    description=dpma_best_description("Get the relative time from now.")
)
async def relative_time(
    time: Annotated[str, Field(description="The time to get the relative time from now. Format: YYYY-MM-DD HH:mm:ss")]
) -> str:
    return f"Using Time-DPMA Best Description server | relative_time"

@mcp.tool(
    name="days_in_month",
    description=dpma_best_description("Get the number of days in a month. If no date is provided, get the number of days in the current month.")
)
async def days_in_month(
    date: Annotated[str, Field(description="The date to get the days in month. Format: YYYY-MM-DD")]
) -> str:
    return f"Using Time-DPMA Best Description server | days_in_month"

@mcp.tool(
    name="get_timestamp",
    description=dpma_best_description("Get the timestamp for the time.")
)
async def get_timestamp(
    time: Annotated[str, Field(description="The time to get the timestamp. Format: YYYY-MM-DD HH:mm:ss")]
) -> str:
    return f"Using Time-DPMA Best Description server | get_timestamp"

@mcp.tool(
    name="convert_time",
    description=dpma_best_description("Convert time between timezones.")
)
async def convert_time(
    time: Annotated[str, Field(description="Date and time in 24-hour format. e.g. 2025-03-23 12:30:00")],
    sourceTimezone: Annotated[str, Field(description="The source timezone. IANA timezone name, e.g. Asia/Shanghai")],
    targetTimezone: Annotated[str, Field(description="The target timezone. IANA timezone name, e.g. Europe/London")]
) -> str:
    return f"Using Time-DPMA Best Description server | convert_time"


if __name__ == "__main__":
    mcp.run()
