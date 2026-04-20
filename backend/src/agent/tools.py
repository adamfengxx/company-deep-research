from langchain_tavily import TavilySearch
from agent.config import settings


def get_web_search_tool(max_results: int = 5) -> TavilySearch:
    return TavilySearch(
        max_results=max_results,
        tavily_api_key=settings.tavily_api_key,
    )
