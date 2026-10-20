"""Check that documentation audits catch omissions outside SKILL.md."""
import json
import shutil
from pathlib import Path

import pytest

from scripts.check_repository import ROOT, GENERATED, inspect


@pytest.fixture
def repository(tmp_path):
    for path in ROOT.rglob("*"):
        relative = path.relative_to(ROOT)
        if GENERATED.intersection(relative.parts):
            continue
        if path.is_file() and (path.suffix in {".md", ".json"} or path.name == "LICENSE"):
            dest = tmp_path / relative
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(path, dest)
    return tmp_path


def test_supporting_documents_are_not_hidden(repository):
    extra = repository / "skills" / "deep-research" / "notes.md"
    extra.write_text("A sentence.\n" * 26)
    assert any("deep-research/notes.md" in error for error in inspect(repository)["errors"])


def test_preserved_source_cannot_grow_under_an_old_exception(repository):
    extra = repository / "skills" / "sr-screener" / "templates" / "prompts.md"
    extra.write_text(extra.read_text() + "\nAdditional rule.\n")
    assert any("保持する原文が変わっています" in error for error in inspect(repository)["errors"])


def test_missing_screening_registration_is_detected(repository):
    path = repository / "package.json"
    data = json.loads(path.read_text())
    data["pi"]["skills"].remove("./skills/sr-screener")
    path.write_text(json.dumps(data))
    assert any("登録内容が一覧と一致しません" in error for error in inspect(repository)["errors"])


def test_broken_supporting_link_is_detected(repository):
    (repository / "README.md").write_text("[missing](missing.md)\n")
    assert any("リンク先がありません" in error for error in inspect(repository)["errors"])


def test_repository_conforms():
    assert inspect(ROOT)["errors"] == []


def test_no_startup_prompt_is_injected():
    config = json.loads((ROOT / "hooks/hooks.json").read_text())
    assert "SessionStart" not in config["hooks"]


def test_plugin_keeps_the_write_guard_wired():
    config = json.loads((ROOT / "hooks/hooks.json").read_text())
    entries = config["hooks"]["PreToolUse"]
    assert any(
        set(entry["matcher"].split("|")) >= {"Write", "Edit", "MultiEdit", "Bash"}
        and any("hooks/run_guard.sh" in hook["command"] for hook in entry["hooks"])
        for entry in entries
    )


def test_only_skills_are_registered():
    assert not (ROOT / "commands").exists()
    for relative in ["package.json"]:
        config = json.loads((ROOT / relative).read_text())
        assert set(config["pi"]) == {"skills"}
    for name in inspect(ROOT)["skills"]:
        assert (ROOT / "skills" / name / "SKILL.md").is_file()
        assert not (ROOT / "skills" / name).is_symlink()
        assert not (ROOT / name).exists()
    assert not (ROOT / "pi").exists()
    assert set(inspect(ROOT)["skills"]) == {
        "deep-research", "academic-paper", "academic-paper-reviewer",
        "academic-pipeline", "sr-screener",
    }
