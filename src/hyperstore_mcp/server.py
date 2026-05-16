"""HyperStore FastMCP server — registers all tools, resources, and prompts."""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from mcp.server.fastmcp import FastMCP

from . import __version__
from .client import HyperStoreClient
from .config import Settings, get_settings
from .prompts import register_prompts
from .resources import register_resources
from .tools import register_tools


def build_server(settings: Settings | None = None) -> FastMCP:
    """Construct a FastMCP server wired up with HyperStore tools, resources, and prompts."""
    settings = settings or get_settings()

    mcp = FastMCP(
        name="hyperstore",
        instructions=(
            "HyperStore MCP — search and inspect 1000+ curated AI applications. "
            "Use `ai_search` for natural-language queries, `search_apps` for keyword "
            "searches, `list_categories` to browse topics, and `get_app` for full detail. "
            "All data comes from store.hypergpt.ai and is read-only."
        ),
    )

    @asynccontextmanager
    async def client_factory() -> AsyncIterator[HyperStoreClient]:
        client = HyperStoreClient(settings)
        try:
            yield client
        finally:
            await client.aclose()

    register_tools(mcp, client_factory)
    register_resources(mcp, client_factory, settings)
    register_prompts(mcp)

    return mcp


__all__ = ["__version__", "build_server"]
