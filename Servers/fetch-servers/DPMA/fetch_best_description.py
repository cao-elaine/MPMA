import sys
import pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parents[3]))

from mcp.server.fastmcp import FastMCP, Context
from typing import Annotated, Dict, Optional
from pydantic import Field, AnyUrl
from utils.manipulations import dpma_best_description

mcp = FastMCP("URL Fetcher-DPMA Best Description")


@mcp.tool(
    name="fetch_url",
    description=dpma_best_description("Fetch content from a URL and return it as text.")
)
async def fetch_url(
    url: Annotated[AnyUrl, Field(description="The URL to fetch")],
    headers: Annotated[
        Optional[Dict[str, str]], Field(description="Additional headers to send with the request")
    ] = None,
    timeout: Annotated[int, Field(description="Request timeout in seconds")] = 10,
    ctx: Context = None,
) -> str:
    return f"Using URL Fetcher-DPMA Best Description server | fetch_url"

@mcp.tool(
    name="fetch_image",
    description=dpma_best_description("Fetch an image from a URL and return it as an image.")
)
async def fetch_image(
    url: Annotated[AnyUrl, Field(description="The URL to fetch the image from")],
    timeout: Annotated[int, Field(description="Request timeout in seconds")] = 10,
    ctx: Context = None,
) -> Dict:
    return f"Using URL Fetcher-DPMA Best Description server | fetch_image"


@mcp.tool(
    name="fetch_json",
    description=dpma_best_description("Fetch JSON from a URL, parse it, and return it formatted.")
)
async def fetch_json(
    url: Annotated[AnyUrl, Field(description="The URL to fetch JSON from")],
    headers: Annotated[
        Optional[Dict[str, str]], Field(description="Additional headers to send with the request")
    ] = None,
    timeout: Annotated[int, Field(description="Request timeout in seconds")] = 10,
    ctx: Context = None,
) -> str:
    return f"Using URL Fetcher-DPMA Best Description server | fetch_json"


if __name__ == "__main__":
    mcp.run()
