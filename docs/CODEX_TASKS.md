# Codex Task Queue

This file mirrors the GitHub issues. Use it when starting Codex in plan mode.

## Working rule

Prioritize frictionless visible value over architectural completeness.

A good task result is something that makes this command path better:

```bash
butterfly init
butterfly import-source chatgpt ./data/inbox/chatgpt/export.zip
butterfly analyze --analyzer rules
butterfly export-obsidian
butterfly report butterflies
```

Do not start with Open Notebook, Neo4j, a web UI, or full two-way sync.

## MVP Task 1: harden starter project

- Run tests locally.
- Fix syntax/type/runtime issues.
- Ensure `pip install -e .` works.
- Ensure CLI command registration works.
- Add smoke test for `butterfly init`.

## MVP Task 2: improve ChatGPT importer

- Test with real export shape.
- Preserve conversation/message ids.
- Handle missing timestamps.
- Preserve attachments metadata if available.
- Make re-import idempotent.

## MVP Task 3: Obsidian exporter v1

- Export stable filenames.
- Preserve human blocks.
- Add generated summary block from latest analysis.
- Create dashboards:
  - Forgotten Butterflies
  - Echo Index
  - Personal Timeline

## MVP Task 4: local LLM analysis

- Add chunking.
- Improve JSON parsing.
- Store prompt/model/input hash.
- Add retry/repair for malformed JSON.
- Support summary, concept, and timeline prompts.

## MVP Task 5: source importers

- Harden WordPress WXR importer.
- Harden Gmail MBOX importer.
- Add source group conventions.
- Keep YouTube as experimental/noisy source.

## MVP Task 6: concept graph

- Generate concept records from analyses.
- Create relations with evidence.
- Add relation types:
  - mentions
  - echoes
  - evolves_into
  - possible_project
  - childhood_echo

## MVP Task 7: timeline and echoes

- Extract timeline events.
- Support approximate dates and life periods.
- Detect concepts appearing across distant periods.
- Generate `40 Echoes/Echo Index.md`.

## MVP Task 8: future sync preparation

- Preserve generated/human markers.
- Add parser for human-edited Markdown blocks.
- Store human overrides.
- Never overwrite human meaning silently.

## Later Phase: output surface experiments

These are deliberately not MVP tasks.

- Open Notebook / local RAG bundle exporter.
- Static HTML explorer.
- GraphML / Neo4j export.
- MCP-like local query server.

Open Notebook is interesting, but it should come after the core import/analyze/export loop proves useful with real ChatGPT, WordPress, and Gmail exports.
