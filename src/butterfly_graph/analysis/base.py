from __future__ import annotations

from abc import ABC, abstractmethod

from butterfly_graph.models import AnalysisArtifact, NormalizedDocument


class Analyzer(ABC):
    name: str
    version: str

    @abstractmethod
    def analyze_document(self, document: NormalizedDocument) -> list[AnalysisArtifact]:
        raise NotImplementedError
