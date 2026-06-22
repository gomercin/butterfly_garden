from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any, Iterable

from butterfly_graph.models import AnalysisArtifact, ImportBatch, MessageRecord, NormalizedDocument, RawSourceArtifact

SCHEMA_PATH = Path(__file__).resolve().parents[2] / "docs" / "schema.sql"


def dumps(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


class SQLiteStore:
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

    def connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def init_db(self) -> None:
        with self.connect() as conn:
            conn.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))

    def upsert_import_batch(self, batch: ImportBatch) -> None:
        sql = "INSERT OR REPLACE INTO import_batches (id, source_system, source_group, imported_at, parser_version, metadata_json) VALUES (?, ?, ?, ?, ?, ?)"
        with self.connect() as conn:
            conn.execute(sql, (batch.id, batch.source_system.value, batch.source_group, batch.imported_at, batch.parser_version, dumps(batch.metadata)))

    def upsert_raw_artifact(self, artifact: RawSourceArtifact) -> None:
        sql = "INSERT OR REPLACE INTO raw_artifacts (id, import_batch_id, source_system, source_group, raw_file_path, raw_sha256, size_bytes, metadata_json) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
        with self.connect() as conn:
            conn.execute(sql, (artifact.id, artifact.import_batch_id, artifact.source_system.value, artifact.source_group, artifact.raw_file_path, artifact.raw_sha256, artifact.size_bytes, dumps(artifact.metadata)))

    def upsert_documents(self, documents: Iterable[NormalizedDocument]) -> None:
        sql = "INSERT OR REPLACE INTO documents (id, source_system, source_group, source_original_id, title, document_type, created_at, updated_at, imported_at, language, raw_artifact_id, raw_sha256, normalized_sha256, content_text, metadata_json) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        rows = [(d.id, d.source_system.value, d.source_group, d.source_original_id, d.title, d.document_type.value, d.created_at, d.updated_at, d.imported_at, d.language, d.raw_artifact_id, d.raw_sha256, d.normalized_sha256, d.content_text, dumps(d.metadata)) for d in documents]
        with self.connect() as conn:
            conn.executemany(sql, rows)

    def upsert_messages(self, messages: Iterable[MessageRecord]) -> None:
        sql = "INSERT OR REPLACE INTO messages (id, document_id, source_original_id, parent_message_id, role, created_at, message_index, content_text, content_sha256, metadata_json) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        rows = [(m.id, m.document_id, m.source_original_id, m.parent_message_id, m.role.value, m.created_at, m.message_index, m.content_text, m.content_sha256, dumps(m.metadata)) for m in messages]
        with self.connect() as conn:
            conn.executemany(sql, rows)

    def insert_analysis(self, analysis: AnalysisArtifact) -> None:
        sql = "INSERT OR REPLACE INTO analyses (id, target_id, target_type, analysis_type, analyzer_name, analyzer_version, prompt_version, model_name, input_sha256, output_json, confidence, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        with self.connect() as conn:
            conn.execute(sql, (analysis.id, analysis.target_id, analysis.target_type, analysis.analysis_type, analysis.analyzer_name, analysis.analyzer_version, analysis.prompt_version, analysis.model_name, analysis.input_sha256, dumps(analysis.output), analysis.confidence, analysis.created_at))

    def list_documents(self, limit: int | None = None) -> list[sqlite3.Row]:
        query = "SELECT * FROM documents ORDER BY COALESCE(created_at, imported_at) DESC"
        params: tuple[Any, ...] = ()
        if limit is not None:
            query += " LIMIT ?"
            params = (limit,)
        with self.connect() as conn:
            return list(conn.execute(query, params))

    def list_messages_for_document(self, document_id: str) -> list[sqlite3.Row]:
        with self.connect() as conn:
            return list(conn.execute("SELECT * FROM messages WHERE document_id = ? ORDER BY message_index", (document_id,)))

    def list_analyses(self, analysis_type: str | None = None) -> list[sqlite3.Row]:
        query = "SELECT * FROM analyses"
        params: tuple[Any, ...] = ()
        if analysis_type:
            query += " WHERE analysis_type = ?"
            params = (analysis_type,)
        query += " ORDER BY created_at DESC"
        with self.connect() as conn:
            return list(conn.execute(query, params))
