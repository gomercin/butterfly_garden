# Sync Design Notes

MVP is read-only, but imports must be future sync-safe.

## Stable anchors

Store:

- source_system
- source_group
- source_original_id
- raw_sha256
- normalized_sha256
- import_batch_id
- message_id / parent_message_id where available

## Generated and human blocks

Use Obsidian markers:

```markdown
<!-- butterfly:generated:start summary v1 -->
...
<!-- butterfly:generated:end summary v1 -->

<!-- butterfly:human:start notes -->
...
<!-- butterfly:human:end notes -->
```

Future exporters may replace generated blocks but must preserve human blocks.

## Human edits become data

Later, import edits as `human_overrides`, not as mutations of generated analysis.
