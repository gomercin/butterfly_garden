from __future__ import annotations

import json
import tempfile
import zipfile
from pathlib import Path
from typing import Any

from butterfly_graph.constants import PARSER_VERSION
from butterfly_graph.hashing import canonical_json_hash, sha256_file, sha256_text
from butterfly_graph.models import (
    DocumentType,
    ImportBatch,
    ImportResult,
    MessageRecord,
    MessageRole,
    NormalizedDocument,
    RawSourceArtifact,
    SourceSystem,
    new_id,
)
from butterfly_graph.text import clean_text
from butterfly_graph.timeutils import from_unix_timestamp, utc_now_iso


def _message_text(message: dict[str, Any]) -> str:
    content = message.get("content") or {}
    parts = content.get("parts")
    if isinstance(parts, list):
        return clean_text("\n\n".join(str(p) for p in parts if p is not None))
    text = content.get("text")
    return clean_text(text if isinstance(text, str) else "")


def _message_role(message: dict[str, Any]) -> MessageRole:
    role = (message.get("author") or {}).get("role")
    return MessageRole(role) if role in {"user", "assistant", "system", "tool"} else MessageRole.UNKNOWN


def _load(source_path: Path) -> tuple[list[dict[str, Any]], Path]:
    if source_path.is_dir():
        p = source_path / "conversations.json"
        if not p.exists():
            raise FileNotFoundError(f"No conversations.json in {source_path}")
        return json.loads(p.read_text(encoding="utf-8")), p
    if zipfile.is_zipfile(source_path):
        tmp = Path(tempfile.mkdtemp(prefix="butterfly_chatgpt_"))
        with zipfile.ZipFile(source_path) as zf:
            names = [n for n in zf.namelist() if n.endswith("conversations.json")]
            if not names:
                raise FileNotFoundError("No conversations.json in zip")
            zf.extract(names[0], tmp)
            return json.loads((tmp / names[0]).read_text(encoding="utf-8")), source_path
    if source_path.name == "conversations.json":
        return json.loads(source_path.read_text(encoding="utf-8")), source_path
    raise ValueError(f"Unsupported ChatGPT export path: {source_path}")


class ChatGPTImporter:
    source_system_name = SourceSystem.CHATGPT.value

    def import_source(self, source_path: Path, source_group: str | None = None) -> ImportResult:
        imported_at = utc_now_iso()
        conversations, raw_ref = _load(source_path)
        batch = ImportBatch(
            source_system=SourceSystem.CHATGPT,
            source_group=source_group or "chatgpt_chats",
            imported_at=imported_at,
            parser_version=PARSER_VERSION,
            metadata={"source_path": str(source_path)},
        )
        raw_hash = sha256_file(raw_ref)
        raw = RawSourceArtifact(
            import_batch_id=batch.id,
            source_system=SourceSystem.CHATGPT,
            source_group=batch.source_group,
            raw_file_path=str(source_path),
            raw_sha256=raw_hash,
            size_bytes=source_path.stat().st_size if source_path.exists() else None,
        )
        docs: list[NormalizedDocument] = []
        messages: list[MessageRecord] = []
        warnings: list[str] = []

        for ci, conv in enumerate(conversations):
            conv_id = str(conv.get("id") or conv.get("conversation_id") or f"conversation-{ci}")
            title = clean_text(conv.get("title") or f"Untitled ChatGPT Conversation {ci + 1}")
            nodes = []
            for node_id, node in (conv.get("mapping") or {}).items():
                msg = (node or {}).get("message")
                if msg and _message_text(msg):
                    nodes.append((node_id, node))
            nodes.sort(key=lambda item: (float(((item[1].get("message") or {}).get("create_time")) or 0), item[0]))

            doc_id = new_id("doc")
            parts = []
            for i, (node_id, node) in enumerate(nodes):
                msg = node.get("message") or {}
                text = _message_text(msg)
                role = _message_role(msg)
                parts.append(f"## {role.value}\n\n{text}")
                messages.append(
                    MessageRecord(
                        document_id=doc_id,
                        source_original_id=str(msg.get("id") or node_id),
                        parent_message_id=str(node.get("parent")) if node.get("parent") else None,
                        role=role,
                        created_at=from_unix_timestamp(msg.get("create_time")),
                        message_index=i,
                        content_text=text,
                        content_sha256=sha256_text(text),
                        metadata={"chatgpt_node_id": node_id},
                    )
                )

            content_text = clean_text("\n\n".join(parts))
            payload = {
                "source_system": "chatgpt",
                "source_original_id": conv_id,
                "title": title,
                "content_text": content_text,
                "message_count": len(nodes),
            }
            docs.append(
                NormalizedDocument(
                    id=doc_id,
                    source_system=SourceSystem.CHATGPT,
                    source_group=batch.source_group,
                    source_original_id=conv_id,
                    title=title,
                    document_type=DocumentType.CONVERSATION,
                    created_at=from_unix_timestamp(conv.get("create_time")),
                    updated_at=from_unix_timestamp(conv.get("update_time")),
                    imported_at=imported_at,
                    raw_artifact_id=raw.id,
                    raw_sha256=raw_hash,
                    normalized_sha256=canonical_json_hash(payload),
                    content_text=content_text,
                    metadata={"message_count": len(nodes), "chatgpt_conversation_index": ci},
                )
            )
        if not docs:
            warnings.append("No conversations parsed.")
        return ImportResult(batch=batch, raw_artifact=raw, documents=docs, messages=messages, warnings=warnings)
