from __future__ import annotations

import re
import unicodedata


def clean_text(value: str | None) -> str:
    if not value:
        return ""
    value = value.replace("\r\n", "\n").replace("\r", "\n")
    value = re.sub(r"\n{4,}", "\n\n\n", value)
    return value.strip()


def slugify(value: str, max_length: int = 90) -> str:
    value = unicodedata.normalize("NFKD", value)
    value = value.encode("ascii", "ignore").decode("ascii")
    value = re.sub(r"[^a-zA-Z0-9\-_\s]", "", value)
    value = re.sub(r"\s+", "-", value.strip().lower())
    value = re.sub(r"-+", "-", value)
    return (value[:max_length].strip("-") or "untitled")
