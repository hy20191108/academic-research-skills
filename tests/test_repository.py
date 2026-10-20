"""Check that documentation audits catch omissions outside SKILL.md."""
import json
import shutil
import subprocess
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
    extra = repository / "deep-research" / "notes.md"
    extra.write_text("A sentence.\n" * 26)
    assert any("deep-research/notes.md" in error for error in inspect(repository)["errors"])


def test_preserved_source_cannot_grow_under_an_old_exception(repository):
    extra = repository / "sr-screener" / "templates" / "prompts.md"
    extra.write_text(extra.read_text() + "\nAdditional rule.\n")
    assert any("保持する原文が変わっています" in error for error in inspect(repository)["errors"])


def test_missing_screening_registration_is_detected(repository):
    path = repository / "pi" / "package.json"
    data = json.loads(path.read_text())
    data["pi"]["skills"].remove("../sr-screener")
    path.write_text(json.dumps(data))
    assert any("登録内容が一覧と一致しません" in error for error in inspect(repository)["errors"])


def test_broken_supporting_link_is_detected(repository):
    (repository / "README.md").write_text("[missing](missing.md)\n")
    assert any("リンク先がありません" in error for error in inspect(repository)["errors"])


def test_repository_conforms():
    assert inspect(ROOT)["errors"] == []


def test_session_start_announces_all_tasks_without_loading_legacy_prompts():
    result = subprocess.run(
        ["bash", str(ROOT / "scripts/announce-ars-loaded.sh")],
        input="{}", text=True, capture_output=True, check=True, cwd=ROOT,
    )
    output = json.loads(result.stdout)["hookSpecificOutput"]
    assert output["hookEventName"] == "SessionStart"
    context = output["additionalContext"]
    assert len(context) <= 1200
    for name in inspect(ROOT)["skills"]:
        assert name in context


def test_plugin_keeps_the_write_guard_wired():
    config = json.loads((ROOT / "hooks/hooks.json").read_text())
    entries = config["hooks"]["PreToolUse"]
    assert any(
        set(entry["matcher"].split("|")) >= {"Write", "Edit", "MultiEdit", "Bash"}
        and any("hooks/run_guard.sh" in hook["command"] for hook in entry["hooks"])
        for entry in entries
    )


def test_japanese_command_checks_its_skill_identifier(repository):
    command = repository / "commands" / "ars-plan.md"
    text = command.read_text().replace(
        "`academic-research-skills:academic-paper`", "`academic-research-skills:missing`"
    )
    command.write_text(text)
    assert any("呼出し先のスキルがありません" in error for error in inspect(repository)["errors"])
