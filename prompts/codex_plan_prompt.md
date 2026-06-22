# Codex Planning Prompt

Read the repository docs and produce a concrete implementation plan for the next coding session.

Focus on the next useful milestone, not the full dream.

Constraints:

- No web UI yet.
- No ChatGPT API integration.
- No two-way sync yet.
- Keep raw imports immutable.
- Preserve future sync markers in Markdown.
- Make the CLI path work first.

Target command flow:

```bash
butterfly init
butterfly import-source chatgpt ./data/inbox/chatgpt/export.zip
butterfly analyze --analyzer rules
butterfly export-obsidian
```
