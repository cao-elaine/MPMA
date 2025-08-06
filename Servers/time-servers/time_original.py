from mcp.server.fastmcp import FastMCP
from typing import Annotated
from pydantic import Field

mcp = FastMCP("Time-Original")

@mcp.tool(
    name="current_time",
    description="Get the current date and time."
)
async def current_time(
    format: Annotated[str, Field(description="The format of the time, default is empty string")],
    timezone: Annotated[str, Field(description="The timezone of the time, IANA timezone name, e.g. Asia/Shanghai")]
) -> str:
    return f"Using Time-original server | current_time"

@mcp.tool(
    name="relative_time",
    description="Get the relative time from now."
)
async def relative_time(
    time: Annotated[str, Field(description="The time to get the relative time from now. Format: YYYY-MM-DD HH:mm:ss")]
) -> str:
    return f"Using Time-original server | relative_time"

@mcp.tool(
    name="days_in_month",
    description="Get the number of days in a month. If no date is provided, get the number of days in the current month."
)
async def days_in_month(
    date: Annotated[str, Field(description="The date to get the days in month. Format: YYYY-MM-DD")]
) -> str:
    return f"Using Time-original server | days_in_month"

@mcp.tool(
    name="get_timestamp",
    description="Get the timestamp for the time."
)
async def get_timestamp(
    time: Annotated[str, Field(description="The time to get the timestamp. Format: YYYY-MM-DD HH:mm:ss")]
) -> str:
    return f"Using Time-original server | get_timestamp"

@mcp.tool(
    name="convert_time",
    description="Convert time between timezones."
)
async def convert_time(
    time: Annotated[str, Field(description="Date and time in 24-hour format. e.g. 2025-03-23 12:30:00")],
    sourceTimezone: Annotated[str, Field(description="The source timezone. IANA timezone name, e.g. Asia/Shanghai")],
    targetTimezone: Annotated[str, Field(description="The target timezone. IANA timezone name, e.g. Europe/London")]
) -> str:
    return f"Using Time-original server | convert_time"


if __name__ == "__main__":
    mcp.run()
