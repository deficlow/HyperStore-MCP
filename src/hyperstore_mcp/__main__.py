"""CLI entry point — `hyperstore-mcp` or `python -m hyperstore_mcp`."""

from __future__ import annotations

import argparse
import logging
import sys

from . import __version__
from .config import get_settings
from .server import build_server


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="hyperstore-mcp",
        description="MCP server for HyperStore (https://store.hypergpt.ai).",
    )
    p.add_argument(
        "--transport",
        choices=["stdio", "http", "sse"],
        default="stdio",
        help="Transport to run (default: stdio).",
    )
    p.add_argument("--host", default=None, help="Bind host for http/sse (overrides MCP_HOST).")
    p.add_argument("--port", type=int, default=None, help="Bind port for http/sse (overrides MCP_PORT).")
    p.add_argument("--version", action="version", version=f"hyperstore-mcp {__version__}")
    return p


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    settings = get_settings()

    if args.host:
        settings.host = args.host
    if args.port:
        settings.port = args.port

    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper(), logging.INFO),
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    mcp = build_server(settings)

    if args.transport == "stdio":
        mcp.run(transport="stdio")
    elif args.transport == "http":
        # FastMCP's "streamable-http" transport (modern remote MCP).
        mcp.settings.host = settings.host
        mcp.settings.port = settings.port
        mcp.run(transport="streamable-http")
    elif args.transport == "sse":
        # Legacy SSE transport — kept for older remote MCP clients.
        mcp.settings.host = settings.host
        mcp.settings.port = settings.port
        mcp.run(transport="sse")
    else:
        print(f"Unknown transport: {args.transport}", file=sys.stderr)
        return 2

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
