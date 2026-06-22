from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

from butterfly_graph.models import ImportResult


class Importer(ABC):
    source_system_name: str

    @abstractmethod
    def import_source(self, source_path: Path, source_group: str | None = None) -> ImportResult:
        raise NotImplementedError
