# ADR 0001: Canonical core with multiple output surfaces

## Status

Accepted.

## Context

Butterfly Graph may output to Obsidian, Open Notebook, static reports, or future graph/RAG tools. The archive will contain highly personal and long-lived data, so the project must avoid lock-in to one UI or one database owned by an external app.

## Decision

Butterfly Graph will use a canonical local core:

- raw exports are immutable
- normalized records are stored in SQLite and canonical snapshots
- generated analysis artifacts are traceable by source ids and hashes
- output surfaces are implemented as exporters

Obsidian is the primary MVP surface.

Open Notebook is an optional analysis surface via a portable Markdown + manifest bundle.

## Consequences

Positive:

- lower lock-in
- easier future two-way sync
- easier testing
- Git-friendly Obsidian output
- optional RAG experimentation

Negative:

- more code than simply uploading everything to one app
- requires discipline around canonical records vs generated Markdown

## Rule

Markdown is allowed to be human-edited, but canonical source identity lives in the core.

Generated blocks may be refreshed. Human blocks must be preserved.
