# Agent Instructions

You are implementing Butterfly Graph.

## Intent

This is a local-first archive and idea graph for rediscovering recurring patterns, dormant project seeds, life echoes, and “shiny butterflies” across personal data.

The product is not a generic note app. It is a frictionless import → analysis → rediscovery pipeline.

## Architecture

Use a canonical core with multiple output surfaces.

```text
raw exports
  -> canonical SQLite / JSON records
  -> analysis artifacts
  -> exporters
```

Surface roles:

- Obsidian is the garden: editable Markdown, backlinks, graph view, dashboards.
- Open Notebook/local RAG is the microscope: optional exploratory chat over selected bundles.
- SQLite/canonical records are the seed bank: source identity, hashes, analyses, relations, timeline, overrides.

## Hard constraints

1. Raw exports are immutable.
2. SQLite/canonical records are source of truth.
3. Markdown is generated output plus human curation surface.
4. Do not silently overwrite human edits.
5. Every generated summary/concept/relation must trace to source ids and hashes.
6. Prioritize frictionless CLI before UI.
7. No ChatGPT API dependency in MVP.
8. No two-way sync in MVP, but preserve markers for it.
9. Keep Open Notebook optional; do not move source-of-truth responsibilities into it.
10. Prefer small, testable increments over architecture astronauting.

## First coding goal

Make this work:

```bash
butterfly init
butterfly import-source chatgpt ./data/inbox/chatgpt/export.zip
butterfly analyze --analyzer rules
butterfly export-obsidian
butterfly report butterflies
```

Then optionally:

```bash
butterfly export-open-notebook-bundle
```

## Before adding features

Check whether the feature improves one of these:

- import reliability
- analysis quality
- rediscovery quality
- human curation safety
- one-command frictionlessness

If not, defer it.

Ask questions only if blocked. Otherwise make reasonable choices and document them.
