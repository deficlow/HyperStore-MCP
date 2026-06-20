"""MCP tool definitions. Each function maps to one HyperStore endpoint."""

from __future__ import annotations

from typing import Annotated

from pydantic import Field

# Common type aliases for tool params — keep schemas readable to the LLM.
Slug = Annotated[str, Field(description="URL slug, e.g. 'chatgpt' or 'ai-image-tools'.")]
Limit = Annotated[int, Field(default=24, ge=1, le=48, description="Max results per page.")]
Cursor = Annotated[int | None, Field(default=None, description="Pagination cursor (app id from prior page).")]
Pricing = Annotated[
    str | None,
    Field(
        default=None,
        description="Filter by pricing model: 'free', 'freemium', 'paid', 'free-trial', 'subscription', or 'one-time'.",
    ),
]


def register_tools(mcp, client_factory):
    """Register all HyperStore tools on a FastMCP instance.

    `client_factory` is a callable that returns an awaitable yielding a
    `HyperStoreClient` for the lifetime of one tool invocation.
    """

    @mcp.tool(
        name="search_apps",
        description=(
            "Search HyperStore's AI apps directory by keyword. Returns a paginated list of "
            "matching apps with name, slug, short description, pricing, and rating. "
            "Use this when the user gives concrete keywords (e.g. 'image upscaler', 'code copilot')."
        ),
    )
    async def search_apps(
        query: Annotated[str, Field(min_length=1, max_length=200, description="Search query.")],
        limit: Limit = 24,
        cursor: Cursor = None,
    ) -> dict:
        async with client_factory() as client:
            return await client.search(query, cursor=cursor, limit=limit)

    @mcp.tool(
        name="ai_search",
        description=(
            "Natural-language semantic search powered by embeddings. Best for fuzzy intent "
            "('a tool that helps me write Python tests', 'something like Midjourney but free'). "
            "Returns up to 12 apps ranked by semantic similarity."
        ),
    )
    async def ai_search(
        prompt: Annotated[str, Field(min_length=2, max_length=500, description="Natural-language description of what the user is looking for.")],
    ) -> dict:
        async with client_factory() as client:
            return await client.ai_search(prompt)

    @mcp.tool(
        name="get_app",
        description=(
            "Fetch the full detail page for a single AI app by slug: long description, features, "
            "screenshots, categories, pricing, rating, website URL, source attribution."
        ),
    )
    async def get_app(slug: Slug) -> dict:
        async with client_factory() as client:
            return await client.get_app(slug)

    @mcp.tool(
        name="list_apps",
        description=(
            "Paginated apps listing with optional filters. Combine `category`, `pricing`, and a "
            "free-text `query` to drill down. Returns apps sorted by popularity. Use `cursor` "
            "(last app id from previous page) to paginate."
        ),
    )
    async def list_apps(
        category: Annotated[str | None, Field(default=None, description="Optional category slug to filter by.")] = None,
        pricing: Pricing = None,
        query: Annotated[str | None, Field(default=None, max_length=200, description="Optional keyword filter.")] = None,
        cursor: Cursor = None,
        limit: Limit = 24,
    ) -> dict:
        async with client_factory() as client:
            return await client.list_apps(
                query=query,
                pricing=pricing,
                category=category,
                cursor=cursor,
                limit=limit,
            )

    @mcp.tool(
        name="list_categories",
        description=(
            "List all HyperStore categories with app counts. Use this first when the user asks "
            "'what kinds of AI tools are there?' or to discover available category slugs."
        ),
    )
    async def list_categories() -> list[dict]:
        async with client_factory() as client:
            return await client.list_categories()

    @mcp.tool(
        name="category_apps",
        description=(
            "Get apps within a specific category. Returns the category metadata plus a paginated "
            "list of apps in that category, sorted by popularity."
        ),
    )
    async def category_apps(
        slug: Slug,
        pricing: Pricing = None,
        cursor: Cursor = None,
        limit: Limit = 24,
    ) -> dict:
        async with client_factory() as client:
            return await client.category_apps(slug, pricing=pricing, cursor=cursor, limit=limit)

    @mcp.tool(
        name="browse_apps",
        description=(
            "Browse apps A-Z by starting letter. Use letter='#' for apps starting with digits or "
            "symbols. Useful for alphabetical discovery rather than search."
        ),
    )
    async def browse_apps(
        letter: Annotated[str, Field(min_length=1, max_length=1, description="A single letter A-Z, or '#' for digits/symbols.")],
        pricing: Pricing = None,
        cursor: Cursor = None,
        limit: Limit = 24,
    ) -> dict:
        async with client_factory() as client:
            return await client.browse(letter, pricing=pricing, cursor=cursor, limit=limit)

    @mcp.tool(
        name="get_homepage",
        description=(
            "Fetch the HyperStore homepage payload: top categories with their featured apps, "
            "the trending apps strip, and totals. Good first call to give the user a broad overview."
        ),
    )
    async def get_homepage(
        page: Annotated[int, Field(default=1, ge=1, description="Homepage pagination — page 1 returns trending + stats.")] = 1,
    ) -> dict:
        async with client_factory() as client:
            return await client.homepage(page=page)

    @mcp.tool(
        name="get_alternatives",
        description=(
            "Get curated alternatives to a specific AI app by slug. Returns the app plus a list "
            "of competing/similar tools ranked by match confidence. Use this when the user asks "
            "'what are alternatives to X', 'something like X', or 'X vs others'."
        ),
    )
    async def get_alternatives(slug: Slug, limit: Limit = 24) -> dict:
        async with client_factory() as client:
            return await client.app_alternatives(slug, limit=limit)

    @mcp.tool(
        name="list_audiences",
        description=(
            "List the audience segments HyperStore curates tools for (e.g. 'developers', "
            "'lawyers', 'students'), each with a slug and app count. Call this first to discover "
            "audience slugs for `apps_for_audience`."
        ),
    )
    async def list_audiences() -> list[dict]:
        async with client_factory() as client:
            return await client.list_audiences()

    @mcp.tool(
        name="apps_for_audience",
        description=(
            "Get the best AI tools for a specific audience by slug (from `list_audiences`), "
            "ranked by relevance then popularity. Use when the user asks 'best AI tools for "
            "{role/profession}'. Paginate with `cursor` (last app id from the previous page)."
        ),
    )
    async def apps_for_audience(slug: Slug, cursor: Cursor = None, limit: Limit = 24) -> dict:
        async with client_factory() as client:
            return await client.audience_apps(slug, cursor=cursor, limit=limit)

    @mcp.tool(
        name="list_use_cases",
        description=(
            "List the use-case taxonomies HyperStore curates tools for (e.g. 'legal-contracts', "
            "'tiktok-shorts'), each with a slug and app count. Call this first to discover "
            "use-case slugs for `apps_for_use_case`."
        ),
    )
    async def list_use_cases() -> list[dict]:
        async with client_factory() as client:
            return await client.list_use_cases()

    @mcp.tool(
        name="apps_for_use_case",
        description=(
            "Get AI tools for a specific use case by slug (from `list_use_cases`), ranked by "
            "relevance then popularity. Use when the user asks 'AI tools for {task}'. Paginate "
            "with `cursor` (last app id from the previous page)."
        ),
    )
    async def apps_for_use_case(slug: Slug, cursor: Cursor = None, limit: Limit = 24) -> dict:
        async with client_factory() as client:
            return await client.use_case_apps(slug, cursor=cursor, limit=limit)

    return [
        search_apps,
        ai_search,
        get_app,
        list_apps,
        list_categories,
        category_apps,
        browse_apps,
        get_homepage,
        get_alternatives,
        list_audiences,
        apps_for_audience,
        list_use_cases,
        apps_for_use_case,
    ]
