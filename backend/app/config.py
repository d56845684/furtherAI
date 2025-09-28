from functools import lru_cache
from typing import List, Optional, Union

from pydantic import BaseSettings, Field, validator


class Settings(BaseSettings):
    app_name: str = Field("SQL Agent Service", env="APP_NAME")
    environment: str = Field("development", env="ENVIRONMENT")
    api_prefix: str = Field("/api", env="API_PREFIX")
    database_url: str = Field(..., env="DATABASE_URL")
    openai_api_key: Optional[str] = Field(default=None, env="OPENAI_API_KEY")
    openai_model: str = Field("gpt-4o-mini", env="OPENAI_MODEL")
    max_reasoning_steps: int = Field(5, env="MAX_REASONING_STEPS")
    allow_mcp: bool = Field(True, env="ALLOW_MCP")
    allow_tool_calling: bool = Field(True, env="ALLOW_TOOL_CALLING")
    allowed_origins: List[str] = Field(default_factory=lambda: ["*"], env="ALLOWED_ORIGINS")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

    @validator("allowed_origins", pre=True)
    def split_origins(cls, value: Union[str, List[str]]) -> List[str]:
        if isinstance(value, list):
            return value
        if isinstance(value, str):
            # Handle empty string or None
            if not value or value.strip() == "":
                return ["*"]
            # Split by comma and strip whitespace
            origins = [origin.strip() for origin in value.split(",") if origin.strip()]
            return origins if origins else ["*"]
        return ["*"]


@lru_cache
def get_settings() -> Settings:
    return Settings()
