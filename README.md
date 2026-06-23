# Butterfly Graph Starter

Local-first personal archive → concept graph → multiple discovery surfaces.

This starter is intentionally small but sync-aware. It imports exports from ChatGPT, Gmail MBOX, WordPress WXR, and later YouTube Takeout, normalizes them into stable records, stores them in SQLite, runs analysis, and exports readable Markdown.

```text
raw exports
  → canonical documents/messages
  → analyses/concepts/relations/timeline
  → output surfaces
  → human curation
```

## Core rule

Raw exports are immutable. SQLite/canonical JSON are the truth layer. Markdown is a readable interface. Human edits are preserved through marked blocks and later `human_overrides`.

## Surfaces

Butterfly Graph should not depend on one frontend.

```text
SQLite/canonical data = seed bank
Obsidian = garden
Open Notebook / local RAG = microscope
```

Current exporters:

- `ObsidianExporter` for local Markdown vaults and graph browsing.
- `OpenNotebookBundleExporter` for a portable Markdown + manifest bundle that can be tested with Open Notebook or similar local RAG tools.

See:

- `docs/FRONTEND_STRATEGY.md`
- `docs/OPEN_NOTEBOOK_EXPERIMENT.md`
- `docs/adr/0001-canonical-core-multiple-surfaces.md`

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

Optional Open Notebook/RAG bundle:

```bash
butterfly export-open-notebook-bundle
# or
butterfly run-all --source-type chatgpt --source data/inbox/chatgpt/export.zip --include-open-notebook-bundle
```

## Folder intent

```text
data/inbox/                 put raw exports here
data/raw/                   optional immutable copies later
data/normalized/            optional normalized JSON snapshots later
data/summaries/             generated JSON/Markdown analyses later
data/open_notebook_bundle/  portable Markdown bundle for RAG experiments
data/graph.sqlite           SQLite truth layer
vault/                      Obsidian output
prompts/                    local LLM and ChatGPT enrichment prompts
docs/                       architecture, data model, MVP plan, task queue
```

## MVP success criterion

The first real milestone is not a perfect second brain. It is seeing 5 forgotten-but-interesting butterflies from old conversations/posts.

## Codex entry points

Start with:

- `prompts/AGENT_INSTRUCTIONS.md`
- `prompts/codex_plan_prompt.md`
- `docs/CODEX_TASKS.md`
- GitHub issues in this repository
