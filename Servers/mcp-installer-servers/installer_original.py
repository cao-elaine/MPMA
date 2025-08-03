from mcp.server.fastmcp import FastMCP
from typing import Annotated
from pydantic import Field

mcp = FastMCP("MCP Installer-Original")

@mcp.tool(
    name="install_repo_mcp_server",
    description="Install an MCP server via npx or uvx"
)
async def install_repo_mcp_server(
    name: Annotated[str, Field(description="The package name of the MCP server")],
    args: Annotated[list[str], Field(description="The arguments to pass along")],
    env: Annotated[list[str], Field(description="The environment variables to set, delimited by =")]
) -> str:
    return f"Using MCP Installer-Original server | install_repo_mcp_server"

@mcp.tool(
    name="install_local_mcp_server",
    description="Install an MCP server whose code is cloned locally on your computer"
)
async def install_local_mcp_server(
    path: Annotated[str, Field(description="The path to the MCP server code cloned on your computer")],
    args: Annotated[list[str], Field(description="The arguments to pass along")],
    env: Annotated[list[str], Field(description="The environment variables to set, delimited by =")]
) -> str:
    return f"Using MCP Installer-Original server | install_local_mcp_server"



if __name__ == "__main__":
    mcp.run()
