#!/usr/bin/env python3
"""Discover repository-local evidence for a candidate Project Constitution.

The scanner is deliberately conservative: it records observations and enforcement
signals, but never promotes a finding to an approved project rule.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover
    tomllib = None

DOC_NAMES = (
    "AGENTS.md",
    "CLAUDE.md",
    "CONTRIBUTING.md",
    "README.md",
    "ARCHITECTURE.md",
)
LOCKFILES = {
    "pnpm-lock.yaml": "pnpm",
    "yarn.lock": "yarn",
    "package-lock.json": "npm",
    "bun.lockb": "bun",
    "uv.lock": "uv",
    "poetry.lock": "poetry",
}
SOURCE_EXTENSIONS = {
    ".ts", ".tsx", ".js", ".jsx", ".py", ".go", ".rs", ".java", ".kt", ".cs", ".rb", ".php",
}
SKIP_DIRS = {
    ".git", "node_modules", ".next", "dist", "build", "coverage", ".venv", "venv",
    ".pytest_cache", ".mypy_cache", ".ruff_cache", "vendor",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def run_git(repo: Path, *args: str) -> str | None:
    proc = subprocess.run(
        ["git", "-C", str(repo), *args],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    )
    return proc.stdout.strip() if proc.returncode == 0 else None


def add(
    findings: list[dict[str, Any]],
    fid: str,
    category: str,
    statement: str,
    confidence: int,
    evidence: list[str],
    source_types: list[str],
    enforcement: str = "none",
) -> None:
    findings.append(
        {
            "id": fid,
            "category": category,
            "statement": statement,
            "confidence": confidence,
            "status": "candidate",
            "evidence": evidence,
            "source_types": source_types,
            "enforcement": enforcement,
        }
    )


def load_json(path: Path) -> dict[str, Any] | None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return value if isinstance(value, dict) else None


def scan_package(repo: Path, findings: list[dict[str, Any]]) -> None:
    pkg = repo / "package.json"
    data = load_json(pkg)
    if not data:
        return
    scripts = data.get("scripts")
    if isinstance(scripts, dict):
        for purpose in ("lint", "typecheck", "test", "build", "format", "check"):
            command = scripts.get(purpose)
            if isinstance(command, str) and command.strip():
                add(
                    findings,
                    f"node-script-{purpose}",
                    "required-command",
                    f"package.json defines the {purpose} command: {command}",
                    95,
                    [f"package.json:scripts.{purpose}"],
                    ["config"],
                    "script",
                )


def scan_typescript(repo: Path, findings: list[dict[str, Any]]) -> None:
    for name in ("tsconfig.json", "tsconfig.base.json"):
        path = repo / name
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        if re.search(r'"strict"\s*:\s*true', text):
            add(
                findings,
                "typescript-strict",
                "language",
                "TypeScript strict mode is configured.",
                98,
                [f"{name}: compilerOptions.strict=true"],
                ["config"],
                "compiler",
            )
        break


def scan_python(repo: Path, findings: list[dict[str, Any]]) -> None:
    path = repo / "pyproject.toml"
    if not path.exists() or tomllib is None:
        return
    try:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return
    tool = data.get("tool", {})
    if not isinstance(tool, dict):
        return
    for name in ("ruff", "black", "mypy", "pytest", "pytest.ini_options"):
        if name in tool:
            normalized = "pytest" if name.startswith("pytest") else name
            add(
                findings,
                f"python-tool-{normalized}",
                "tooling",
                f"pyproject.toml configures {normalized}.",
                95,
                [f"pyproject.toml:[tool.{name}]"],
                ["config"],
                "tool-config",
            )


def scan_makefile(repo: Path, findings: list[dict[str, Any]]) -> None:
    path = repo / "Makefile"
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8", errors="ignore")
    targets = []
    for line in text.splitlines():
        match = re.match(r"^([A-Za-z0-9_.-]+):(?:\s|$)", line)
        if match and not line.startswith("."):
            targets.append(match.group(1))
    important = [x for x in ("test", "lint", "check", "validate", "build", "ci") if x in targets]
    if important:
        add(
            findings,
            "makefile-quality-targets",
            "required-command",
            "Makefile exposes quality/build targets: " + ", ".join(important),
            90,
            ["Makefile:" + ",".join(important)],
            ["config"],
            "script",
        )


def scan_ci(repo: Path, findings: list[dict[str, Any]]) -> None:
    root = repo / ".github" / "workflows"
    if not root.exists():
        return
    workflows = sorted(list(root.glob("*.yml")) + list(root.glob("*.yaml")))
    if workflows:
        add(
            findings,
            "ci-workflows",
            "delivery",
            f"Repository has {len(workflows)} GitHub Actions workflow(s).",
            95,
            [str(p.relative_to(repo)) for p in workflows],
            ["ci"],
            "ci",
        )
    commands: list[str] = []
    evidence: list[str] = []
    for path in workflows:
        for lineno, raw in enumerate(path.read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
            stripped = raw.strip()
            if stripped.startswith("run:"):
                cmd = stripped[4:].strip()
                if cmd:
                    commands.append(cmd)
                    evidence.append(f"{path.relative_to(repo)}:{lineno}")
    if commands:
        sample = commands[:8]
        add(
            findings,
            "ci-run-commands",
            "required-command",
            "CI executes repository commands: " + " | ".join(sample),
            95,
            evidence[:8],
            ["ci"],
            "ci",
        )


def scan_instruction_docs(repo: Path, findings: list[dict[str, Any]]) -> None:
    found = [name for name in DOC_NAMES if (repo / name).exists()]
    if found:
        add(
            findings,
            "instruction-documents",
            "documentation",
            "Repository contains project instruction/context documents: " + ", ".join(found),
            75,
            found,
            ["docs"],
            "human-review",
        )


def scan_configs(repo: Path, findings: list[dict[str, Any]]) -> None:
    groups = {
        "formatter": [
            ".prettierrc", ".prettierrc.json", ".prettierrc.js", "prettier.config.js",
            "prettier.config.mjs", ".editorconfig",
        ],
        "lint": [
            "eslint.config.js", "eslint.config.mjs", ".eslintrc", ".eslintrc.json",
            "ruff.toml",
        ],
    }
    for category, names in groups.items():
        found = [name for name in names if (repo / name).exists()]
        if found:
            add(
                findings,
                f"{category}-config",
                "tooling",
                f"Repository has explicit {category} configuration.",
                95,
                found,
                ["config"],
                "tool-config",
            )

    lockfiles = [name for name in LOCKFILES if (repo / name).exists()]
    if lockfiles:
        managers = sorted({LOCKFILES[name] for name in lockfiles})
        add(
            findings,
            "package-manager",
            "tooling",
            "Repository package/dependency manager evidence: " + ", ".join(managers),
            98,
            lockfiles,
            ["config"],
            "lockfile",
        )


def detect_conflicts(repo: Path) -> list[dict[str, Any]]:
    conflicts: list[dict[str, Any]] = []
    present = [(name, manager) for name, manager in LOCKFILES.items() if (repo / name).exists()]
    managers = sorted({manager for _, manager in present})
    if len(managers) > 1:
        conflicts.append(
            {
                "id": "package-manager-lockfiles",
                "category": "tooling",
                "statement": "Multiple package/dependency manager lockfiles are present; intended ownership must be resolved.",
                "evidence": [name for name, _ in present],
                "options": managers,
                "status": "unresolved",
            }
        )

    package = load_json(repo / "package.json") if (repo / "package.json").exists() else None
    declared = package.get("packageManager") if isinstance(package, dict) else None
    if isinstance(declared, str) and declared.strip():
        declared_manager = declared.split("@", 1)[0].strip().lower()
        lock_managers = {manager for _, manager in present}
        if lock_managers and declared_manager not in lock_managers:
            conflicts.append(
                {
                    "id": "package-manager-declaration",
                    "category": "tooling",
                    "statement": "package.json packageManager does not match the observed lockfile manager.",
                    "evidence": [f"package.json:packageManager={declared}"] + [name for name, _ in present],
                    "options": [declared_manager] + sorted(lock_managers),
                    "status": "unresolved",
                }
            )
    return conflicts


def iter_files(repo: Path):
    for path in repo.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(repo)
        if any(part in SKIP_DIRS for part in rel.parts):
            continue
        yield path, rel


def scan_code_patterns(repo: Path, findings: list[dict[str, Any]]) -> None:
    language_counts: Counter[str] = Counter()
    test_counts: Counter[str] = Counter()
    total_tests = 0
    for path, rel in iter_files(repo):
        ext = path.suffix.lower()
        if ext in SOURCE_EXTENSIONS:
            language_counts[ext] += 1
        name = path.name
        pattern = None
        if re.search(r"\.(test|spec)\.[^.]+$", name):
            pattern = "*.test/spec.*"
        elif name.startswith("test_") and ext == ".py":
            pattern = "test_*.py"
        elif "tests" in rel.parts or "__tests__" in rel.parts:
            pattern = "tests-directory"
        if pattern:
            test_counts[pattern] += 1
            total_tests += 1

    if language_counts:
        top = ", ".join(f"{ext}:{count}" for ext, count in language_counts.most_common(5))
        add(
            findings,
            "source-language-shape",
            "code-shape",
            "Observed source-file distribution: " + top,
            70,
            [f"repository scan: {sum(language_counts.values())} source files"],
            ["code"],
        )
    if total_tests:
        top_pattern, top_count = test_counts.most_common(1)[0]
        share = top_count / total_tests
        confidence = 85 if total_tests >= 5 and share >= 0.75 else 70
        add(
            findings,
            "test-layout",
            "testing",
            f"Observed test layout: {dict(test_counts)}",
            confidence,
            [f"repository scan: {total_tests} test-like files"],
            ["code"],
        )


def discover(repo: Path) -> dict[str, Any]:
    repo = repo.expanduser().resolve()
    if not repo.exists() or not repo.is_dir():
        raise ValueError(f"repository path does not exist: {repo}")

    findings: list[dict[str, Any]] = []
    scan_package(repo, findings)
    scan_typescript(repo, findings)
    scan_python(repo, findings)
    scan_makefile(repo, findings)
    scan_ci(repo, findings)
    scan_instruction_docs(repo, findings)
    scan_configs(repo, findings)
    scan_code_patterns(repo, findings)

    head = run_git(repo, "rev-parse", "HEAD")
    dirty_text = run_git(repo, "status", "--porcelain")
    return {
        "version": 1,
        "generated_at": utc_now(),
        "repository": str(repo),
        "git_head": head,
        "git_dirty": None if dirty_text is None else bool(dirty_text),
        "authority_rule": "candidate observation != approved rule != executable enforcement",
        "findings": sorted(findings, key=lambda x: (-x["confidence"], x["id"])),
        "conflicts": detect_conflicts(repo),
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Project Constitution Discovery",
        "",
        f"Repository: {report['repository']}",
        f"Git HEAD: {report.get('git_head') or 'unknown'}",
        f"Generated: {report['generated_at']}",
        "",
        "> These are repository observations, not approved project rules.",
        "",
        "| Candidate | Category | Confidence | Enforcement | Observation | Evidence |",
        "|---|---|---:|---|---|---|",
    ]
    for f in report["findings"]:
        evidence = "<br>".join(f["evidence"])
        statement = f["statement"].replace("|", "\\|")
        lines.append(
            f"| {f['id']} | {f['category']} | {f['confidence']} | {f['enforcement']} | "
            f"{statement} | {evidence} |"
        )
    lines += ["", "## Conflicts", ""]
    conflicts = report.get("conflicts") or []
    if conflicts:
        lines += ["| Conflict | Observation | Evidence |", "|---|---|---|"]
        for conflict in conflicts:
            evidence = "<br>".join(conflict.get("evidence") or [])
            statement = str(conflict.get("statement") or "").replace("|", "\\|")
            lines.append(f"| {conflict['id']} | {statement} | {evidence} |")
    else:
        lines.append("No repository-local conflicts detected by the current scanner.")
    lines += [
        "",
        "## Promotion rule",
        "",
        "Review each candidate and every unresolved conflict. Approve, reject or scope candidates explicitly. A high confidence score does not grant authority.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Discover candidate project constitution evidence")
    parser.add_argument("repository")
    parser.add_argument("--output-dir")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    try:
        report = discover(Path(args.repository))
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    if args.output_dir:
        out = Path(args.output_dir).expanduser().resolve()
        out.mkdir(parents=True, exist_ok=True)
        (out / "observations.json").write_text(
            json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        (out / "PROJECT-CONSTITUTION-DISCOVERY.md").write_text(
            render_markdown(report), encoding="utf-8"
        )
        print(out)
        return 0

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(render_markdown(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
