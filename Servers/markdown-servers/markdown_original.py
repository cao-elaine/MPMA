from mcp.server.fastmcp import FastMCP
from typing import Annotated
from pydantic import Field

mcp = FastMCP("Markdown-Original")


@mcp.tool(
    name="youtube-to-markdown",
    description="Convert a YouTube video to markdown, including transcript if available"
)
async def youtube_to_markdown(
    url: Annotated[str, Field(description="URL of the YouTube video")]
) -> str:
    return f"Using Markdown-original server | youtube-to-markdown"


@mcp.tool(
    name="pdf-to-markdown",
    description="Convert a PDF file to markdown"
)
async def pdf_to_markdown(
    filepath: Annotated[str, Field(description="Absolute path of the PDF file to convert")]
) -> str:
    return f"Using Markdown-original server | pdf-to-markdown"


@mcp.tool(
    name="bing-search-to-markdown",
    description="Convert a Bing search results page to markdown"
)
async def bing_search_to_markdown(
    url: Annotated[str, Field(description="URL of the Bing search results page")]
) -> str:
    return f"Using Markdown-original server | bing-search-to-markdown"


@mcp.tool(
    name="webpage-to-markdown",
    description="Convert a webpage to markdown"
)
async def webpage_to_markdown(
    url: Annotated[str, Field(description="URL of the webpage to convert")]
) -> str:
    return f"Using Markdown-original server | webpage-to-markdown"

@mcp.tool(
    name="image-to-markdown",
    description="Convert an image to markdown, including metadata and description"
)
async def image_to_markdown(
    filepath: Annotated[str, Field(description="Absolute path of the image file to convert")]
) -> str:
    return f"Using Markdown-original server | image-to-markdown"


@mcp.tool(
    name="audio-to-markdown",
    description="Convert an audio file to markdown, including transcription if possible"
)
async def audio_to_markdown(
    filepath: Annotated[str, Field(description="Absolute path of the audio file to convert")]
) -> str:
    return f"Using Markdown-original server | audio-to-markdown"


@mcp.tool(
    name="docx-to-markdown",
    description="Convert a DOCX file to markdown"
)
async def docx_to_markdown(
    filepath: Annotated[str, Field(description="Absolute path of the DOCX file to convert")]
) -> str:
    return f"Using Markdown-original server | docx-to-markdown"


@mcp.tool(
    name="xlsx-to-markdown",
    description="Convert an XLSX file to markdown"
)
async def xlsx_to_markdown(
    filepath: Annotated[str, Field(description="Absolute path of the XLSX file to convert")]
) -> str:
    return f"Using Markdown-original server | xlsx-to-markdown"


@mcp.tool(
    name="pptx-to-markdown",
    description="Convert a PPTX file to markdown"
)
async def pptx_to_markdown(
    filepath: Annotated[str, Field(description="Absolute path of the PPTX file to convert")]
) -> str:
    return f"Using Markdown-original server | pptx-to-markdown"


@mcp.tool(
    name="get-markdown-file",
    description="Get a markdown file by absolute file path"
)
async def get_markdown_file(
    filepath: Annotated[str, Field(description="Absolute path to file of markdown'd text")]
) -> str:
    return f"Using Markdown-original server | get-markdown-file"


if __name__ == "__main__":
    mcp.run()
