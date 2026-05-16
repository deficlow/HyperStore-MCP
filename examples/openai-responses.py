"""Use HyperStore from the OpenAI Responses API as a remote MCP tool."""

from openai import OpenAI

client = OpenAI()

response = client.responses.create(
    model="gpt-4.1",
    tools=[
        {
            "type": "mcp",
            "server_label": "hyperstore",
            "server_url": "https://mcp.store.hypergpt.ai/mcp",
            "require_approval": "never",
        }
    ],
    input="Find me 3 free AI tools that help with writing unit tests in Python.",
)

print(response.output_text)
