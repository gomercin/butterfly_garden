# Agent Instructions

You are implementing Butterfly Graph.

## Intent

This is a local-first archive and idea graph for rediscovering recurring patterns, dormant project seeds, life echoes, and “shiny butterflies” across personal data.

## Hard constraints

1. Raw exports are immutable.
2. SQLite/canonical records are source of truth.
3. Markdown is generated output plus human curation surface.
4. Do not silently overwrite human edits.
5. Every generated summary/concept/relation must trace to source ids and hashes.
6. Prioritize frictionless CLI before UI.
7. No ChatGPT API dependency in MVP.
8. No two-way sync in MVP, but preserve markers for it.

## First coding goal

Make this work:

```bash
butterfly init
butterfly import-source chatgpt ./data/inbox/chatgpt/export.zip
butterfly analyze --analyzer rules
butterfly export-obsidian
butterfly report butterflies
```

Ask questions only if blocked. Otherwise make reasonable choices and document them.
