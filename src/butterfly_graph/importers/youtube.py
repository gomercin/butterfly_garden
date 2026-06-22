from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from bs4 import BeautifulSoup

from butterfly_graph.constants import PARSER_VERSION
from butterfly_graph.hashing import canonical_json_hash, sha256_file
from butterfly_graph.models import (
    DocumentType,
    ImportBatch,
    ImportResult,
    NormalizedDocument,
    RawSourceArtifact,
    SourceSystem,
)
from butterfly_graph.text import clean_text
from butterfly_graph.timeutils import utc_now_iso


class YouTubeTakeoutImporter:
    source_system_name = SourceSystem.YOUTUBE.value

    def import_source(self, source_path: Path, source_group: str | None = None) -> ImportResult:
        imported_at = utc_now_iso()
        raw_hash = sha256_file(source_path)
        batch = ImportBatch(
            source_system=SourceSystem.YOUTUBE,
            source_group=source_group or "youtube_history",
            imported_at=imported_at,
            parser_version=PARSER_VERSION,
            metadata={"source_path": str(source_path)},
        )
        raw = RawSourceArtifact(
            import_batch_id=batch.id,
            source_system=SourceSystem.YOUTUBE,
            source_group=batch.source_group,
            raw_file_path=str(source_path),
            raw_sha256=raw_hash,
            size_bytes=source_path.stat().st_size,
        )
        docs = []
        warnings = []
        if source_path.suffix.lower() == ".json":
            data: Any = json.loads(source_path.read_text(encoding="utf-8"))
            if isinstance(data, list):
                for i, item in enumerate(data):
                    title = clean_text(str(item.get("title") or f"YouTube event {i+1}"))
                    body = clean_text(json.dumps(item, ensure_ascii=False, indent=2))
                    docs.append(
                        NormalizedDocument(
                            source_system=SourceSystem.YOUTUBE,
                            source_group=batch.source_group,
                            source_original_id=str(item.get("titleUrl") or item.get("time") or i),
                            title=title,
                            document_type=DocumentType.VIDEO_HISTORY_EVENT,
                            created_at=item.get("time"),
                            imported_at=imported_at,
                            raw_artifact_id=raw.id,
                            raw_sha256=raw_hash,
                            normalized_sha256=canonical_json_hash(item),
                            content_text=body,
                            metadata=item,
                        )
                    )
        elif source_path.suffix.lower() in {".html", ".htm"}:
            text = BeautifulSoup(source_path.read_text(encoding="utf-8"), "html.parser").get_text("\n")
            docs.append(
                NormalizedDocument(
                    source_system=SourceSystem.YOUTUBE,
                    source_group=batch.source_group,
                    source_original_id=source_path.name,
                    title=f"YouTube Takeout HTML: {source_path.name}",
                    document_type=DocumentType.VIDEO_HISTORY_EVENT,
                    imported_at=imported_at,
                    raw_artifact_id=raw.id,
                    raw_sha256=raw_hash,
                    normalized_sha256=canonical_json_hash({"text": text}),
                    content_text=clean_text(text),
                    metadata={"placeholder": True},
                )
            )
            warnings.append("HTML YouTube import is a placeholder. Prefer JSON if available.")
        else:
            warnings.append(f"Unsupported YouTube file extension: {source_path.suffix}")
        return ImportResult(batch=batch, raw_artifact=raw, documents=docs, warnings=warnings)
