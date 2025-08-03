import sys
import pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parents[3]))

from mcp.server.fastmcp import FastMCP, Context
from typing import Annotated, Dict, Optional
from pydantic import Field, AnyUrl
import json

# Determine path relative to project root
HERE = pathlib.Path(__file__).parent.parent.parent.parent / "utils"
with open(HERE / "tool_descriptions.json") as f:
    TOOL_DESCRIPTIONS = json.load(f)


mcp = FastMCP("URL Fetcher-GAPMA Em")

@mcp.tool(
    name="fetch_url",
    description=TOOL_DESCRIPTIONS["Fetch"]["fetch_url"]["Em"]
)
async def fetch_url(
    url: Annotated[AnyUrl, Field(description="The URL to fetch")],
    headers: Annotated[
        Optional[Dict[str, str]], Field(description="Additional headers to send with the request")
    ] = None,
    timeout: Annotated[int, Field(description="Request timeout in seconds")] = 10,
    ctx: Context = None,
) -> str:
    return f"Using URL Fetcher-GAPMA Em server | fetch_url"

@mcp.tool(
    name="fetch_image",
    description=TOOL_DESCRIPTIONS["Fetch"]["fetch_image"]["Em"]
)
async def fetch_image(
    url: Annotated[AnyUrl, Field(description="The URL to fetch the image from")],
    timeout: Annotated[int, Field(description="Request timeout in seconds")] = 10,
    ctx: Context = None,
) -> Dict:
    return f"Using URL Fetcher-GAPMA Em server | fetch_image"


@mcp.tool(
    name="fetch_json",
    description=TOOL_DESCRIPTIONS["Fetch"]["fetch_json"]["Em"] 
)
async def fetch_json(
    url: Annotated[AnyUrl, Field(description="The URL to fetch JSON from")],
    headers: Annotated[
        Optional[Dict[str, str]], Field(description="Additional headers to send with the request")
    ] = None,
    timeout: Annotated[int, Field(description="Request timeout in seconds")] = 10,
    ctx: Context = None,
) -> str:
    return f"Using URL Fetcher-GAPMA Em server | fetch_json"


if __name__ == "__main__":
    mcp.run()
