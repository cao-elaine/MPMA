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


mcp = FastMCP("Markdown-Competitor 5")


@mcp.tool(
    name="youtube-to-markdown",
    description=TOOL_DESCRIPTIONS["Markdown"]["youtube-to-markdown"]["Competitors"][4]
)
async def youtube_to_markdown(
    url: Annotated[str, Field(description="URL of the YouTube video")]
) -> str:
    return f"Using Markdown-Competitor 5 server | youtube-to-markdown"


@mcp.tool(
    name="pdf-to-markdown",
    description=TOOL_DESCRIPTIONS["Markdown"]["pdf-to-markdown"]["Competitors"][4]
)
async def pdf_to_markdown(
    filepath: Annotated[str, Field(description="Absolute path of the PDF file to convert")]
) -> str:
    return f"Using Markdown-Competitor 5 server | pdf-to-markdown"


@mcp.tool(
    name="bing-search-to-markdown",
    description=TOOL_DESCRIPTIONS["Markdown"]["bing-search-to-markdown"]["Competitors"][4]
)
async def bing_search_to_markdown(
    url: Annotated[str, Field(description="URL of the Bing search results page")]
) -> str:
    return f"Using Markdown-Competitor 5 server | bing-search-to-markdown"


@mcp.tool(
    name="webpage-to-markdown",
    description=TOOL_DESCRIPTIONS["Markdown"]["webpage-to-markdown"]["Competitors"][4]
)
async def webpage_to_markdown(
    url: Annotated[str, Field(description="URL of the webpage to convert")]
) -> str:
    return f"Using Markdown-Competitor 5 server | webpage-to-markdown"

@mcp.tool(
    name="image-to-markdown",
    description=TOOL_DESCRIPTIONS["Markdown"]["image-to-markdown"]["Competitors"][4]
)
async def image_to_markdown(
    filepath: Annotated[str, Field(description="Absolute path of the image file to convert")]
) -> str:
    return f"Using Markdown-Competitor 5 server | image-to-markdown"


@mcp.tool(
    name="audio-to-markdown",
    description=TOOL_DESCRIPTIONS["Markdown"]["audio-to-markdown"]["Competitors"][4]
)
async def audio_to_markdown(
    filepath: Annotated[str, Field(description="Absolute path of the audio file to convert")]
) -> str:
    return f"Using Markdown-Competitor 5 server | audio-to-markdown"


@mcp.tool(
    name="docx-to-markdown",
    description=TOOL_DESCRIPTIONS["Markdown"]["docx-to-markdown"]["Competitors"][4]
)
async def docx_to_markdown(
    filepath: Annotated[str, Field(description="Absolute path of the DOCX file to convert")]
) -> str:
    return f"Using Markdown-Competitor 5 server | docx-to-markdown"


@mcp.tool(
    name="xlsx-to-markdown",
    description=TOOL_DESCRIPTIONS["Markdown"]["xlsx-to-markdown"]["Competitors"][4]
)
async def xlsx_to_markdown(
    filepath: Annotated[str, Field(description="Absolute path of the XLSX file to convert")]
) -> str:
    return f"Using Markdown-Competitor 5 server | xlsx-to-markdown"


@mcp.tool(
    name="pptx-to-markdown",
    description=TOOL_DESCRIPTIONS["Markdown"]["pptx-to-markdown"]["Competitors"][4]
)
async def pptx_to_markdown(
    filepath: Annotated[str, Field(description="Absolute path of the PPTX file to convert")]
) -> str:
    return f"Using Markdown-Competitor 5 server | pptx-to-markdown"


@mcp.tool(
    name="get-markdown-file",
    description=TOOL_DESCRIPTIONS["Markdown"]["get-markdown-file"]["Competitors"][4]
)
async def get_markdown_file(
    filepath: Annotated[str, Field(description="Absolute path to file of markdown'd text")]
) -> str:
    return f"Using Markdown-Competitor 5 server | get-markdown-file"


if __name__ == "__main__":
    mcp.run()
