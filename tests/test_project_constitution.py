import importlib.util
import json
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "scripts" / "discover_project_constitution.py"
spec = importlib.util.spec_from_file_location("constitution", MODULE)
constitution = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(constitution)


def fixture_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "package.json").write_text(
        json.dumps(
            {
                "scripts": {
                    "lint": "eslint .",
                    "typecheck": "tsc --noEmit",
                    "test": "vitest run",
                    "build": "vite build",
                }
            }
        ),
        encoding="utf-8",
    )
    (repo / "package-lock.json").write_text("{}\n", encoding="utf-8")
    (repo / "tsconfig.json").write_text(
        '{"compilerOptions":{"strict":true}}\n', encoding="utf-8"
    )
    (repo / "AGENTS.md").write_text("# Rules\n", encoding="utf-8")
    (repo / ".github" / "workflows").mkdir(parents=True)
    (repo / ".github" / "workflows" / "ci.yml").write_text(
        "jobs:\n  test:\n    steps:\n      - run: npm test\n", encoding="utf-8"
    )
    (repo / "src").mkdir()
    for i in range(5):
        (repo / "src" / f"x{i}.test.ts").write_text("test('x',()=>{})\n", encoding="utf-8")
    subprocess.run(["git", "-C", str(repo), "init", "-q"], check=True)
    subprocess.run(["git", "-C", str(repo), "config", "user.email", "test@example.test"], check=True)
    subprocess.run(["git", "-C", str(repo), "config", "user.name", "Test"], check=True)
    subprocess.run(["git", "-C", str(repo), "add", "."], check=True)
    subprocess.run(["git", "-C", str(repo), "commit", "-qm", "base"], check=True)
    return repo


def test_discovery_records_candidates_without_approving(tmp_path):
    repo = fixture_repo(tmp_path)
    report = constitution.discover(repo)
    ids = {item["id"] for item in report["findings"]}
    assert {"node-script-lint", "node-script-test", "typescript-strict", "ci-workflows"} <= ids
    assert all(item["status"] == "candidate" for item in report["findings"])
    assert report["authority_rule"].startswith("candidate observation")


def test_cli_can_persist_dossier(tmp_path):
    repo = fixture_repo(tmp_path)
    out = tmp_path / "out"
    proc = subprocess.run(
        [str(MODULE), str(repo), "--output-dir", str(out)],
        text=True,
        capture_output=True,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    data = json.loads((out / "observations.json").read_text())
    assert data["git_head"]
    assert (out / "PROJECT-CONSTITUTION-DISCOVERY.md").exists()


def test_discovery_surfaces_package_manager_conflict(tmp_path):
    repo = fixture_repo(tmp_path)
    (repo / "yarn.lock").write_text("# competing manager\n", encoding="utf-8")
    report = constitution.discover(repo)
    ids = {item["id"] for item in report["conflicts"]}
    assert "package-manager-lockfiles" in ids
    conflict = next(item for item in report["conflicts"] if item["id"] == "package-manager-lockfiles")
    assert conflict["status"] == "unresolved"
    assert set(conflict["options"]) == {"npm", "yarn"}
