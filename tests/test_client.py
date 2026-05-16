"""Contract tests for HyperStoreClient against mocked HTTP responses."""

from __future__ import annotations

import pytest

from hyperstore_mcp.client import HyperStoreClient, HyperStoreError
from hyperstore_mcp.config import Settings


@pytest.fixture
def settings() -> Settings:
    return Settings(HYPERSTORE_API_BASE="https://store.hypergpt.ai")  # type: ignore[call-arg]


async def test_search_calls_search_endpoint(httpx_mock, settings):
    httpx_mock.add_response(
        url="https://store.hypergpt.ai/api/search?q=chatgpt&limit=24",
        json={"query": "chatgpt", "apps": [], "next_cursor": None},
    )
    async with HyperStoreClient(settings) as client:
        result = await client.search("chatgpt")
    assert result == {"query": "chatgpt", "apps": [], "next_cursor": None}


async def test_get_app_404_raises(httpx_mock, settings):
    httpx_mock.add_response(
        url="https://store.hypergpt.ai/api/apps/nope",
        status_code=404,
        json={"detail": "App not found"},
    )
    async with HyperStoreClient(settings) as client:
        with pytest.raises(HyperStoreError) as exc:
            await client.get_app("nope")
    assert exc.value.status == 404
    assert "App not found" in exc.value.message


async def test_ai_search_posts_prompt(httpx_mock, settings):
    httpx_mock.add_response(
        url="https://store.hypergpt.ai/api/ai-search",
        method="POST",
        match_json={"prompt": "image upscaler", "turnstile_token": ""},
        json={"apps": [], "message": "Found 0 AI tools matching your request"},
    )
    async with HyperStoreClient(settings) as client:
        result = await client.ai_search("image upscaler")
    assert "message" in result


async def test_list_apps_drops_none_params(httpx_mock, settings):
    httpx_mock.add_response(
        url="https://store.hypergpt.ai/api/apps?limit=24",
        json={"apps": [], "next_cursor": None},
    )
    async with HyperStoreClient(settings) as client:
        result = await client.list_apps()
    assert result == {"apps": [], "next_cursor": None}
