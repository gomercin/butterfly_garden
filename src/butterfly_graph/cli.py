from __future__ import annotations

import json
from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console
from rich.table import Table

from butterfly_graph.analysis.ollama import OllamaAnalyzer
from butterfly_graph.analysis.rules import RulesAnalyzer
from butterfly_graph.config import get_settings
from butterfly_graph.exporters.obsidian import ObsidianExporter
from butterfly_graph.importers.chatgpt import ChatGPTImporter
from butterfly_graph.importers.gmail_mbox import GmailMboxImporter
from butterfly_graph.importers.wordpress import WordPressWxrImporter
from butterfly_graph.importers.youtube import YouTubeTakeoutImporter
from butterfly_graph.models import DocumentType, NormalizedDocument, SourceSystem
from butterfly_graph.storage import SQLiteStore

app = typer.Typer(help="Butterfly Graph CLI")
console = Console()


def get_store() -> SQLiteStore:
    return SQLiteStore(get_settings().db_path)


@app.command()
def init() -> None:
    settings = get_settings()
    for path in [
        Path("data/inbox"),
        Path("data/raw"),
        Path("data/normalized"),
        Path("data/summaries"),
        Path("data/embeddings"),
        settings.vault_path,
    ]:
        path.mkdir(parents=True, exist_ok=True)
    store = SQLiteStore(settings.db_path)
    store.init_db()
    console.print(
        f"[green]Initialized Butterfly Graph[/green]\n"
        f"Database: {settings.db_path}\n"
        f"Vault: {settings.vault_path}"
    )


@app.command("import-source")
def import_source(
    source_type: Annotated[str, typer.Argument(help="chatgpt | gmail | wordpress | youtube")],
    source_path: Annotated[Path, typer.Argument(help="Path to export file/folder")],
    source_group: Annotated[str | None, typer.Option(help="Optional source group label")] = None,
) -> None:
    store = get_store()
    store.init_db()
    importers = {
        "chatgpt": ChatGPTImporter(),
        "gmail": GmailMboxImporter(),
        "wordpress": WordPressWxrImporter(),
        "youtube": YouTubeTakeoutImporter(),
    }
    importer = importers.get(source_type)
    if importer is None:
        raise typer.BadParameter(f"Unknown source type: {source_type}")
    result = importer.import_source(source_path, source_group=source_group)
    store.upsert_import_batch(result.batch)
    store.upsert_raw_artifact(result.raw_artifact)
    store.upsert_documents(result.documents)
    store.upsert_messages(result.messages)
    console.print(f"[green]Imported {len(result.documents)} documents and {len(result.messages)} messages[/green]")
    for warning in result.warnings:
        console.print(f"[yellow]Warning:[/yellow] {warning}")


@app.command()
def analyze(
    analyzer: Annotated[str, typer.Option(help="rules | ollama")] = "rules",
    limit: Annotated[int | None, typer.Option(help="Limit documents for test runs")] = None,
) -> None:
    settings = get_settings()
    store = get_store()
    store.init_db()
    analyzer_impl = RulesAnalyzer() if analyzer == "rules" else OllamaAnalyzer(settings.ollama_url, settings.ollama_model)
    count = 0
    for row in store.list_documents(limit=limit):
        doc = NormalizedDocument(
            id=row["id"],
            source_system=SourceSystem(row["source_system"]),
            source_group=row["source_group"],
            source_original_id=row["source_original_id"],
            title=row["title"],
            document_type=DocumentType(row["document_type"]),
            created_at=row["created_at"],
            updated_at=row["updated_at"],
            imported_at=row["imported_at"],
            language=row["language"],
            raw_artifact_id=row["raw_artifact_id"],
            raw_sha256=row["raw_sha256"],
            normalized_sha256=row["normalized_sha256"],
            content_text=row["content_text"],
            metadata={},
        )
        for artifact in analyzer_impl.analyze_document(doc):
            store.insert_analysis(artifact)
            count += 1
    console.print(f"[green]Created {count} analysis artifacts using {analyzer}[/green]")


@app.command("export-obsidian")
def export_obsidian() -> None:
    settings = get_settings()
    store = get_store()
    store.init_db()
    ObsidianExporter(store, settings.vault_path).export_all()
    console.print(f"[green]Exported Obsidian vault to {settings.vault_path}[/green]")


@app.command()
def report(kind: Annotated[str, typer.Argument(help="butterflies | documents")] = "butterflies") -> None:
    store = get_store()
    store.init_db()
    if kind == "documents":
        table = Table(title="Documents")
        table.add_column("Title")
        table.add_column("Source")
        table.add_column("Created")
        for row in store.list_documents(limit=50):
            table.add_row(row["title"][:60], row["source_system"], str(row["created_at"]))
        console.print(table)
        return
    if kind == "butterflies":
        table = Table(title="Butterfly Candidates")
        table.add_column("Score")
        table.add_column("Target")
        table.add_column("Triggers")
        for row in store.list_analyses("summary"):
            output = json.loads(row["output_json"])
            score = output.get("shiny_butterfly_score")
            if score is not None and float(score) >= 0.25:
                table.add_row(f"{float(score):.2f}", row["target_id"], ", ".join(output.get("activation_triggers", [])))
        console.print(table)
        return
    raise typer.BadParameter(f"Unknown report kind: {kind}")


@app.command("run-all")
def run_all(
    source_type: Annotated[str, typer.Option(help="chatgpt | gmail | wordpress | youtube")],
    source: Annotated[Path, typer.Option(help="Path to export file/folder")],
    analyzer: Annotated[str, typer.Option(help="rules | ollama")] = "rules",
) -> None:
    init()
    import_source(source_type, source)
    analyze(analyzer=analyzer)
    export_obsidian()
    report("butterflies")
