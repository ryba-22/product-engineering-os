#!/usr/bin/env python3
"""Read-only Delivery Assurance. Input claims are not authenticated observations."""
from __future__ import annotations

import argparse
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
import re
import sys
from typing import Callable

from jsonschema import Draft202012Validator, FormatChecker
import yaml
from yaml.constructor import ConstructorError

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "06-modules/delivery-production/delivery-assurance"
SCHEMA = CONTRACT / "release-evidence.schema.json"
POLICY_SCHEMA = CONTRACT / "project-policy.schema.json"
RULES = CONTRACT / "rules.json"
SHA40 = re.compile(r"^[0-9a-fA-F]{40}$")
DIGEST = re.compile(r"^sha256:[0-9a-fA-F]{64}$")
STATUS = {"PASS", "FAIL", "UNKNOWN", "NOT_APPLICABLE", "WAIVED"}


def finding(rule_id: str, status: str, reason: str, evidence: str | None = None) -> dict:
    if status not in STATUS:
        raise ValueError("Invalid rule status")
    return {"rule_id": rule_id, "status": status, "reason": reason, "evidence": evidence}


class UniqueKeyLoader(yaml.BaseLoader):
    """String-valued GitHub YAML, rejecting duplicate keys instead of last-wins parsing."""

    def construct_mapping(self, node, deep=False):
        if not isinstance(node, yaml.MappingNode):
            raise ConstructorError(None, None, "Expected YAML mapping", node.start_mark)
        result = {}
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)
            if key in result:
                raise ConstructorError("mapping", node.start_mark,
                                       "Duplicate mapping key: " + str(key), key_node.start_mark)
            result[key] = self.construct_object(value_node, deep=deep)
        return result


