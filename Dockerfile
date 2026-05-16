FROM python:3.12-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN pip install --no-cache-dir uv

COPY pyproject.toml README.md LICENSE ./
COPY src ./src
RUN uv pip install --system --no-cache ".[http]"

# ── Runtime ────────────────────────────────────────────────────────────────────
FROM python:3.12-slim AS runtime

LABEL io.modelcontextprotocol.server.name="io.github.deficlow/hyperstore-mcp"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    MCP_HOST=0.0.0.0 \
    MCP_PORT=8080

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin/hyperstore-mcp /usr/local/bin/hyperstore-mcp

RUN useradd -u 10001 -m mcp
USER mcp

EXPOSE 8080

CMD ["hyperstore-mcp", "--transport", "http"]
