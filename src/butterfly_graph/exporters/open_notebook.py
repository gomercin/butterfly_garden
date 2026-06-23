from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from butterfly_graph.storage import SQLiteStore
from butterfly_graph.text import clean_text, slugify


def _frontmatter(data: dict[str, Any]) -> str:
    lines = ["---"]
    for key, value in data.items():
        if value is None:
            lines.append(f'{key}: ""')
        elif isinstance(value, (int, float)):
            lines.append(f"{key}: {value}")
        else:
            escaped = str(value).replace('"', '\\"')
            lines.append(f'{key}: "{escaped}"')
    lines.append("---")
    return "\n".join(lines)


class OpenNotebookBundleExporter:
    """Export a portable source bundle for Open Notebook-style RAG experiments.

    This is intentionally not a direct Open Notebook API integration. The goal is to keep
    Butterfly Graph's canonical store independent while producing a clean folder of Markdown
    documents and a manifest that can be imported, uploaded, or adapted later.
    """

    def __init__(self, store: SQLiteStore, output_path: Path):
        self.store = store
        self.output_path = output_path

    def export_all(self) -> None:
        self.output_path.mkdir(parents=True, exist_ok=True)
        documents_path = self.output_path / "documents"
        documents_path.mkdir(parents=True, exist_ok=True)

        manifest: list[dict[str, Any]] = []
        for row in self.store.list_documents():
            title = row["title"]
            source_system = row["source_system"]
            source_original_id = row["source_original_id"] or row["id"]
            file_name = f"{source_system}-{slugify(source_original_id)}-{slugify(title)}.md"
            relative_path = Path("documents") / file_name
            output_file = self.output_path / relative_path

            metadata = {
                "butterfly_document_id": row["id"],
                "source_system": source_system,
                "source_group": row["source_group"],
                "source_original_id": row["source_original_id"],
                "document_type": row["document_type"],
                "created_at": row["created_at"],
                "updated_at": row["updated_at"],
                "normalized_sha256": row["normalized_sha256"],
            }
            body = f"{_frontmatter(metadata)}\n\n# {title}\n\n{clean_text(row['content_text'])}\n"
            output_file.write_text(body, encoding="utf-8")

            manifest.append(
                {
                    **metadata,
                    "title": title,
                    "path": str(relative_path),
                    "content_length": len(row["content_text"] or ""),
                }
            )

        (self.output_path / "manifest.json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        (self.output_path / "README.md").write_text(
            "# Open Notebook Import Bundle\n\n"
            "This folder contains Markdown documents exported from Butterfly Graph.\n\n"
            "Use this as a controlled subset for Open Notebook or similar local RAG tools.\n"
            "The canonical source of truth remains Butterfly Graph's SQLite database and raw exports.\n",
            encoding="utf-8",
        )
