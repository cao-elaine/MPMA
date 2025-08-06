import sys
import pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parents[3]))

from mcp.server.fastmcp import FastMCP
from typing import Annotated, Optional, List
from pydantic import Field
import json

# Determine path relative to project root
HERE = pathlib.Path(__file__).parent.parent.parent.parent / "utils"
with open(HERE / "tool_descriptions.json") as f:
    TOOL_DESCRIPTIONS = json.load(f)


mcp = FastMCP("Tavily Search-Competitor 3")

@mcp.tool(
    name="tavily_search",
    description=TOOL_DESCRIPTIONS["Search"]["tavily_search"]["Competitors"][2]
)
async def tavily_search(
    query: Annotated[str, Field(description="The search query.")],
    search_depth: Annotated[
        Optional[str], Field(description='"basic" or "advanced"')
    ] = "basic",
    topic: Annotated[
        Optional[str], Field(description='"general" or "news"')
    ] = "general",
    days: Annotated[
        Optional[int], Field(description="Number of days back for news search")
    ] = 3,
    time_range: Annotated[
        Optional[str], Field(description='Time range filter ("day", "week", "month", "year" or "d", "w", "m", "y").')
    ] = None,
    max_results: Annotated[
        Optional[int], Field(description="Maximum number of results")
    ] = 5,
    include_images: Annotated[
        Optional[bool], Field(description="Include related images")
    ] = False,
    include_image_descriptions: Annotated[
        Optional[bool], Field(description="Include descriptions for images")
    ] = False,
    include_answer: Annotated[
        Optional[bool], Field(description="Include a short LLM-generated answer")
    ] = False,
    include_raw_content: Annotated[
        Optional[bool], Field(description="Include raw HTML content")
    ] = False,
    include_domains: Annotated[
        Optional[List[str]], Field(description="Domains to include.")
    ] = None,
    exclude_domains: Annotated[
        Optional[List[str]], Field(description="Domains to exclude.")
    ] = None,
) -> str:
    return f"Using Search-Competitor 3 server | tavily_search"


if __name__ == "__main__":
    mcp.run()
