from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from butterfly_graph.storage import SQLiteStore
from butterfly_graph.text import clean_text, slugify


def _yaml_scalar(value: Any) -> str:
    if value is None:
        return '\"\"'
    if isinstance(value, (int, float)):
        return str(value)
    return '\"' + str(value).replace('\"', '\\\"') + '\"'


def _frontmatter(data: dict[str, Any]) -> str:
    lines = ["---"]
    for key, value in data.items():
        if isinstance(value, list):
            lines.append(f"{key}:")
            for item in value:
                lines.append(f"  - {_yaml_scalar(item)}")
        else:
            lines.append(f"{key}: {_yaml_scalar(value)}")
    lines.append("---")
    return "\n".join(lines)


class ObsidianExporter:
    def __init__(self, store: SQLiteStore, vault_path: Path):
        self.store = store
        self.vault_path = vault_path

    def export_all(self) -> None:
        self.export_conversations()
        self.export_dashboards()

    def export_conversations(self) -> None:
        out_dir = self.vault_path / "10 Conversations"
        out_dir.mkdir(parents=True, exist_ok=True)
        for doc in self.store.list_documents():
            title = doc["title"]
            metadata = json.loads(doc["metadata_json"] or "{}")
            fm = _frontmatter(
                {
                    "type": doc["document_type"],
                    "source_system": doc["source_system"],
                    "source_group": doc["source_group"],
                    "source_original_id": doc["source_original_id"],
                    "created_at": doc["created_at"],
                    "updated_at": doc["updated_at"],
                    "imported_at": doc["imported_at"],
                    "normalized_sha256": doc["normalized_sha256"],
                    "message_count": metadata.get("message_count"),
                    "human_excitement": "",
                    "curation_status": "unreviewed",
                }
            )
            messages = self.store.list_messages_for_document(doc["id"])
            if messages:
                transcript = "\n\n".join(
                    [
                        f"### {m['message_index']:03d} · {m['role']}\n\n{clean_text(m['content_text'])}"
                        for m in messages
                    ]
                )
            else:
                transcript = clean_text(doc["content_text"])
            content = "\n".join(
                [
                    fm,
                    "",
                    f"# {title}",
                    "",
                    "<!-- butterfly:generated:start summary-placeholder v1 -->",
                    "Summary not generated yet.",
                    "<!-- butterfly:generated:end summary-placeholder v1 -->",
                    "",
                    "## Human notes",
                    "",
                    "<!-- butterfly:human:start notes -->",
                    "",
                    "<!-- butterfly:human:end notes -->",
                    "",
                    "## Transcript / Source Text",
                    "",
                    "<!-- butterfly:generated:start transcript v1 -->",
                    "",
                    transcript,
                    "",
                    "<!-- butterfly:generated:end transcript v1 -->",
                    "",
                ]
            )
            (out_dir / f"{slugify(title)}.md").write_text(content, encoding="utf-8")

    def export_dashboards(self) -> None:
        out_dir = self.vault_path / "60 Butterflies"
        out_dir.mkdir(parents=True, exist_ok=True)
        rows = []
        for item in self.store.list_analyses("summary"):
            output = json.loads(item["output_json"])
            score = output.get("shiny_butterfly_score")
            if score is not None and float(score) >= 0.25:
                rows.append(
                    f"- score {score:.2f} · target `{item['target_id']}` · "
                    f"triggers: {output.get('activation_triggers', [])}"
                )
        dashboard = (
            "# Forgotten Butterflies\n\nGenerated dashboard.\n\n## Candidates\n\n"
            + ("\n".join(rows) if rows else "_No candidates yet. Run analysis first._")
            + "\n"
        )
        (out_dir / "Forgotten High Excitement Ideas.md").write_text(dashboard, encoding="utf-8")
        timeline_dir = self.vault_path / "50 Timeline"
        timeline_dir.mkdir(parents=True, exist_ok=True)
        (timeline_dir / "Personal Timeline.md").write_text(
            "# Personal Timeline\n\n_Seed timeline. Add events manually or run timeline extraction later._\n",
            encoding="utf-8",
        )
        echo_dir = self.vault_path / "40 Echoes"
        echo_dir.mkdir(parents=True, exist_ok=True)
        (echo_dir / "Echo Index.md").write_text(
            "# Echo Index\n\n_Recurring patterns across years will appear here._\n",
            encoding="utf-8",
        )