def assess_workflow(path: Path) -> list[dict]:
    """Inspect declared local workflow controls; never imply environment settings were checked."""
    try:
        content = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        return [finding("DA-GHA-000", "UNKNOWN", "Workflow cannot be read: " + type(exc).__name__, str(path))]
    try:
        workflow = yaml.load(content, Loader=UniqueKeyLoader)
    except (yaml.YAMLError, TypeError, ValueError) as exc:
        return [finding("DA-GHA-000", "FAIL", "Invalid/ambiguous YAML: " + " ".join(str(exc).splitlines())[:400], str(path))]
    if not isinstance(workflow, dict):
        return [finding("DA-GHA-000", "FAIL", "Expected workflow mapping", str(path))]
    events = workflow.get("on")
    if not (isinstance(events, dict) and bool(events) or
            isinstance(events, list) and bool(events) or
            isinstance(events, str) and bool(events.strip())):
        return [finding("DA-GHA-000", "FAIL", "Missing/invalid required GitHub 'on' trigger", str(path))]
    jobs = workflow.get("jobs")
    if not isinstance(jobs, dict) or not jobs:
        return [finding("DA-GHA-000", "FAIL", "Missing/invalid jobs mapping", str(path))
                ]  # Not a complete GitHub Actions schema validator.

    action_refs: list[str] = []
    production = False
    dynamic_environment = False
    deployment_like = any(re.search(r"deploy|promot|release|production", str(job_id), re.I) for job_id in jobs)
    deployment_like = deployment_like or bool(re.search(r"deploy|promot|production", str(workflow.get("name", "")), re.I))
    for job in jobs.values():
        if not isinstance(job, dict):
            return [finding("DA-GHA-000", "FAIL", "Invalid job definition", str(path))]
        env = job.get("environment")
        if env == "production" or isinstance(env, dict) and env.get("name") == "production":
            production = True
        if isinstance(env, str) and "${{" in env or isinstance(env, dict) and "${{" in str(env.get("name", "")):
            dynamic_environment = True
        steps = job.get("steps", []) or []
        if not isinstance(steps, list) or any(not isinstance(step, dict) for step in steps):
            return [finding("DA-GHA-000", "FAIL", "Invalid steps list", str(path))]
        action_refs.extend(step["uses"] for step in steps if isinstance(step.get("uses"), str))
        if isinstance(job.get("uses"), str):
            action_refs.append(job["uses"])

    unpinned = [ref for ref in action_refs if not (
        ref.startswith("./") or
        ref.startswith("docker://") and DIGEST.fullmatch(ref.rsplit("@", 1)[-1]) and "@sha256:" in ref or
        not ref.startswith("docker://") and "@" in ref and SHA40.fullmatch(ref.rsplit("@", 1)[1])
    )]
    results = [
        finding("DA-GHA-001", "FAIL" if unpinned else "PASS" if action_refs else "NOT_APPLICABLE",
                "Unpinned external uses: " + ", ".join(unpinned) if unpinned else
                "Uses references are SHA pinned" if action_refs else "No uses references", str(path))
    ]
    workflow_run = (isinstance(events, dict) and "workflow_run" in events or
                    isinstance(events, list) and "workflow_run" in events or
                    events == "workflow_run")
    # Security analysis is job-scoped: a secret in an unrelated job is not proof
    # that a checked-out PR commit can access it. Unknown cross-job flows stay UNKNOWN.
    shared_env = workflow.get("env", {})
    dangerous = False
    for job in jobs.values():
        steps = job.get("steps", []) or []
        upstream_checkout = any(
            str(step.get("uses", "")).startswith("actions/checkout@") and
            "github.event.workflow_run.head_sha" in str((step.get("with") or {}).get("ref", ""))
            for step in steps if isinstance(step.get("with", {}), dict)
        )
        secret_in_job = "secrets." in json.dumps({"env": shared_env, "job": job})
        if workflow_run and upstream_checkout and secret_in_job:
            dangerous = True
    results.append(finding(
        "DA-GHA-002", "FAIL" if dangerous else "UNKNOWN" if workflow_run else "NOT_APPLICABLE",
        "Untrusted workflow_run checkout with same-job secret use" if dangerous else
        "workflow_run needs live trust-boundary review" if workflow_run else "No workflow_run event",
        str(path)
    ))
    results.append(finding(
        "DA-GHA-003", "UNKNOWN" if production or dynamic_environment or deployment_like else "NOT_APPLICABLE",
        "Production/dynamic environment does not prove GitHub protection settings" if production or dynamic_environment
        else "Deploy-like workflow without observed protection settings" if deployment_like
        else "No apparent deployment job/environment; no protection assertion", str(path)
    ))
    results.append(finding("DA-GHA-000", "PASS", "Basic workflow structure and key uniqueness valid (not a full actionlint check)", str(path)))
    return results


def parse_time(value: str) -> datetime:
    dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if dt.utcoffset() is None:
        raise ValueError("Timestamp has no timezone offset")
    return dt.astimezone(timezone.utc)


def malformed_timestamps(value, prefix="record"):
    """Do not depend on jsonschema's optional date-time format extras."""
    if isinstance(value, dict):
        for key, child in value.items():
            if key in {"observed_at", "expires_at"} and isinstance(child, str):
                try:
                    parse_time(child)
                except ValueError:
                    return prefix + "." + key
            problem = malformed_timestamps(child, prefix + "." + key)
            if problem:
                return problem
    elif isinstance(value, list):
        for i, child in enumerate(value):
            problem = malformed_timestamps(child, prefix + "[" + str(i) + "]")
            if problem:
                return problem
    return None


def schema_errors(value: dict, schema_path: Path) -> list[str]:
    validator = Draft202012Validator(json.loads(schema_path.read_text()), format_checker=FormatChecker())
    errors = sorted(validator.iter_errors(value), key=lambda e: str(e.path))
    return ["/".join(map(str, e.path)) + ": " + e.message for e in errors[:5]]


def _authenticated(verifier: Callable | None, kind: str, identifier: str, payload: dict, record: dict) -> bool:
    """Only an independently wired adapter may attest observations; no JSON 'verified' flag."""
    if verifier is None:
        return False
    try:
        return verifier(kind, identifier, payload, record) is True
    except Exception:
        return False


