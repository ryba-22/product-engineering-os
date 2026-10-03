#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = ROOT.parent / "Polska-Mysl-Architektoniczna-Obsidian"
DEFAULT_OUTPUT = ROOT / "machine" / "pma-registry.json"


def git_sha(path: Path) -> str | None:
    if not (path / ".git").exists():
        return None
    p = subprocess.run(
        ["git", "-C", str(path), "rev-parse", "HEAD"],
        text=True,
        capture_output=True,
    )
    return p.stdout.strip() if p.returncode == 0 else None


def resolve_registry(source: Path) -> tuple[Path, Path]:
    if source.is_file():
        return source, source.parent
    candidate = source / "dist" / "peos" / "registry.json"
    if not candidate.exists():
        raise FileNotFoundError(f"PMA registry not found: {candidate}")
    return candidate, source


def validate_registry(data: dict) -> list[str]:
    errors = []
    if data.get("publication_boundary") != "public-only":
        errors.append("registry publication_boundary must be public-only")
    entries = data.get("entries")
    if not isinstance(entries, list):
        errors.append("registry entries must be a list")
        return errors
    ids = []
    for i, entry in enumerate(entries):
        if not isinstance(entry, dict):
            errors.append(f"entry {i} is not an object")
            continue
        eid = entry.get("id")
        path = str(entry.get("path") or "")
        if not eid:
            errors.append(f"entry {i} has no id")
        else:
            ids.append(eid)
        if not path.startswith("content/"):
            errors.append(f"{eid or i}: path outside public content/: {path}")
        if path.startswith("private/") or path.startswith("assets-private/"):
            errors.append(f"{eid or i}: private path leaked into registry")
    if len(ids) != len(set(ids)):
        errors.append("duplicate PMA entry ids")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source",
        default=os.environ.get("PMA_PATH", str(DEFAULT_SOURCE)),
        help="PMA vault root or registry.json path",
    )
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args()

    source = Path(args.source).expanduser().resolve()
    output = Path(args.output).expanduser().resolve()

    try:
        registry_path, source_root = resolve_registry(source)
        data = json.loads(registry_path.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"FAIL PMA import: {exc}")
        return 1

    errors = validate_registry(data)
    if errors:
        print("FAIL PMA import")
        for error in errors:
            print(f"- {error}")
        return 1

    payload = {
        "schema_version": "1.0.0",
        "source": "Polska-Mysl-Architektoniczna-Obsidian",
        "source_repository": "https://github.com/ryba-22/Polska-Mysl-Architektoniczna-Obsidian",
        "source_sha": git_sha(source_root),
        "publication_boundary": "public-only",
        "entry_count": len(data["entries"]),
        "entries": data["entries"],
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"OK: imported {len(data['entries'])} PMA entries -> {output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
