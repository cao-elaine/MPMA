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


mcp = FastMCP("MCP Installer-Competitor 5")

@mcp.tool(
    name="install_repo_mcp_server",
    description=TOOL_DESCRIPTIONS["MCP Installer"]["install_repo_mcp_server"]["Competitors"][4]
)
async def install_repo_mcp_server(
    name: Annotated[str, Field(description="The package name of the MCP server")],
    args: Annotated[list[str], Field(description="The arguments to pass along")],
    env: Annotated[list[str], Field(description="The environment variables to set, delimited by =")]
) -> str:
    return f"Using MCP Installer-Competitor 5 server | install_repo_mcp_server"

@mcp.tool(
    name="install_local_mcp_server",
    description=TOOL_DESCRIPTIONS["MCP Installer"]["install_local_mcp_server"]["Competitors"][4]
)
async def install_local_mcp_server(
    path: Annotated[str, Field(description="The path to the MCP server code cloned on your computer")],
    args: Annotated[list[str], Field(description="The arguments to pass along")],
    env: Annotated[list[str], Field(description="The environment variables to set, delimited by =")]
) -> str:
    return f"Using MCP Installer-Competitor 5 server | install_local_mcp_server"

if __name__ == "__main__":
    mcp.run()
