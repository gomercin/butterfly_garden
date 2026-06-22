# Architecture

## Pipeline

```text
ChatGPT export / Gmail MBOX / WordPress WXR / YouTube Takeout
        ↓
Importer interface
        ↓
Canonical document + message records
        ↓
SQLite store + hashes
        ↓
Analyzers: rules, Ollama, manual ChatGPT enrichment
        ↓
Concepts, relations, summaries, timeline events, echoes
        ↓
Obsidian exporter
```

## Design decisions

1. **Raw source is immutable.** Never edit or rewrite exports.
2. **SQLite is the source of truth.** Markdown is generated output plus human curation surface.
3. **Every generated object is traceable.** Store analyzer name, version, prompt version, model, input hash, and evidence.
4. **Future sync is protected.** Generated and human sections are separated in Markdown.
5. **Friction over completeness.** Build one useful `run-all` path first.

## What not to build first

- web app
- Neo4j
- browser extension
- automatic two-way sync
- ChatGPT API integration
- perfect ontology

The first product moment is: “Oh damn, I forgot this idea, and it connects to that.”
