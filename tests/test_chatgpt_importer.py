from pathlib import Path

from butterfly_graph.importers.chatgpt import ChatGPTImporter


def test_chatgpt_importer_from_json(tmp_path: Path):
    fixture = Path("tests/fixtures/chatgpt_conversations.json")
    target = tmp_path / "conversations.json"
    target.write_text(fixture.read_text(encoding="utf-8"), encoding="utf-8")
    result = ChatGPTImporter().import_source(target)
    assert len(result.documents) == 1
    assert len(result.messages) == 2
    assert result.documents[0].title == "Translator Game"
