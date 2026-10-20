"""移行時の出力と非破壊操作を固定する．"""
import re

import pytest

from scripts import migrate_literature_corpus_to_v3_7_3 as migration


SOURCE = '''# 利用者のコメント
literature_corpus:
  - citation_key: "new"
    year: 2024
  - citation_key: partial
    year: 2023
    contamination_signals:
      preprint_post_llm_inflection: false
    contamination_signals_backfilled_at: '2020-01-01T00:00:00Z'
  - citation_key: missing
    title: "年が不明"
  - citation_key: manual
    year: 2022
    obtained_via: manual
'''

EXPECTED = '''# 利用者のコメント
literature_corpus:
  - citation_key: "new"
    year: 2024
    contamination_signals:
      preprint_post_llm_inflection: true
      semantic_scholar_unmatched: false
    contamination_signals_backfilled_at: NOW
  - citation_key: partial
    year: 2023
    contamination_signals:
      preprint_post_llm_inflection: false
      semantic_scholar_unmatched: false
    contamination_signals_backfilled_at: '2020-01-01T00:00:00Z'
  - citation_key: missing
    title: "年が不明"
  - citation_key: manual
    year: 2022
    obtained_via: manual
    contamination_signals:
      preprint_post_llm_inflection: true
    contamination_signals_backfilled_at: NOW
'''


@pytest.mark.parametrize("dry_run", [False, True])
def test_migration_preserves_format_and_existing_evidence(tmp_path, monkeypatch, dry_run):
    passport = tmp_path / "passport.yaml"
    passport.write_text(SOURCE)

    def signals(entry, client):
        result = {"preprint_post_llm_inflection": True}
        if entry.get("obtained_via") != "manual":
            result["semantic_scholar_unmatched"] = False
        return result, {}

    monkeypatch.setattr(migration.cs, "build_signals_with_omissions", signals)
    report = migration.migrate_passport(passport, ss_client=object(), dry_run=dry_run)
    assert report == {
        "processed": 4, "patched": 3, "skipped_already_migrated": 0,
        "skipped_insufficient_data": 1, "manual_unmatched_omitted": 1,
    }
    output = passport.read_text()
    if dry_run:
        assert output == SOURCE
    else:
        normalized = re.sub(
            r"(?m)^(    contamination_signals_backfilled_at: )'\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ'$",
            lambda match: match[0] if "2020-01-01" in match[0] else match[1] + "NOW",
            output,
        )
        assert normalized == EXPECTED
        again = migration.migrate_passport(passport, ss_client=object(), dry_run=False)
        assert again["patched"] == 0
        assert again["skipped_already_migrated"] == 3
        assert passport.read_text() == output
