from __future__ import annotations

from enum import StrEnum
from typing import Any, Literal
from uuid import uuid4

from pydantic import BaseModel, Field


def new_id(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex}"


class SourceSystem(StrEnum):
    CHATGPT = "chatgpt"
    GMAIL = "gmail"
    WORDPRESS = "wordpress"
    YOUTUBE = "youtube"
    MANUAL = "manual"
    UNKNOWN = "unknown"


class DocumentType(StrEnum):
    CONVERSATION = "conversation"
    EMAIL = "email"
    BLOG_POST = "blog_post"
    PAGE = "page"
    VIDEO_HISTORY_EVENT = "video_history_event"
    STORY = "story"
    UNKNOWN = "unknown"


class MessageRole(StrEnum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
    TOOL = "tool"
    EMAIL = "email"
    UNKNOWN = "unknown"


class DatePrecision(StrEnum):
    EXACT = "exact"
    MONTH = "month"
    YEAR = "year"
    APPROXIMATE = "approximate"
    UNKNOWN = "unknown"


class RelationType(StrEnum):
    MENTIONS = "mentions"
    INSPIRED_BY = "inspired_by"
    EVOLVES_INTO = "evolves_into"
    ECHOES = "echoes"
    SAME_PATTERN_AS = "same_pattern_as"
    POSSIBLE_PROJECT = "possible_project"
    CHILDHOOD_ECHO = "childhood_echo"
    RELATED_TO = "related_to"


class ReviewStatus(StrEnum):
    UNREVIEWED = "unreviewed"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    REWRITTEN = "rewritten"


class Excitement(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    UNKNOWN = "unknown"


class ImportBatch(BaseModel):
    id: str = Field(default_factory=lambda: new_id("batch"))
    source_system: SourceSystem
    source_group: str | None = None
    imported_at: str
    parser_version: str
    metadata: dict[str, Any] = Field(default_factory=dict)


class RawSourceArtifact(BaseModel):
    id: str = Field(default_factory=lambda: new_id("raw"))
    import_batch_id: str
    source_system: SourceSystem
    source_group: str | None = None
    raw_file_path: str
    raw_sha256: str
    size_bytes: int | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class NormalizedDocument(BaseModel):
    id: str = Field(default_factory=lambda: new_id("doc"))
    source_system: SourceSystem
    source_group: str | None = None
    source_original_id: str | None = None
    title: str
    document_type: DocumentType
    created_at: str | None = None
    updated_at: str | None = None
    imported_at: str
    language: str | None = None
    raw_artifact_id: str | None = None
    raw_sha256: str | None = None
    normalized_sha256: str
    content_text: str
    metadata: dict[str, Any] = Field(default_factory=dict)


class MessageRecord(BaseModel):
    id: str = Field(default_factory=lambda: new_id("msg"))
    document_id: str
    source_original_id: str | None = None
    parent_message_id: str | None = None
    role: MessageRole
    created_at: str | None = None
    message_index: int
    content_text: str
    content_sha256: str
    metadata: dict[str, Any] = Field(default_factory=dict)


class AnalysisArtifact(BaseModel):
    id: str = Field(default_factory=lambda: new_id("analysis"))
    target_id: str
    target_type: Literal["document", "message", "concept", "timeline_event"]
    analysis_type: str
    analyzer_name: str
    analyzer_version: str
    prompt_version: str | None = None
    model_name: str | None = None
    input_sha256: str
    output: dict[str, Any]
    confidence: float | None = None
    created_at: str


class ConceptRecord(BaseModel):
    id: str = Field(default_factory=lambda: new_id("concept"))
    name: str
    summary: str | None = None
    first_seen_at: str | None = None
    last_seen_at: str | None = None
    source_count: int = 0
    strength: float | None = None
    novelty: str | None = None
    human_excitement: Excitement | None = None
    status: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class RelationRecord(BaseModel):
    id: str = Field(default_factory=lambda: new_id("rel"))
    source_id: str
    source_type: str
    target_id: str
    target_type: str
    relation_type: RelationType
    strength: float | None = None
    evidence: list[dict[str, Any]] = Field(default_factory=list)
    generated_by: str | None = None
    status: ReviewStatus = ReviewStatus.UNREVIEWED
    created_at: str
    metadata: dict[str, Any] = Field(default_factory=dict)


class TimelineEvent(BaseModel):
    id: str = Field(default_factory=lambda: new_id("event"))
    title: str
    event_date: str | None = None
    date_precision: DatePrecision = DatePrecision.UNKNOWN
    life_period: str | None = None
    age_estimate: str | None = None
    source_id: str | None = None
    source_type: str | None = None
    themes: list[str] = Field(default_factory=list)
    confidence: float | None = None
    summary: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class HumanOverride(BaseModel):
    id: str = Field(default_factory=lambda: new_id("override"))
    target_id: str
    target_type: str
    field_name: str
    value: Any
    reason: str | None = None
    created_at: str
    updated_at: str


class ImportResult(BaseModel):
    batch: ImportBatch
    raw_artifact: RawSourceArtifact
    documents: list[NormalizedDocument] = Field(default_factory=list)
    messages: list[MessageRecord] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
