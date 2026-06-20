"""Thin async wrapper around the HyperStore public REST API."""

from __future__ import annotations

from typing import Any

import httpx

from .config import Settings


class HyperStoreError(Exception):
    """Raised when the HyperStore API returns an error."""

    def __init__(self, status: int, message: str):
        self.status = status
        self.message = message
        super().__init__(f"HyperStore API {status}: {message}")


class HyperStoreClient:
    """Async client for the HyperStore public REST API.

    All methods correspond 1:1 to public endpoints under `/api`.
    Read-only — no auth required.
    """

    def __init__(self, settings: Settings, http: httpx.AsyncClient | None = None):
        self._settings = settings
        self._owns_client = http is None
        self._http = http or httpx.AsyncClient(
            base_url=f"{settings.api_base_clean}/api",
            timeout=settings.timeout,
            headers={
                "User-Agent": settings.user_agent,
                "Accept": "application/json",
            },
        )

    async def aclose(self) -> None:
        if self._owns_client:
            await self._http.aclose()

    async def __aenter__(self) -> HyperStoreClient:
        return self

    async def __aexit__(self, *exc: Any) -> None:
        await self.aclose()

    # ── internals ────────────────────────────────────────────────────────────
    async def _get(self, path: str, params: dict[str, Any] | None = None) -> Any:
        clean_params = {k: v for k, v in (params or {}).items() if v is not None}
        resp = await self._http.get(path, params=clean_params)
        return self._unwrap(resp)

    async def _post(self, path: str, json: dict[str, Any]) -> Any:
        resp = await self._http.post(path, json=json)
        return self._unwrap(resp)

    @staticmethod
    def _unwrap(resp: httpx.Response) -> Any:
        if resp.status_code >= 400:
            try:
                detail = resp.json().get("detail", resp.text)
            except Exception:
                detail = resp.text
            raise HyperStoreError(resp.status_code, str(detail))
        return resp.json()

    # ── public endpoints ─────────────────────────────────────────────────────
    async def homepage(self, page: int = 1) -> dict[str, Any]:
        return await self._get("/homepage", {"page": page})

    async def list_apps(
        self,
        *,
        query: str | None = None,
        pricing: str | None = None,
        category: str | None = None,
        cursor: int | None = None,
        limit: int = 24,
    ) -> dict[str, Any]:
        return await self._get(
            "/apps",
            {
                "q": query,
                "pricing": pricing,
                "category": category,
                "cursor": cursor,
                "limit": limit,
            },
        )

    async def get_app(self, slug: str) -> dict[str, Any]:
        return await self._get(f"/apps/{slug}")

    async def list_categories(self) -> list[dict[str, Any]]:
        return await self._get("/categories")

    async def category_apps(
        self,
        slug: str,
        *,
        pricing: str | None = None,
        cursor: int | None = None,
        limit: int = 24,
    ) -> dict[str, Any]:
        return await self._get(
            f"/categories/{slug}/apps",
            {"pricing": pricing, "cursor": cursor, "limit": limit},
        )

    async def ai_search(self, prompt: str) -> dict[str, Any]:
        return await self._post("/ai-search", {"prompt": prompt, "turnstile_token": ""})

    async def search(
        self,
        query: str,
        *,
        cursor: int | None = None,
        limit: int = 24,
    ) -> dict[str, Any]:
        return await self._get("/search", {"q": query, "cursor": cursor, "limit": limit})

    async def browse(
        self,
        letter: str,
        *,
        pricing: str | None = None,
        cursor: int | None = None,
        limit: int = 24,
    ) -> dict[str, Any]:
        return await self._get(
            "/browse",
            {"letter": letter, "pricing": pricing, "cursor": cursor, "limit": limit},
        )

    async def app_alternatives(self, slug: str, *, limit: int = 24) -> dict[str, Any]:
        return await self._get(f"/apps/{slug}/alternatives", {"limit": limit})

    async def list_audiences(self) -> list[dict[str, Any]]:
        return await self._get("/audiences")

    async def audience_apps(
        self,
        slug: str,
        *,
        cursor: int | None = None,
        limit: int = 24,
    ) -> dict[str, Any]:
        return await self._get(
            f"/audiences/{slug}/apps",
            {"cursor": cursor, "limit": limit},
        )

    async def list_use_cases(self) -> list[dict[str, Any]]:
        return await self._get("/use-cases")

    async def use_case_apps(
        self,
        slug: str,
        *,
        cursor: int | None = None,
        limit: int = 24,
    ) -> dict[str, Any]:
        return await self._get(
            f"/use-cases/{slug}/apps",
            {"cursor": cursor, "limit": limit},
        )
