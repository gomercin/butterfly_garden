from __future__ import annotations

import xml.etree.ElementTree as ET
from pathlib import Path

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

CONTENT_NS = "{http://purl.org/rss/1.0/modules/content/}"
WP_NS = "{http://wordpress.org/export/1.2/}"


def _text(node: ET.Element, name: str) -> str | None:
    found = node.find(name)
    return clean_text(found.text) if found is not None and found.text else None


class WordPressWxrImporter:
    source_system_name = SourceSystem.WORDPRESS.value

    def import_source(self, source_path: Path, source_group: str | None = None) -> ImportResult:
        imported_at = utc_now_iso()
        raw_hash = sha256_file(source_path)
        batch = ImportBatch(
            source_system=SourceSystem.WORDPRESS,
            source_group=source_group or "wordpress_blog",
            imported_at=imported_at,
            parser_version=PARSER_VERSION,
            metadata={"source_path": str(source_path)},
        )
        raw = RawSourceArtifact(
            import_batch_id=batch.id,
            source_system=SourceSystem.WORDPRESS,
            source_group=batch.source_group,
            raw_file_path=str(source_path),
            raw_sha256=raw_hash,
            size_bytes=source_path.stat().st_size,
        )
        tree = ET.parse(source_path)
        channel = tree.getroot().find("channel")
        docs = []
        for i, item in enumerate(channel.findall("item") if channel is not None else []):
            title = _text(item, "title") or f"Untitled WordPress item {i+1}"
            post_id = _text(item, f"{WP_NS}post_id") or _text(item, "guid") or f"wp-item-{i}"
            post_type = _text(item, f"{WP_NS}post_type") or "post"
            html = _text(item, f"{CONTENT_NS}encoded") or ""
            content = clean_text(BeautifulSoup(html, "html.parser").get_text("\n"))
            metadata = {
                "post_type": post_type,
                "status": _text(item, f"{WP_NS}status"),
                "link": _text(item, "link"),
                "pub_date": _text(item, "pubDate"),
            }
            payload = {"source": "wordpress", "id": post_id, "title": title, "content": content, "metadata": metadata}
            docs.append(
                NormalizedDocument(
                    source_system=SourceSystem.WORDPRESS,
                    source_group=batch.source_group,
                    source_original_id=post_id,
                    title=title,
                    document_type=DocumentType.BLOG_POST if post_type == "post" else DocumentType.PAGE,
                    created_at=_text(item, f"{WP_NS}post_date_gmt") or _text(item, "pubDate"),
                    imported_at=imported_at,
                    raw_artifact_id=raw.id,
                    raw_sha256=raw_hash,
                    normalized_sha256=canonical_json_hash(payload),
                    content_text=content,
                    metadata=metadata,
                )
            )
        return ImportResult(batch=batch, raw_artifact=raw, documents=docs)
