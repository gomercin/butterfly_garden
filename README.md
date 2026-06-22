# Butterfly Graph Starter

Local-first personal archive → concept graph → Obsidian vault.

This starter is intentionally small but sync-aware. It imports exports from ChatGPT, Gmail MBOX, WordPress WXR, and later YouTube Takeout, normalizes them into stable records, stores them in SQLite, runs analysis, and exports readable Markdown.

```text
raw exports
  → canonical documents/messages
  → analyses/concepts/relations/timeline
  → Obsidian notes
  → human curation
```

## Core rule

Raw exports are immutable. SQLite/canonical JSON are the truth layer. Markdown is the readable interface. Human edits are preserved through marked blocks and later `human_overrides`.

## Install

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

## First run

```bash
butterfly init
butterfly import-source chatgpt data/inbox/chatgpt/export.zip
butterfly analyze --analyzer rules
butterfly export-obsidian
butterfly report butterflies
```

## One-command path

```bash
butterfly run-all --source-type chatgpt --source data/inbox/chatgpt/export.zip
```

## Folder intent

```text
data/inbox/       put raw exports here
data/raw/         optional immutable copies later
data/normalized/  optional normalized JSON snapshots later
data/summaries/   generated JSON/Markdown analyses later
data/graph.sqlite SQLite truth layer
vault/            Obsidian output
prompts/          local LLM and ChatGPT enrichment prompts
docs/             architecture, data model, MVP plan
```

## MVP success criterion

The first real milestone is not a perfect second brain. It is seeing 5 forgotten-but-interesting butterflies from old conversations/posts.
