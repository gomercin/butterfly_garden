from __future__ import annotations

import os
from pathlib import Path

from pydantic import BaseModel

from butterfly_graph.constants import DEFAULT_DB_PATH, DEFAULT_VAULT_PATH


class Settings(BaseModel):
    db_path: Path = Path(os.getenv("BUTTERFLY_DB_PATH", DEFAULT_DB_PATH))
    vault_path: Path = Path(os.getenv("BUTTERFLY_VAULT_PATH", DEFAULT_VAULT_PATH))
    ollama_url: str = os.getenv("BUTTERFLY_OLLAMA_URL", "http://localhost:11434")
    ollama_model: str = os.getenv("BUTTERFLY_OLLAMA_MODEL", "llama3.1")


def get_settings() -> Settings:
    return Settings()
