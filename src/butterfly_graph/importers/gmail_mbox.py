from __future__ import annotations

import email
import mailbox
from email.message import Message
from pathlib import Path

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


def _body(msg: Message) -> str:
    if msg.is_multipart():
        parts = []
        for part in msg.walk():
            if part.get_content_type() == "text/plain" and "attachment" not in str(part.get("Content-Disposition") or "").lower():
                payload = part.get_payload(decode=True)
                if payload:
                    parts.append(payload.decode(part.get_content_charset() or "utf-8", errors="replace"))
        return clean_text("\n\n".join(parts))
    payload = msg.get_payload(decode=True)
    return clean_text(payload.decode(msg.get_content_charset() or "utf-8", errors="replace")) if payload else ""


class GmailMboxImporter:
    source_system_name = SourceSystem.GMAIL.value

    def import_source(self, source_path: Path, source_group: str | None = None) -> ImportResult:
        imported_at = utc_now_iso()
        raw_hash = sha256_file(source_path)
        batch = ImportBatch(
            source_system=SourceSystem.GMAIL,
            source_group=source_group or "gmail_label",
            imported_at=imported_at,
            parser_version=PARSER_VERSION,
            metadata={"source_path": str(source_path)},
        )
        raw = RawSourceArtifact(
            import_batch_id=batch.id,
            source_system=SourceSystem.GMAIL,
            source_group=batch.source_group,
            raw_file_path=str(source_path),
            raw_sha256=raw_hash,
            size_bytes=source_path.stat().st_size,
        )
        docs = []
        for i, msg in enumerate(mailbox.mbox(source_path)):
            subject = clean_text(str(email.header.make_header(email.header.decode_header(msg.get("Subject", "")))))
            body = _body(msg)
            original_id = msg.get("Message-ID") or f"mbox-message-{i}"
            metadata = {"from": msg.get("From"), "to": msg.get("To"), "date": msg.get("Date"), "subject": subject}
            payload = {"source": "gmail", "id": original_id, "title": subject, "body": body, "metadata": metadata}
            docs.append(
                NormalizedDocument(
                    source_system=SourceSystem.GMAIL,
                    source_group=batch.source_group,
                    source_original_id=original_id,
                    title=subject or f"Untitled email {i+1}",
                    document_type=DocumentType.EMAIL,
                    created_at=msg.get("Date"),
                    imported_at=imported_at,
                    raw_artifact_id=raw.id,
                    raw_sha256=raw_hash,
                    normalized_sha256=canonical_json_hash(payload),
                    content_text=body,
                    metadata=metadata,
                )
            )
        return ImportResult(batch=batch, raw_artifact=raw, documents=docs)