def proof_status(item: dict, as_of: datetime, max_age_minutes: int | None,
                 verifier: Callable | None, kind: str, identifier: str, record: dict) -> str:
    status = item["status"]
    if status == "PASS":
        if not item.get("evidence_ref") or not item.get("observed_at"):
            return "UNKNOWN"
        observed = parse_time(item["observed_at"])
        if observed > as_of:
            return "UNKNOWN"
        if max_age_minutes is not None and as_of - observed > timedelta(minutes=max_age_minutes):
            return "FAIL"
        if not _authenticated(verifier, kind, identifier, item, record):
            return "UNKNOWN"
    if status == "WAIVED":
        acceptance = item["risk_acceptance"]
        if as_of >= parse_time(acceptance["expires_at"]):
            return "FAIL"
        if not _authenticated(verifier, "waiver", kind + ":" + identifier, item, record):
            return "UNKNOWN"
    return status


def assess_release(record: dict, as_of: datetime, policy: dict | None = None,
                   verifier: Callable | None = None, policy_verified: bool = False) -> list[dict]:
    """Assess contradictions and independent evidence, never authenticate self-declared JSON."""
    errs = schema_errors(record, SCHEMA)
    if errs:
        return [finding("DA-REL-000", "FAIL", "Release schema: " + "; ".join(errs))]
    wrong_date = malformed_timestamps(record)
    if wrong_date:
        return [finding("DA-REL-000", "FAIL", "Invalid offset-aware timestamp: " + wrong_date)]
    if as_of.tzinfo is None:
        raise ValueError("as_of must include timezone")

    out: list[dict] = []
    policy_ok = False
    if policy is not None:
        p_errors = schema_errors(policy, POLICY_SCHEMA)
        bad_date = malformed_timestamps(policy)
        if p_errors or bad_date:
            return [finding("DA-REL-006", "FAIL", "Invalid project policy: " + "; ".join(p_errors) + str(bad_date or ""))]
        policy_ok = True
    out.append(finding("DA-REL-006", "PASS" if policy_ok and policy_verified else "UNKNOWN",
                       "Project policy independently verified by calling integration" if policy_ok and policy_verified
                       else "No authenticated, independently pinned project policy; local policy is advisory only"))

    checks = record["checks"]
    gate_ids = [c["id"] for c in checks]
    artifact_names = [a["name"] for a in record["artifacts"]]
    if len(gate_ids) != len(set(gate_ids)) or len(artifact_names) != len(set(artifact_names)):
        return out + [finding("DA-REL-000", "FAIL", "Duplicate CI gate or artifact names")]
    check_map = {c["id"]: c for c in checks}
    artifact_map = {a["name"]: a for a in record["artifacts"]}
    required_checks = policy["required_ci_checks"] if policy_ok else []
    required_artifacts = policy["required_artifacts"] if policy_ok else []
    limits = policy["max_age_minutes"] if policy_ok else {}
    if not required_checks:
        out.append(finding("DA-REL-001", "UNKNOWN", "Required gate set not independently established"))
    for gate in required_checks:
        check = check_map.get(gate)
        if check is None:
            out.append(finding("DA-REL-001", "UNKNOWN", "Required CI gate missing: " + gate))
            continue
        status = proof_status(check, as_of, limits.get("ci_gate"), verifier, "ci_gate", gate, record)
        if status == "NOT_APPLICABLE":
            status = "FAIL"
        out.append(finding("DA-REL-001", status, "Policy-required CI gate: " + gate, check.get("evidence_ref")))
    # Reject declared failure in optional controls rather than silently describing a clean release.
    for check in checks:
        if check["id"] not in required_checks and check["status"] == "FAIL":
            out.append(finding("DA-REL-001", "FAIL", "Other CI gate failed: " + check["id"], check.get("evidence_ref")))

    if not required_artifacts:
        out.append(finding("DA-REL-002", "UNKNOWN", "Required artifact set not independently established"))
    for name in required_artifacts:
        artifact = artifact_map.get(name)
        if artifact is None:
            out.append(finding("DA-REL-002", "UNKNOWN", "Expected artifact absent: " + name))
            continue
        ci, staging, production = (artifact.get(k) for k in ("ci_digest", "staging_digest", "production_digest"))
        if not ci or not staging or record["target_environment"] == "production" and not production:
            status = "UNKNOWN"
            reason = name + ": required artifact digest missing"
        elif ci != staging or record["target_environment"] == "production" and ci != production:
            status = "FAIL"
            reason = name + ": conflicting digest declarations"
        elif not _authenticated(verifier, "artifact", name, artifact, record):
            status = "UNKNOWN"
            reason = name + ": same declared digests, no independent OCI observation"
        else:
            status = "PASS"
            reason = name + ": image identity independently observed"
        out.append(finding("DA-REL-002", status, reason))

    target = record["target_environment"]
    approval = record.get("production_approval")
    if target != "production":
        out.append(finding("DA-REL-003", "NOT_APPLICABLE", "No production promotion"))
    elif approval is None:
        out.append(finding("DA-REL-003", "UNKNOWN", "Production approval missing"))
    else:
        status = proof_status(approval, as_of, limits.get("approval"), verifier, "approval", "production", record)
        out.append(finding("DA-REL-003", "FAIL" if status == "NOT_APPLICABLE" else status,
                           "Production approval", approval.get("evidence_ref")))
    recovery = record.get("recovery")
    if target != "production" and recovery is None:
        out.append(finding("DA-REL-004", "NOT_APPLICABLE", "No production recovery assertion"))
    elif recovery is None or not recovery["required"]:
        out.append(finding("DA-REL-004", "UNKNOWN", "Recovery contract not independently established"))
    else:
        status = proof_status(recovery, as_of, limits.get("recovery"), verifier, "recovery", "production", record)
        if status == "PASS" and as_of >= parse_time(recovery["expires_at"]):
            status = "FAIL"
        out.append(finding("DA-REL-004", "FAIL" if status == "NOT_APPLICABLE" else status,
                           "Recovery proof", recovery.get("evidence_ref")))
    health = record.get("runtime_health")
    if target != "production":
        out.append(finding("DA-REL-005", "NOT_APPLICABLE", "No production runtime assertion"))
    elif health is None:
        out.append(finding("DA-REL-005", "UNKNOWN", "Runtime health missing"))
    else:
        status = proof_status(health, as_of, limits.get("runtime_health"), verifier, "runtime_health", "production", record)
        if status == "PASS" and health.get("source") != "runtime":
            status = "UNKNOWN"
        out.append(finding("DA-REL-005", "FAIL" if status == "NOT_APPLICABLE" else status,
                           "Runtime health", health.get("evidence_ref")))
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
    return "ELIGIBLE_FOR_REVIEW"  # advisory assessment, never a deployment authorization


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Read-only delivery assessment; cannot authorize deployment")
    sub = p.add_subparsers(dest="command", required=True)
    w = sub.add_parser("workflows")
    w.add_argument("paths", nargs="+", type=Path)
    r = sub.add_parser("release")
    r.add_argument("path", type=Path)
    r.add_argument("--policy", type=Path, help="Project-owned policy; not itself authenticated")
    r.add_argument("--as-of", help="ISO8601 timestamp with timezone")
    args = p.parse_args(argv)
    if args.command == "workflows":
        results = [dict(f, path=str(path)) for path in args.paths for f in assess_workflow(path)]
    else:
        try:
            record = json.loads(args.path.read_text(encoding="utf-8"))
            policy = json.loads(args.policy.read_text(encoding="utf-8")) if args.policy else None
            now = parse_time(args.as_of) if args.as_of else datetime.now(timezone.utc)
            # No CLI adapter to GitHub/registry/runtime: do not claim authenticated PASS.
            results = assess_release(record, now, policy=policy)
        except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
            results = [finding("DA-REL-000", "UNKNOWN", "Input cannot be verified: " + type(exc).__name__)]
    print(json.dumps({"mode": "ADVISORY", "verdict": aggregate(results), "findings": results},
                     ensure_ascii=False, indent=2))
    return 0  # Deliberately never enforces a production gate.


if __name__ == "__main__":
    sys.exit(main())
