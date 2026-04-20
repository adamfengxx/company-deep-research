import logging
from contextlib import asynccontextmanager
from langchain_mcp_adapters.client import MultiServerMCPClient
from agent.config import settings

logger = logging.getLogger(__name__)

@asynccontextmanager
async def mcp_client():
    logger.info("Opening MCP client")
    client = MultiServerMCPClient({
        "alphavantage": {
            "url": f"https://mcp.alphavantage.co/mcp?apikey={settings.alphavantage_api_key}",
            "transport": "http",
        }
    })
    try:
        yield client
    finally:
        logger.info("Closing MCP client")



async def get_mcp_tools() -> list:
    logger.info("Loading MCP tools")

    try:
         async with mcp_client() as client:
            tools = await client.get_tools()
    except Exception:
        logger.exception("Failed to load MCP tools")
        raise

    logger.info("Loaded MCP tools", extra={"tool_count": len(tools)})
    return tools
