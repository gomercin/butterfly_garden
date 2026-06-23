# Open Notebook Experiment

Open Notebook is not the main storage layer for Butterfly Graph. It is a candidate analysis surface.

## Hypothesis

A local RAG/chat notebook may be useful for broad exploratory questions over a selected subset of the archive.

Examples:

- Where did the Translator idea appear before?
- Which old blog posts echo my current consciousness/game ideas?
- Which conversations combine conflict resolution and game mechanics?
- What themes appear both in old newsletters and recent ChatGPT chats?

## Input bundle

Generate a portable bundle:

```bash
butterfly export-open-notebook-bundle
```

Output:

```text
data/open_notebook_bundle/
  README.md
  manifest.json
  documents/
    chatgpt-...md
    wordpress-...md
    gmail-...md
```

## Experiment plan

1. Import only a small subset first: 50-100 high-signal documents.
2. Ask a fixed set of questions.
3. Compare the answers with Butterfly Graph's own reports.
4. Note where Open Notebook is better:
   - semantic recall
   - conversational exploration
   - summarization
5. Note where Butterfly Graph should remain better:
   - source identity
   - timeline precision
   - sync safety
   - human curation
   - repeatable batch processing

## Acceptance criteria

Open Notebook earns a permanent role only if it reliably produces useful insights that are not already visible in Obsidian dashboards.

It should remain optional unless it clearly improves discovery quality.
