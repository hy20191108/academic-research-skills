"""Check every maintained Markdown file and the plugin's public entry points."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
GENERATED = {".git", ".venv", "node_modules", "__pycache__", ".pytest_cache"}


def inspect(root: Path) -> dict:
    exceptions = json.loads((root / "documentation-exceptions.json").read_text())
    files, errors, warnings, skills = [], [], [], []
    seen = set()
    for path in sorted(root.rglob("*.md")):
        relative = path.relative_to(root)
        if GENERATED.intersection(relative.parts):
            continue
        name = relative.as_posix()
        seen.add(name)
        raw = path.read_bytes()
        text = raw.decode("utf-8").replace("\r\n", "\n").replace("\r", "\n")
        lines = text.splitlines()
        record = {"file": name, "lines": len(lines), "characters": len(text)}
        oversized = len(lines) > 25 or len(text) > 1200
        exception = exceptions.get(name)
        if exception:
            record["exception"] = exception["reason"]
            if hashlib.sha256(raw).hexdigest() != exception["sha256"]:
                errors.append(f"{name}: preserved source changed; review its exception")
        elif oversized:
            errors.append(f"{name}: exceeds 25 lines or 1200 characters")
        for number, line in enumerate(lines, 1):
            if len(line) > 40 and re.search(r"[\u3040-\u30ff\u3400-\u9fff]", line):
                warnings.append(f"{name}:{number}: Japanese line has {len(line)} characters")
        if path.name == "SKILL.md" or relative.parts[0] in {"agents", "commands"}:
            match = re.match(r"---\n(.*?)\n---(?:\n|$)", text, re.S)
            try:
                data = yaml.safe_load(match[1]) if match else None
                expected = path.parent.name if path.name == "SKILL.md" else path.stem
                if (
                    not isinstance(data, dict)
                    or data.get("name") != expected
                    or not isinstance(data.get("description"), str)
                    or not 0 < len(data["description"]) <= 15
                    or not data["description"].strip()
                ):
                    raise ValueError("invalid metadata")
            except (ValueError, yaml.YAMLError):
                errors.append(f"{name}: invalid name or description")
            if path.name == "SKILL.md":
                skills.append(path.parent.name)
        for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", text):
            target = target.split("#", 1)[0]
            if not target or re.match(r"[a-zA-Z][a-zA-Z0-9+.-]*:", target):
                continue
            if not (path.parent / target).exists():
                errors.append(f"{name}: missing local link {target}")
        for target in re.findall(r"Trigger the `([^`]+)` skill", text):
            if not (root / target / "SKILL.md").is_file():
                errors.append(f"{name}: missing command target {target}")
        files.append(record)
    for missing in exceptions.keys() - seen:
        errors.append(f"{missing}: stale exception")
    if len(skills) > 50:
        errors.append("more than 50 skills")
    marketplace = json.loads((root / ".claude-plugin/marketplace.json").read_text())
    manifests = [
        (root, marketplace["plugins"][0]["skills"]),
        (root, json.loads((root / "package.json").read_text())["pi"]["skills"]),
        (root / "pi", json.loads((root / "pi/package.json").read_text())["pi"]["skills"]),
    ]
    for base, locations in manifests:
        registered = []
        for location in locations:
            path = base / location / "SKILL.md"
            if not path.is_file():
                errors.append(f"missing registered skill {location}")
            registered.append(path.parent.name)
        if sorted(registered) != sorted(skills):
            errors.append(f"{base.name}: skill registration differs from the catalog")
    return {"skills": skills, "files": files, "warnings": warnings, "errors": errors}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    report = inspect(args.root)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"{len(report['skills'])} skills; {len(report['files'])} Markdown files")
        for item in report["files"]:
            if "exception" in item:
                print(f"Preserved {item['file']} ({item['lines']} lines, "
                      f"{item['characters']} characters): {item['exception']}")
        for message in report["warnings"]:
            print("Warning:", message)
        for message in report["errors"]:
            print("Error:", message)
    return bool(report["errors"])


if __name__ == "__main__":
    raise SystemExit(main())
