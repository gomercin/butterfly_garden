# Data Model

Core entities live in `src/butterfly_graph/models.py`.

## ImportBatch
One import run. Useful when exports are re-imported later.

## RawSourceArtifact
A raw file/archive, with path, SHA256, source system, and source group.

## NormalizedDocument
A logical document: ChatGPT conversation, WordPress post, email, YouTube history item, or manual story.

## MessageRecord
Message-level records for chats/emails. Important for future partial reprocessing and diffing.

## AnalysisArtifact
Generated summaries/extractions. Stores analyzer metadata and input hash.

## ConceptRecord
A reusable “large neuron”: recurring pattern, idea, project, metaphor, or theme.

## RelationRecord
Typed edge between entities. Examples: `echoes`, `inspired_by`, `evolves_into`, `same_pattern_as`.

## TimelineEvent
An exact or approximate life/story event.

## HumanOverride
Future-safe way to store manual decisions without overwriting generated data.
