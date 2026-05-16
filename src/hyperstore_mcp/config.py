from __future__ import annotations

from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from . import __version__


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    api_base: str = Field(
        default="https://store.hypergpt.ai",
        alias="HYPERSTORE_API_BASE",
    )
    timeout: float = Field(default=20.0, alias="HYPERSTORE_TIMEOUT")
    user_agent: str = Field(
        default=f"hyperstore-mcp/{__version__}",
        alias="HYPERSTORE_USER_AGENT",
    )

    host: str = Field(default="0.0.0.0", validation_alias=AliasChoices("MCP_HOST", "HOST"))
    # PORT is the Railway/Heroku/Cloud Run convention; MCP_PORT is the explicit override.
    port: int = Field(default=8080, validation_alias=AliasChoices("MCP_PORT", "PORT"))
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")

    @property
    def api_base_clean(self) -> str:
        return self.api_base.rstrip("/")


def get_settings() -> Settings:
    return Settings()
