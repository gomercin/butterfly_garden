PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS import_batches (
    id TEXT PRIMARY KEY,
    source_system TEXT NOT NULL,
    source_group TEXT,
    imported_at TEXT NOT NULL,
    parser_version TEXT NOT NULL,
    metadata_json TEXT NOT NULL DEFAULT '{}'
);

CREATE TABLE IF NOT EXISTS raw_artifacts (
    id TEXT PRIMARY KEY,
    import_batch_id TEXT NOT NULL,
    source_system TEXT NOT NULL,
    source_group TEXT,
    raw_file_path TEXT NOT NULL,
    raw_sha256 TEXT NOT NULL,
    size_bytes INTEGER,
    metadata_json TEXT NOT NULL DEFAULT '{}',
    FOREIGN KEY(import_batch_id) REFERENCES import_batches(id)
);

CREATE TABLE IF NOT EXISTS documents (
    id TEXT PRIMARY KEY,
    source_system TEXT NOT NULL,
    source_group TEXT,
    source_original_id TEXT,
    title TEXT NOT NULL,
    document_type TEXT NOT NULL,
    created_at TEXT,
    updated_at TEXT,
    imported_at TEXT NOT NULL,
    language TEXT,
    raw_artifact_id TEXT,
    raw_sha256 TEXT,
    normalized_sha256 TEXT NOT NULL,
    content_text TEXT NOT NULL,
    metadata_json TEXT NOT NULL DEFAULT '{}',
    FOREIGN KEY(raw_artifact_id) REFERENCES raw_artifacts(id)
);

CREATE TABLE IF NOT EXISTS messages (
    id TEXT PRIMARY KEY,
    document_id TEXT NOT NULL,
    source_original_id TEXT,
    parent_message_id TEXT,
    role TEXT NOT NULL,
    created_at TEXT,
    message_index INTEGER NOT NULL,
    content_text TEXT NOT NULL,
    content_sha256 TEXT NOT NULL,
    metadata_json TEXT NOT NULL DEFAULT '{}',
    FOREIGN KEY(document_id) REFERENCES documents(id)
);

CREATE TABLE IF NOT EXISTS analyses (
    id TEXT PRIMARY KEY,
    target_id TEXT NOT NULL,
    target_type TEXT NOT NULL,
    analysis_type TEXT NOT NULL,
    analyzer_name TEXT NOT NULL,
    analyzer_version TEXT NOT NULL,
    prompt_version TEXT,
    model_name TEXT,
    input_sha256 TEXT NOT NULL,
    output_json TEXT NOT NULL,
    confidence REAL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS concepts (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    summary TEXT,
    first_seen_at TEXT,
    last_seen_at TEXT,
    source_count INTEGER NOT NULL DEFAULT 0,
    strength REAL,
    novelty TEXT,
    human_excitement TEXT,
    status TEXT,
    metadata_json TEXT NOT NULL DEFAULT '{}'
);

CREATE TABLE IF NOT EXISTS relations (
    id TEXT PRIMARY KEY,
    source_id TEXT NOT NULL,
    source_type TEXT NOT NULL,
    target_id TEXT NOT NULL,
    target_type TEXT NOT NULL,
    relation_type TEXT NOT NULL,
    strength REAL,
    evidence_json TEXT NOT NULL DEFAULT '[]',
    generated_by TEXT,
    status TEXT NOT NULL DEFAULT 'unreviewed',
    created_at TEXT NOT NULL,
    metadata_json TEXT NOT NULL DEFAULT '{}'
);

CREATE TABLE IF NOT EXISTS timeline_events (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    event_date TEXT,
    date_precision TEXT NOT NULL,
    life_period TEXT,
    age_estimate TEXT,
    source_id TEXT,
    source_type TEXT,
    themes_json TEXT NOT NULL DEFAULT '[]',
    confidence REAL,
    summary TEXT,
    metadata_json TEXT NOT NULL DEFAULT '{}'
);

CREATE TABLE IF NOT EXISTS human_overrides (
    id TEXT PRIMARY KEY,
    target_id TEXT NOT NULL,
    target_type TEXT NOT NULL,
    field_name TEXT NOT NULL,
    value_json TEXT NOT NULL,
    reason TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
