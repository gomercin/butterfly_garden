# MVP Plan

## Milestone 1 — Skeleton

- CLI
- SQLite schema
- Pydantic models
- importer interfaces
- Obsidian exporter stub

Done when `butterfly init` works.

## Milestone 2 — ChatGPT import

- Parse `conversations.json` from ZIP or folder.
- Store conversations and message records.
- Export conversation notes.

Done when a real export produces Markdown files.

## Milestone 3 — Rules analysis

- Extract rough topics.
- Score candidate butterflies.
- Generate dashboard.

Done when `butterfly report butterflies` shows candidates.

## Milestone 4 — WordPress + Gmail

- Parse WXR.
- Parse selected MBOX.
- Keep source groups separate.

Done when old blogs/newsletters appear as separate clusters.

## Milestone 5 — Local LLM

- Ollama adapter.
- Summary prompt.
- Concept prompt.
- Timeline prompt.

Done when 10 documents can be summarized locally.

## Milestone 6 — Echoes and timeline

- Detect repeated concepts across years.
- Build Echo Index.
- Build Personal Timeline.
