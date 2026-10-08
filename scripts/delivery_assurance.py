#!/usr/bin/env python3
"""Advisory, read-only delivery evidence assessment. No network or mutations."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import sys

from jsonschema import Draft202012Validator, FormatChecker
import yaml

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "06-modules/delivery-production/delivery-assurance/release-evidence.schema.json"
RULES = ROOT / "06-modules/delivery-production/delivery-assurance/rules.json"
SHA40 = re.compile(r"^[0-9a-fA-F]{40}$")
DIGEST = re.compile(r"^sha256:[0-9a-fA-F]{64}$")
STATUS = {"PASS", "FAIL", "UNKNOWN", "NOT_APPLICABLE", "WAIVED"}


def finding(rule_id: str, status: str, reason: str, evidence: str | None = None) -> dict:
    assert status in STATUS
    return {"rule_id": rule_id, "status": status, "reason": reason, "evidence": evidence}


def assess_workflow(path: Path) -> list[dict]:
    """Local YAML describes only declared controls, not remote GitHub settings."""
    try:
        content = path.read_text(encoding="utf-8")
        workflow = yaml.load(content, Loader=yaml.BaseLoader)
    except (OSError, yaml.YAMLError, UnicodeError) as exc:
        return [finding("DA-GHA-000", "UNKNOWN", f"Workflow unreadable or invalid: {type(exc).__name__}", str(path))]
    if not isinstance(workflow, dict):
        return [finding("DA-GHA-000", "UNKNOWN", "Expected YAML mapping", str(path))]
    jobs = workflow.get("jobs")
    if not isinstance(jobs, dict) or not jobs:
        return [finding("DA-GHA-000", "UNKNOWN", "Missing/invalid jobs mapping", str(path))]
    action_refs = []
    production = False
    for job in jobs.values():
        if not isinstance(job, dict):
            return [finding("DA-GHA-000", "UNKNOWN", "Invalid job definition", str(path))]
        env = job.get("environment")
        if env == "production" or (isinstance(env, dict) and env.get("name") == "production"):
            production = True
        steps = job.get("steps", []) or []
        if not isinstance(steps, list) or any(not isinstance(step, dict) for step in steps):
            return [finding("DA-GHA-000", "UNKNOWN", "Invalid steps list", str(path))]
        for step in steps:
            if isinstance(step.get("uses"), str):
                action_refs.append(step["uses"])
        if isinstance(job.get("uses"), str):
            action_refs.append(job["uses"])
    unpinned = [ref for ref in action_refs if not (
        ref.startswith("./") or
        (ref.startswith("docker://") and "@sha256:" in ref and DIGEST.fullmatch(ref.rsplit("@", 1)[1])) or
        (not ref.startswith("docker://") and "@" in ref and SHA40.fullmatch(ref.rsplit("@", 1)[1]))
    )]
    results = [
        finding("DA-GHA-001", "FAIL" if unpinned else ("PASS" if action_refs else "NOT_APPLICABLE"),
                "Unpinned external action/reusable workflow: " + ", ".join(unpinned) if unpinned
                else "External uses pinned to full SHA" if action_refs else "No uses references", str(path))
    ]
    events = workflow.get("on", {})
    workflow_run = isinstance(events, dict) and "workflow_run" in events or (
        isinstance(events, list) and "workflow_run" in events) or events == "workflow_run"
    privileged_checkout = workflow_run and any(
        isinstance(step.get("with"), dict) and
        "github.event.workflow_run.head_sha" in str(step["with"].get("ref", "")) and
        str(step.get("uses", "")).startswith("actions/checkout@")
        for job in jobs.values() for step in (job.get("steps", []) or [])
    ) and "secrets." in json.dumps(workflow)
    results.append(finding(
        "DA-GHA-002", "FAIL" if privileged_checkout else "UNKNOWN" if workflow_run else "NOT_APPLICABLE",
        "workflow_run head SHA checkout combined with secret reference" if privileged_checkout
        else "workflow_run trust boundary requires privileged-run and upstream artifact review" if workflow_run
        else "No workflow_run trigger", str(path)))
    results.append(finding(
        "DA-GHA-003", "UNKNOWN" if production else "NOT_APPLICABLE",
        "YAML production environment does not prove GitHub environment protection settings" if production
        else "No static production environment declaration", str(path)))
    return results


def parse_time(value: str) -> datetime:
    dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if dt.utcoffset() is None:
        raise ValueError("timestamp must include timezone")
    return dt.astimezone(timezone.utc)


def valid_proof(item: dict, as_of: datetime) -> bool:
    return bool(item.get("evidence_ref") and item.get("observed_at") and
                parse_time(item["observed_at"]) <= as_of)


def proof_status(item: dict, as_of: datetime) -> str:
    status = item["status"]
    if status == "PASS" and not valid_proof(item, as_of):
        return "UNKNOWN"
    if status == "WAIVED":
        acceptance = item["risk_acceptance"]
        if as_of >= parse_time(acceptance["expires_at"]):
            return "FAIL"
    return status


def assess_release(record: dict, as_of: datetime) -> list[dict]:
    """Assess observed release claims; skipped/missing proofs never become PASS."""
    errors = sorted(Draft202012Validator(json.loads(SCHEMA.read_text()), format_checker=FormatChecker()).iter_errors(record), key=lambda e: str(e.path))
    if errors:
        return [finding("DA-REL-000", "FAIL", "Invalid evidence schema: " + "; ".join(
            "/".join(map(str, e.path)) + ": " + e.message for e in errors[:5]))]
    # jsonschema's date-time FormatChecker may lack optional format dependencies.
    # Do not depend on those packages to validate material evidence timestamps.
    def validate_timestamps(value, at="release"):
        if isinstance(value, dict):
            for key, nested in value.items():
                if key in {"observed_at", "expires_at"} and isinstance(nested, str):
                    try:
                        parse_time(nested)
                    except ValueError:
                        return f"{at}.{key}: invalid offset-aware ISO8601 timestamp"
                error = validate_timestamps(nested, f"{at}.{key}")
                if error:
                    return error
        elif isinstance(value, list):
            for i, nested in enumerate(value):
                error = validate_timestamps(nested, f"{at}[{i}]")
                if error:
                    return error
        return None

    timestamp_error = validate_timestamps(record)
    if timestamp_error:
        return [finding("DA-REL-000", "FAIL", timestamp_error)]
    out = []
    checks = record["checks"]
    required = [c for c in checks if c["required"]]
    if not required:
        out.append(finding("DA-REL-001", "UNKNOWN", "No required CI gates evidenced"))
    for check in required:
        status = proof_status(check, as_of)
        if status == "NOT_APPLICABLE":
            status = "FAIL"  # a required gate cannot disappear through its own evidence payload
        out.append(finding("DA-REL-001", status, "Required CI gate: " + check["id"], check.get("evidence_ref")))
    target = record["target_environment"]
    for artifact in record["artifacts"]:
        name = artifact["name"]
        ci, staging, production = (artifact.get(k) for k in ("ci_digest", "staging_digest", "production_digest"))
        if not ci or not DIGEST.fullmatch(ci):
            out.append(finding("DA-REL-002", "UNKNOWN", f"{name}: missing valid CI-built digest"))
        elif not staging:
            out.append(finding("DA-REL-002", "UNKNOWN", f"{name}: staging digest not observed"))
        elif ci != staging:
            out.append(finding("DA-REL-002", "FAIL", f"{name}: CI/staging digest mismatch"))
        elif target == "production" and not production:
            out.append(finding("DA-REL-002", "UNKNOWN", f"{name}: production digest not observed"))
        elif target == "production" and production != ci:
            out.append(finding("DA-REL-002", "FAIL", f"{name}: CI/production digest mismatch"))
        else:
            out.append(finding("DA-REL-002", "PASS", f"{name}: all required observed digests agree"))
    if not record["artifacts"]:
        out.append(finding("DA-REL-002", "UNKNOWN", "No release artifacts identified"))
    approval = record.get("production_approval")
    if target != "production":
        out.append(finding("DA-REL-003", "NOT_APPLICABLE", "Production approval not required for staging-only evaluation"))
    elif approval is None:
        out.append(finding("DA-REL-003", "UNKNOWN", "Production approval evidence missing"))
    else:
        status = proof_status(approval, as_of)
        if status == "NOT_APPLICABLE":
            status = "FAIL"  # production deployment cannot self-exempt the approval
        out.append(finding("DA-REL-003", status, "Production approval evidence", approval.get("evidence_ref")))
    recovery = record.get("recovery")
    if recovery is None:
        out.append(finding("DA-REL-004", "UNKNOWN" if target == "production" else "NOT_APPLICABLE", "Recovery evidence missing"))
    elif not recovery["required"]:
        out.append(finding("DA-REL-004", "UNKNOWN" if target == "production" else "NOT_APPLICABLE",
                           "Project recovery policy not independently verified" if target == "production"
                           else "No production recovery requirement for staging"))
    else:
        status = proof_status(recovery, as_of)
        if status == "NOT_APPLICABLE":
            status = "FAIL"  # a required recovery proof cannot be marked inapplicable
        if status == "PASS" and as_of >= parse_time(recovery["expires_at"]):
            status = "FAIL"
        out.append(finding("DA-REL-004", status, "Recovery proof" +
                           (" expired" if status == "FAIL" and recovery["status"] == "PASS" else ""),
                           recovery.get("evidence_ref")))
    health = record.get("runtime_health")
    if target != "production":
        out.append(finding("DA-REL-005", "NOT_APPLICABLE", "Runtime health is not claimed for staging candidate"))
    elif health is None:
        out.append(finding("DA-REL-005", "UNKNOWN", "No production runtime observation"))
    else:
        status = proof_status(health, as_of)
        if status == "NOT_APPLICABLE":
            status = "FAIL"
        if status == "PASS" and health.get("source") != "runtime":
            status = "UNKNOWN"
        out.append(finding("DA-REL-005", status, "Production runtime health", health.get("evidence_ref")))
    return out


def aggregate(results: list[dict]) -> str:
    states = {r["status"] for r in results}
    if "FAIL" in states:
        return "BLOCKED"
    if "UNKNOWN" in states:
        return "UNVERIFIED"
    if "WAIVED" in states:
        return "REVIEW_REQUIRED"
    if not results or states == {"NOT_APPLICABLE"}:
        return "UNVERIFIED"
    return "ELIGIBLE_FOR_REVIEW"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Read-only Delivery Assurance (advisory, not production authorization)")
    sub = parser.add_subparsers(dest="command", required=True)
    w = sub.add_parser("workflows")
    w.add_argument("paths", nargs="+", type=Path)
    r = sub.add_parser("release")
    r.add_argument("path", type=Path)
    r.add_argument("--as-of", help="ISO8601 timestamp with timezone, for deterministic evaluation")
    args = parser.parse_args(argv)
    if args.command == "workflows":
        results = [dict(f, path=str(path)) for path in args.paths for f in assess_workflow(path)]
    else:
        try:
            record = json.loads(args.path.read_text(encoding="utf-8"))
            now = parse_time(args.as_of) if args.as_of else datetime.now(timezone.utc)
            results = assess_release(record, now)
        except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
            results = [finding("DA-REL-000", "UNKNOWN", f"Input unavailable/invalid: {type(exc).__name__}", str(args.path))]
    print(json.dumps({"mode": "ADVISORY", "verdict": aggregate(results), "findings": results},
                     ensure_ascii=False, indent=2))
    return 0  # advisory mode: semantic FAIL is in machine-readable report, not process exit code


if __name__ == "__main__":
    sys.exit(main())
