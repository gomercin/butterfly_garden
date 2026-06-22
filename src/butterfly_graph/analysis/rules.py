from __future__ import annotations

import re

from butterfly_graph.analysis.base import Analyzer
from butterfly_graph.hashing import sha256_text
from butterfly_graph.models import AnalysisArtifact, NormalizedDocument
from butterfly_graph.timeutils import utc_now_iso

BUTTERFLY_PATTERNS = [r"what if", r"could build", r"project", r"game", r"idea", r"prototype", r"experiment", r"maybe", r"perhaps"]
TOPIC_KEYWORDS = {
    "consciousness": ["consciousness", "conscious", "mind", "self"],
    "conflict": ["conflict", "translator", "misunderstanding", "communication"],
    "ai": ["llm", "chatgpt", "codex", "agent", "ai"],
    "games": ["game", "rpg", "simulation", "game of life"],
    "music": ["clarinet", "music", "song", "repertoire", "chord"],
    "neurodivergence": ["adhd", "autism", "audhd", "routine", "activation energy"],
    "teaching": ["training", "coaching", "teach", "workshop"],
}


class RulesAnalyzer(Analyzer):
    name = "rules"
    version = "0.1.0"

    def analyze_document(self, document: NormalizedDocument) -> list[AnalysisArtifact]:
        text = document.content_text.lower()
        topics = [topic for topic, words in TOPIC_KEYWORDS.items() if any(w in text for w in words)]
        hits = [pattern for pattern in BUTTERFLY_PATTERNS if re.search(pattern, text)]
        score = min(1.0, len(topics) * 0.12 + len(hits) * 0.1)
        output = {"summary_short": document.content_text[:500].strip(), "key_topics": topics, "shiny_butterfly_score": score, "butterfly_pattern_hits": hits, "activation_triggers": topics, "open_loops": [], "note": "Rule-based analysis only. Use Ollama for richer summaries."}
        return [AnalysisArtifact(target_id=document.id, target_type="document", analysis_type="summary", analyzer_name=self.name, analyzer_version=self.version, input_sha256=sha256_text(document.content_text), output=output, confidence=0.35, created_at=utc_now_iso())]
