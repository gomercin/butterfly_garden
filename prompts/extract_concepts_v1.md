Return valid JSON only.

Extract reusable concept nodes from this document. A concept is a recurring idea, pattern, metaphor, project seed, life theme, or creative direction.

Schema:

```json
{
  "concepts": [
    {
      "name": "...",
      "summary": "...",
      "type": "concept|project|theme|metaphor|echo",
      "evidence": ["..."],
      "related_names": ["..."],
      "novelty": "low|medium|high",
      "emotional_charge": "low|medium|high",
      "confidence": 0.0
    }
  ]
}
```

Document:

{{document_text}}
