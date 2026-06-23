# Frontend and Analysis Surface Strategy

Butterfly Graph should not be married to a single UI.

The durable architecture is:

```text
raw exports
  -> canonical SQLite / JSON records
  -> analysis artifacts
  -> one or more output surfaces
```

## Recommended surfaces

### Obsidian: the garden

Use Obsidian as the primary human curation surface.

It is best for:

- local Markdown files
- backlinks
- graph browsing
- manual edits
- Git-friendly diffs
- future sync markers
- dashboards such as Forgotten Butterflies, Echo Index, and Personal Timeline

### Open Notebook: the microscope

Use Open Notebook or similar local RAG tools as an optional research/chat layer.

It is best for:

- asking questions over a controlled source bundle
- testing local LLM behavior
- comparing semantic search against Butterfly Graph's own reports
- exploring old blogs, ChatGPT summaries, and source documents interactively

Open Notebook should not be the source of truth at this stage.

### Butterfly Graph core: the seed bank

SQLite plus canonical records remain the stable middle layer.

The core owns:

- raw source identity
- normalized document records
- message-level hashes
- analysis artifacts
- concepts
- relations
- timeline events
- human overrides

## Rule of thumb

Do not ask one tool to do all jobs.

```text
Obsidian = garden
Open Notebook = microscope
SQLite/canonical data = seed bank
```

## Implementation implication

Exporters must be pluggable.

Current exporters:

- `ObsidianExporter`
- `OpenNotebookBundleExporter`

Future exporters may include:

- static HTML
- Neo4j
- GraphML
- JSON-LD
- MCP-like local server
