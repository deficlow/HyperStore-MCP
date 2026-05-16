# ChatGPT / OpenAI — Remote MCP

HyperStore is hosted as a remote MCP server. Use it from any client that speaks the
Streamable HTTP transport.

## Endpoint

```
https://mcp.store.hypergpt.ai/mcp
```

## ChatGPT (Pro / Team / Enterprise — Connectors)

1. Open ChatGPT → **Settings → Connectors → Add custom connector**.
2. Set:
   - **Name**: HyperStore
   - **MCP Server URL**: `https://mcp.store.hypergpt.ai/mcp`
   - **Authentication**: None
3. Save. The connector exposes 8 tools (`search_apps`, `ai_search`, `get_app`, …).

## OpenAI Responses API

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

## Anthropic Messages API (remote MCP)

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
    messages=[{"role": "user", "content": "What are the top 5 AI image generators on HyperStore?"}],
)

print(response.content)
```
