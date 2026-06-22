Return valid JSON only.

Extract timeline-relevant events. Dates may be exact, year-level, approximate, or unknown.

Schema:

```json
{
  "events": [
    {
      "title": "...",
      "event_date": "YYYY-MM-DD or YYYY-MM or YYYY or null",
      "date_precision": "exact|month|year|approximate|unknown",
      "life_period": "childhood|teenage|university|early-career|netherlands|parenthood|ai-era|unknown",
      "age_estimate": "...",
      "themes": ["..."],
      "summary": "...",
      "confidence": 0.0
    }
  ]
}
```

Document:

{{document_text}}
