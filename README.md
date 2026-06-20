# HyperStore MCP

<!-- mcp-name: io.github.deficlow/hyperstore-mcp -->

> Plug 6,500+ AI apps into any LLM via the [Model Context Protocol](https://modelcontextprotocol.io).

[![PyPI](https://img.shields.io/pypi/v/hyperstore-mcp.svg?label=pypi&color=3776AB)](https://pypi.org/project/hyperstore-mcp/)
[![Glama](https://glama.ai/mcp/servers/deficlow/HyperStore-MCP/badges/score.svg)](https://glama.ai/mcp/servers/deficlow/HyperStore-MCP)
[![Smithery](https://smithery.ai/badge/@deficlow/hyperstore)](https://smithery.ai/server/deficlow/hyperstore)
[![MCP Registry](https://img.shields.io/badge/MCP%20Registry-listed-2D9CDB)](https://registry.modelcontextprotocol.io/v0/servers?search=io.github.deficlow/hyperstore-mcp)
[![CI](https://github.com/deficlow/HyperStore-MCP/actions/workflows/ci.yml/badge.svg)](https://github.com/deficlow/HyperStore-MCP/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**HyperStore** is a curated directory of 6,500+ AI applications, developed by [HyperGPT](https://hypergpt.ai).
This MCP server exposes the [HyperStore](https://store.hypergpt.ai) catalog to any LLM client — Claude, ChatGPT, Cursor,
Windsurf, Cline, Zed, Gemini, and anything else that speaks MCP.

Ask your LLM:

> *"Find me a free AI tool that summarises PDFs."*
> *"Compare ChatGPT, Claude, and Gemini side-by-side."*
> *"Show me the top 5 image-generation apps with an API."*

The LLM calls HyperStore MCP behind the scenes and answers with up-to-date, curated results.

---

## What you get

**13 tools:**

| Tool | Purpose |
|---|---|
| `search_apps` | Full-text keyword search |
| `ai_search` | Embedding-based semantic search |
| `get_app` | Full app detail (features, screenshots, pricing) |
| `list_apps` | Paginated apps with filters (category, pricing) |
| `list_categories` | Browse all 30+ categories |
| `category_apps` | Apps within a category |
| `browse_apps` | A-Z directory listing |
| `get_homepage` | Trending + top categories overview |
| `get_alternatives` | Curated alternatives to an app |
| `list_audiences` | Audience segments (developers, lawyers, …) |
| `apps_for_audience` | Best AI tools for an audience |
| `list_use_cases` | Use-case taxonomies (legal-contracts, …) |
| `apps_for_use_case` | AI tools for a use case |

**3 resources:**

- `hyperstore://app/{slug}` — markdown rendering of any app
- `hyperstore://category/{slug}` — top apps in a category
- `hyperstore://catalog` — full category index

**3 prompts:**

- `find_tool_for_task` — guided discovery for a task
- `compare_apps` — side-by-side app comparison
- `discover_category` — explore a topic

---

## Install

### Option A — `uvx` (zero install, recommended)

Requires [uv](https://docs.astral.sh/uv/). One command and you're done:

```bash
uvx hyperstore-mcp
```

### Option B — `pipx`

```bash
pipx install hyperstore-mcp
hyperstore-mcp
```

### Option C — Docker (for remote hosting)

```bash
docker run --rm -p 8080:8080 ghcr.io/deficlow/hyperstore-mcp
# Now MCP Streamable HTTP at http://localhost:8080/mcp
```

### Option D — Hosted endpoint (no install)

Use our managed Streamable HTTP server:

```
https://mcp.store.hypergpt.ai/mcp
```

---

## Connect from your LLM client

### Claude Desktop

Edit `~/Library/Application Support/Claude/claude_desktop_config.json`
(macOS) or `%APPDATA%\Claude\claude_desktop_config.json` (Windows):

```json
{
  "mcpServers": {
    "hyperstore": {
      "command": "uvx",
      "args": ["hyperstore-mcp"]
    }
  }
}
```

Restart Claude → tools appear in the 🛠 menu.

### Claude Code

```bash
claude mcp add hyperstore -- uvx hyperstore-mcp
```

### Cursor

`.cursor/mcp.json` (project) or `~/.cursor/mcp.json` (global):

```json
{
  "mcpServers": {
    "hyperstore": {
      "command": "uvx",
      "args": ["hyperstore-mcp"]
    }
  }
}
```

### Windsurf

`~/.codeium/windsurf/mcp_config.json`:

```json
{
  "mcpServers": {
    "hyperstore": {
      "command": "uvx",
      "args": ["hyperstore-mcp"]
    }
  }
}
```

### Cline (VS Code)

`settings.json`:

```json
{
  "cline.mcpServers": {
    "hyperstore": {
      "command": "uvx",
      "args": ["hyperstore-mcp"]
    }
  }
}
```

### Zed

`~/.config/zed/settings.json`:

```json
{
  "context_servers": {
    "hyperstore": {
      "command": {
        "path": "uvx",
        "args": ["hyperstore-mcp"]
      }
    }
  }
}
```

### Gemini CLI

`~/.gemini/settings.json`:

```json
{
  "mcpServers": {
    "hyperstore": {
      "command": "uvx",
      "args": ["hyperstore-mcp"]
    }
  }
}
```

### ChatGPT (Pro / Team / Enterprise)

**Settings → Connectors → Add custom connector**:

- **Name**: HyperStore
- **MCP Server URL**: `https://mcp.store.hypergpt.ai/mcp`
- **Authentication**: None

### OpenAI Responses API

```python
from openai import OpenAI

client = OpenAI()
response = client.responses.create(
    model="gpt-4.1",
    tools=[{
        "type": "mcp",
        "server_label": "hyperstore",
        "server_url": "https://mcp.store.hypergpt.ai/mcp",
        "require_approval": "never",
    }],
    input="Find me 3 free AI tools for writing unit tests.",
)
print(response.output_text)
```

### Anthropic Messages API

```python
from anthropic import Anthropic

client = Anthropic()
response = client.messages.create(
    model="claude-opus-4-7",
    max_tokens=1024,
    mcp_servers=[{
        "type": "url",
        "url": "https://mcp.store.hypergpt.ai/mcp",
        "name": "hyperstore",
    }],
    messages=[{"role": "user", "content": "Top 5 AI image generators?"}],
)
```

See [`examples/`](examples/) for ready-to-paste configs for every supported client.

---

## Self-hosting

For self-hosting, use the [Docker image](#option-c--docker-for-remote-hosting).
For direct invocation without Docker, the CLI accepts `--transport http|sse`
(see `hyperstore-mcp --help`).

---

## Configuration

When self-hosting, these environment variables can be set
(see [`.env.example`](.env.example) for the full list):

| Variable | Default | Purpose |
|---|---|---|
| `MCP_HOST` | `0.0.0.0` | Bind host (http/sse transports) |
| `MCP_PORT` | `8080` | Bind port (http/sse transports) |
| `LOG_LEVEL` | `INFO` | Logging level (`DEBUG`, `INFO`, `WARNING`, `ERROR`) |

---

## Development

```bash
git clone https://github.com/deficlow/HyperStore-MCP
cd HyperStore-MCP
uv sync --all-extras
uv run pytest
uv run hyperstore-mcp        # stdio mode for local testing
```

Inspect the running server with the official **MCP Inspector**:

```bash
npx @modelcontextprotocol/inspector uvx hyperstore-mcp
```

---

## How it works

HyperStore MCP is a thin async wrapper around the [HyperStore](https://store.hypergpt.ai) public
REST API. It is **read-only** — no credentials, no writes, no PII. The same data that
powers the website powers the MCP server. Updates land in your LLM the moment they
land on the site.

```
LLM client ──MCP──▶ hyperstore-mcp ──HTTPS──▶ store.hypergpt.ai/api
```

---

## License

MIT © [HyperGPT](https://hypergpt.ai)
