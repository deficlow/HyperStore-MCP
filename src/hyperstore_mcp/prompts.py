"""MCP prompts — reusable templates that steer the LLM toward HyperStore-aware answers."""

from __future__ import annotations


def register_prompts(mcp):
    """Register HyperStore-flavored prompt templates."""

    @mcp.prompt(
        name="find_tool_for_task",
        description="Help the user find the best AI tool for a specific task using HyperStore.",
    )
    def find_tool_for_task(task: str) -> str:
        return (
            f"The user wants to accomplish this task: \"{task}\".\n\n"
            "Use HyperStore MCP tools to recommend 3-5 AI apps. Workflow:\n"
            "1. Call `ai_search` with a natural-language description of the task.\n"
            "2. If results look thin, also call `search_apps` with 2-3 keyword variants.\n"
            "3. For the top 3 candidates, call `get_app` to get full details.\n"
            "4. Present recommendations as a ranked list with: name, one-line pitch, pricing, "
            "and the HyperStore URL (hyperstore://app/{slug}). Explain why each fits the task."
        )

    @mcp.prompt(
        name="compare_apps",
        description="Side-by-side comparison of 2-5 AI apps from HyperStore.",
    )
    def compare_apps(slugs: str) -> str:
        return (
            f"Compare these HyperStore apps: {slugs} (comma-separated slugs).\n\n"
            "1. For each slug, call `get_app` to fetch full details.\n"
            "2. Build a comparison table with rows: Pricing, Open source, Has API, Categories, "
            "Rating, Key features (top 3), Best for.\n"
            "3. End with a one-paragraph recommendation: which app suits which user."
        )

    @mcp.prompt(
        name="discover_category",
        description="Discover top AI tools in a given HyperStore category.",
    )
    def discover_category(category: str) -> str:
        return (
            f"The user wants to explore the \"{category}\" category on HyperStore.\n\n"
            "1. Call `list_categories` to find the matching slug if you're not sure.\n"
            "2. Call `category_apps` with that slug, limit=10.\n"
            "3. For the top 3, call `get_app` for richer detail.\n"
            "4. Summarize the landscape: how many apps total, common pricing models, and "
            "the standout picks with one-line descriptions."
        )

    return [find_tool_for_task, compare_apps, discover_category]
