"""Smoke test: server builds and registers expected tools/resources/prompts."""

from __future__ import annotations

import pytest

from hyperstore_mcp.config import Settings
from hyperstore_mcp.server import build_server


@pytest.fixture
def settings() -> Settings:
    return Settings(HYPERSTORE_API_BASE="https://store.hypergpt.ai")  # type: ignore[call-arg]


async def test_server_registers_eight_tools(settings):
    mcp = build_server(settings)
    tools = await mcp.list_tools()
    names = {t.name for t in tools}
    assert names == {
        "search_apps",
        "ai_search",
        "get_app",
        "list_apps",
        "list_categories",
        "category_apps",
        "browse_apps",
        "get_homepage",
    }


async def test_server_registers_resources_and_prompts(settings):
    mcp = build_server(settings)
    resource_templates = await mcp.list_resource_templates()
    template_uris = {t.uriTemplate for t in resource_templates}
    assert "hyperstore://app/{slug}" in template_uris
    assert "hyperstore://category/{slug}" in template_uris

    static_resources = await mcp.list_resources()
    static_uris = {str(r.uri) for r in static_resources}
    assert "hyperstore://catalog" in static_uris

    prompts = await mcp.list_prompts()
    prompt_names = {p.name for p in prompts}
    assert prompt_names == {"find_tool_for_task", "compare_apps", "discover_category"}
