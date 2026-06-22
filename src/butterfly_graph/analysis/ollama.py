from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import requests

from butterfly_graph.analysis.base import Analyzer
from butterfly_graph.hashing import sha256_text
from butterfly_graph.models import AnalysisArtifact, NormalizedDocument
from butterfly_graph.timeutils import utc_now_iso


class OllamaAnalyzer(Analyzer):
    name = "ollama"
    version = "0.1.0"

    def __init__(self, ollama_url: str = "http://localhost:11434", model: str = "llama3.1", prompt_path: Path | None = None):
        self.ollama_url = ollama_url.rstrip("/")
        self.model = model
        self.prompt_path = prompt_path or Path("prompts/extract_summary_v1.md")

    def _render_prompt(self, text: str) -> str:
        template = self.prompt_path.read_text(encoding="utf-8")
        return template.replace("{{document_text}}", text[:24000])

    def _generate(self, prompt: str) -> dict[str, Any]:
        response = requests.post(f"{self.ollama_url}/api/generate", json={"model": self.model, "prompt": prompt, "stream": False}, timeout=180)
        response.raise_for_status()
        raw = response.json().get("response", "{}")
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return {"raw_response": raw, "parse_error": True}

    def analyze_document(self, document: NormalizedDocument) -> list[AnalysisArtifact]:
        output = self._generate(self._render_prompt(document.content_text))
        return [AnalysisArtifact(target_id=document.id, target_type="document", analysis_type="summary", analyzer_name=self.name, analyzer_version=self.version, prompt_version=self.prompt_path.stem, model_name=self.model, input_sha256=sha256_text(document.content_text), output=output, confidence=output.get("confidence") if isinstance(output, dict) else None, created_at=utc_now_iso())]
