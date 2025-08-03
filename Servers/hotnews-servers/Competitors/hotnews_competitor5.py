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


mcp = FastMCP("HotNews-Competitor 5")


@mcp.tool(
    name="get_hot_news",
    description=TOOL_DESCRIPTIONS["HotNews"]["get_hot_news"]["Competitors"][4]
)
async def get_hot_news(
    sources: Annotated[list[str], Field(
        description="Available HotNews sources (ID: Platform): " \
        "{ID: 1, Platform: 'Zhihu Hot List (知乎热榜)'}, " \
        "{ID: 2, Platform: '36Kr Hot List (36氪热榜)'}, " \
        "{ID: 3, Platform: 'Baidu Hot Discussion (百度热点)'}, " \
        "{ID: 4, Platform: 'Bilibili Hot List (B站热榜)'}, " \
        "{ID: 5, Platform: 'Weibo Hot Search (微博热搜)'}, " \
        "{ID: 6, Platform: 'Douyin Hot List (抖音热点)'}, " \
        "{ID: 7, Platform: 'Hupu Hot List (虎扑热榜)'}, " \
        "{ID: 8, Platform: 'Douban Hot List (豆瓣热榜)'}, " \
        "{ID: 9, Platform: 'IT News (IT新闻)'} " \
        "Example usage: - [3]: Get Baidu Hot Discussion only "
        "- [1,3,7]: Get hot lists from zhihuHot, Baidu, and huPu "
        "- [1,2,3,4]: Get hot lists from zhihuHot, 36Kr, Baidu, and Bilibili")]
) -> str:
    return f"Using HotNews-Competitor 5 server | get_hot_news"


if __name__ == "__main__":
    mcp.run()
