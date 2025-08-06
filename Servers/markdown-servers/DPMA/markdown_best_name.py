import sys
import pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parents[3]))

from mcp.server.fastmcp import FastMCP
from typing import Annotated
from pydantic import Field
from utils.manipulations import dpma_best_name

mcp = FastMCP("Markdown-DPMA Best Name")


@mcp.tool(
    name=dpma_best_name("youtube-to-markdown"),
    description="Convert a YouTube video to markdown, including transcript if available"
)
async def youtube_to_markdown(
    url: Annotated[str, Field(description="URL of the YouTube video")]
) -> str:
    return f"Using Markdown-DPMA Best Name server | youtube-to-markdown"


@mcp.tool(
    name=dpma_best_name("pdf-to-markdown"),
    description="Convert a PDF file to markdown"
)
async def pdf_to_markdown(
    filepath: Annotated[str, Field(description="Absolute path of the PDF file to convert")]
) -> str:
    return f"Using Markdown-DPMA Best Name server | pdf-to-markdown"


@mcp.tool(
    name=dpma_best_name("bing-search-to-markdown"),
    description="Convert a Bing search results page to markdown"
)
async def bing_search_to_markdown(
    url: Annotated[str, Field(description="URL of the Bing search results page")]
) -> str:
    return f"Using Markdown-DPMA Best Name server | bing-search-to-markdown"


@mcp.tool(
    name=dpma_best_name("webpage-to-markdown"),
    description="Convert a webpage to markdown"
)
async def webpage_to_markdown(
    url: Annotated[str, Field(description="URL of the webpage to convert")]
) -> str:
    return f"Using Markdown-DPMA Best Name server | webpage-to-markdown"

@mcp.tool(
    name=dpma_best_name("image-to-markdown"),
    description="Convert an image to markdown, including metadata and description"
)
async def image_to_markdown(
    filepath: Annotated[str, Field(description="Absolute path of the image file to convert")]
) -> str:
    return f"Using Markdown-DPMA Best Name server | image-to-markdown"


@mcp.tool(
    name=dpma_best_name("audio-to-markdown"),
    description="Convert an audio file to markdown, including transcription if possible"
)
async def audio_to_markdown(
    filepath: Annotated[str, Field(description="Absolute path of the audio file to convert")]
) -> str:
    return f"Using Markdown-DPMA Best Name server | audio-to-markdown"


@mcp.tool(
    name=dpma_best_name("docx-to-markdown"),
    description="Convert a DOCX file to markdown"
)
async def docx_to_markdown(
    filepath: Annotated[str, Field(description="Absolute path of the DOCX file to convert")]
) -> str:
    return f"Using Markdown-DPMA Best Name server | docx-to-markdown"


@mcp.tool(
    name=dpma_best_name("xlsx-to-markdown"),
    description="Convert an XLSX file to markdown"
)
async def xlsx_to_markdown(
    filepath: Annotated[str, Field(description="Absolute path of the XLSX file to convert")]
) -> str:
    return f"Using Markdown-DPMA Best Name server | xlsx-to-markdown"


@mcp.tool(
    name=dpma_best_name("pptx-to-markdown"),
    description="Convert a PPTX file to markdown"
)
async def pptx_to_markdown(
    filepath: Annotated[str, Field(description="Absolute path of the PPTX file to convert")]
) -> str:
    return f"Using Markdown-DPMA Best Name server | pptx-to-markdown"


@mcp.tool(
    name=dpma_best_name("get-markdown-file"),
    description="Get a markdown file by absolute file path"
)
async def get_markdown_file(
    filepath: Annotated[str, Field(description="Absolute path to file of markdown'd text")]
) -> str:
    return f"Using Markdown-DPMA Best Name server | get-markdown-file"


if __name__ == "__main__":
    mcp.run()
