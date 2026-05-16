"""MCP resources — expose HyperStore content as readable URIs."""

from __future__ import annotations

from typing import Any

from .config import Settings


def _format_app_markdown(app: dict[str, Any], site_url: str) -> str:
    """Render a HyperStore app payload as a compact markdown document."""
    categories = ", ".join(c["name"] for c in app.get("categories", [])) or "—"
    features = "\n".join(f"- {f}" for f in app.get("features", [])) or "_No features listed._"
    screenshots = "\n".join(f"- {s}" for s in app.get("screenshots", [])) or "_No screenshots._"
    rating = app.get("rating") or 0
    return f"""# {app["name"]}

> {app.get("short_description") or ""}

- **Website**: {app.get("website_url") or "—"}
- **Pricing**: {app.get("pricing_model") or "—"}
- **Open source**: {app.get("is_open_source")}
- **Has API**: {app.get("has_api")}
- **Rating**: {rating}
- **Popularity**: {app.get("popularity_score")}
- **Categories**: {categories}
- **HyperStore page**: {site_url}/{app["slug"]}

## Description

{app.get("long_description") or app.get("short_description") or ""}

## Features

{features}

## Screenshots

{screenshots}
"""


def _format_category_markdown(payload: dict[str, Any], site_url: str) -> str:
    cat = payload["category"]
    apps = payload.get("apps", [])
    lines = [
        f"# {cat['name']}",
        "",
        f"> {cat.get('description') or ''}",
        "",
        f"- **Slug**: `{cat['slug']}`",
        f"- **App count**: {cat.get('app_count')}",
        f"- **HyperStore page**: {site_url}/category/{cat['slug']}",
        "",
        "## Apps",
        "",
    ]
    if not apps:
        lines.append("_No apps yet._")
    for a in apps:
        desc = (a.get("short_description") or "").strip()
        lines.append(f"- **{a['name']}** ({a.get('pricing_model') or '—'}) — {desc} — {site_url}/{a['slug']}")
    return "\n".join(lines) + "\n"


def _format_catalog_markdown(categories: list[dict[str, Any]], site_url: str) -> str:
    lines = [
        "# HyperStore Catalog",
        "",
        f"All categories on {site_url}.",
        "",
    ]
    for c in categories:
        lines.append(
            f"- **{c['name']}** (`{c['slug']}`) — {c.get('app_count', 0)} apps — {site_url}/category/{c['slug']}"
        )
    return "\n".join(lines) + "\n"


def register_resources(mcp, client_factory, settings: Settings):
    """Register MCP resources for app, category and catalog."""
    site_url = settings.api_base_clean

    @mcp.resource(
        "hyperstore://app/{slug}",
        name="HyperStore App",
        description="Markdown rendering of a single AI app's detail page.",
        mime_type="text/markdown",
    )
    async def app_resource(slug: str) -> str:
        async with client_factory() as client:
            data = await client.get_app(slug)
        return _format_app_markdown(data, site_url)

    @mcp.resource(
        "hyperstore://category/{slug}",
        name="HyperStore Category",
        description="Markdown listing of the top apps in a HyperStore category.",
        mime_type="text/markdown",
    )
    async def category_resource(slug: str) -> str:
        async with client_factory() as client:
            data = await client.category_apps(slug, limit=20)
        return _format_category_markdown(data, site_url)

    @mcp.resource(
        "hyperstore://catalog",
        name="HyperStore Catalog",
        description="Index of all HyperStore categories with app counts.",
        mime_type="text/markdown",
    )
    async def catalog_resource() -> str:
        async with client_factory() as client:
            cats = await client.list_categories()
        return _format_catalog_markdown(cats, site_url)

    return [app_resource, category_resource, catalog_resource]
