#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Callable

from jsonschema import Draft7Validator

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = "01-governance/source-registry.json"
EVIDENCE_PATH = "02-evidence/evidence-ledger.json"
POLICY_PATH = ROOT / "machine" / "source-delta-policy.json"
SCHEMA_PATH = ROOT / "01-governance" / "source-delta.schema.json"
REPORTS_DIR = ROOT / "01-governance" / "source-deltas"

FIELD_DIMENSIONS = {
    "name": "identity",
    "url": "provenance",
    "tier": "authority",
    "domains": "scope",
    "strength": "strength",
    "verified_at": "freshness",
    "cutoff_target": "cutoff",
    "evidence_ledger": "evidence",
}
SHA_RE = re.compile(r"^[0-9a-f]{40,64}$")
DELTA_ID_RE = re.compile(r"^SDL-[A-Z0-9-]+$")
DECISION_PATH_RE = re.compile(r"^03-decisions/(PDR|ADR|UDR|SDR|DDR|ODR|TDR)-[0-9]{3,}\.(json|md)$")
LEDGER_DELTA_SOURCE_ID = "EVIDENCE-LEDGER"
REGISTRY_DELTA_SOURCE_ID = "SOURCE-REGISTRY"


def load_policy() -> dict[str, Any]:
    return json.loads(POLICY_PATH.read_text())


def load_json_bytes(raw: bytes) -> dict[str, Any]:
    return json.loads(raw.decode("utf-8"))


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def source_map(registry: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {item["id"]: item for item in registry.get("sources", [])}


def evidence_items(ledger: dict[str, Any]) -> list[dict[str, Any]]:
    return ledger.get("items", [])


def evidence_source_ids(ledger: dict[str, Any]) -> set[str]:
    return {
        source_id
        for item in evidence_items(ledger)
        for source_id in item.get("source_ids", [])
    }


def changed_fields(before: dict[str, Any], after: dict[str, Any]) -> list[str]:
    keys = sorted(set(before) | set(after))
    return [key for key in keys if before.get(key) != after.get(key)]


def change_dimensions(fields: list[str]) -> list[str]:
    return sorted({FIELD_DIMENSIONS.get(field, "metadata") for field in fields})


def evidence_state_for_source(ledger: dict[str, Any], source_id: str) -> dict[str, dict[str, Any]]:
    return {
        item["id"]: item
        for item in evidence_items(ledger)
        if source_id in item.get("source_ids", [])
    }


def evidence_changed_for_source(
    source_id: str,
    base_ledger: dict[str, Any],
    head_ledger: dict[str, Any],
) -> bool:
    return evidence_state_for_source(base_ledger, source_id) != evidence_state_for_source(head_ledger, source_id)


def ledger_metadata(ledger: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in ledger.items() if key != "items"}


def registry_metadata(registry: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in registry.items() if key != "sources"}


def orphan_changed_evidence(
    base_ledger: dict[str, Any],
    head_ledger: dict[str, Any],
) -> list[dict[str, Any]]:
    base = {item["id"]: item for item in evidence_items(base_ledger)}
    head = {item["id"]: item for item in evidence_items(head_ledger)}
    impacted = []
    for evidence_id in sorted(set(base) | set(head)):
        before = base.get(evidence_id)
        after = head.get(evidence_id)
        if before == after:
            continue
        source_ids = set((before or {}).get("source_ids", [])) | set((after or {}).get("source_ids", []))
        if source_ids:
            continue
        current = after or before or {}
        impacted.append({
            "id": evidence_id,
            "baseline_status": (before or {}).get("status", ""),
            "head_status": (after or {}).get("status", ""),
            "strength": current.get("strength", ""),
            "scope": current.get("scope", ""),
            "baseline_cites": False,
            "head_cites": False,
        })
    return impacted


def affected_evidence_for(
    source_id: str,
    base_ledger: dict[str, Any],
    head_ledger: dict[str, Any],
) -> list[dict[str, Any]]:
    base = {item["id"]: item for item in evidence_items(base_ledger)}
    head = {item["id"]: item for item in evidence_items(head_ledger)}
    impacted = []
    for evidence_id in sorted(set(base) | set(head)):
        before = base.get(evidence_id)
        after = head.get(evidence_id)
        baseline_cites = bool(before and source_id in before.get("source_ids", []))
        head_cites = bool(after and source_id in after.get("source_ids", []))
        if not baseline_cites and not head_cites:
            continue
        current = after or before or {}
        impacted.append({
            "id": evidence_id,
            "baseline_status": (before or {}).get("status", ""),
            "head_status": (after or {}).get("status", ""),
            "strength": current.get("strength", ""),
            "scope": current.get("scope", ""),
            "baseline_cites": baseline_cites,
            "head_cites": head_cites,
        })
    return impacted


def value_downgraded(before: Any, after: Any, ranks: dict[str, int]) -> bool:
    if before == after:
        return False
    if before is None and after is not None:
        return False
    if before is not None and after is None:
        return True
    if before not in ranks or after not in ranks:
        return True
    return ranks[after] < ranks[before]


def risk_for(
    event: str,
    before: dict[str, Any] | None,
    after: dict[str, Any] | None,
    impacted: list[dict[str, Any]],
    policy: dict[str, Any],
) -> str:
    risk_policy = policy["risk"]
    if event == "REMOVED":
        return risk_policy["REMOVED"]

    before = before or {}
    after = after or {}
    if value_downgraded(before.get("tier"), after.get("tier"), policy["authority_rank"]):
        return risk_policy["authority_downgrade"]
    if value_downgraded(before.get("strength"), after.get("strength"), policy["strength_rank"]):
        return risk_policy["strength_downgrade"]

    live_statuses = set(policy["live_evidence_statuses"])
    if any(
        item.get("baseline_status") in live_statuses or item.get("head_status") in live_statuses
        for item in impacted
    ):
        return risk_policy["live_evidence_impacted"]

    return risk_policy["ADDED"] if event == "ADDED" else risk_policy["CHANGED"]


def exact_evidence_match(text: str, evidence_id: str) -> bool:
    pattern = rf"(?<![A-Za-z0-9-]){re.escape(evidence_id)}(?![A-Za-z0-9-])"
    return re.search(pattern, text) is not None


def excluded_downstream_path(rel: str) -> bool:
    if rel in {EVIDENCE_PATH, "PACKAGE-INDEX.json"}:
        return True
    if rel.startswith("01-governance/source-deltas/"):
        return True
    if rel.startswith("05-evals/"):
        name = Path(rel).name
        if (
            name.startswith(("executor-", "judge-", "final-results", "run-manifest"))
            or "raw" in name
            or name.endswith(".log")
        ):
            return True
    return False


def downstream_refs_for(evidence_ids: list[str], root: Path = ROOT) -> list[str]:
    if not evidence_ids:
        return []
    refs: set[str] = set()
    excluded_parts = {".git", "__pycache__", ".pytest_cache", ".venv"}
    for path in root.rglob("*"):
        if not path.is_file() or any(part in excluded_parts for part in path.parts):
            continue
        rel = path.relative_to(root).as_posix()
        if excluded_downstream_path(rel):
            continue
        if path.suffix not in {".md", ".json", ".py", ".yml", ".yaml"}:
            continue
        try:
            text = path.read_text(errors="ignore")
        except OSError:
            continue
        if any(exact_evidence_match(text, evidence_id) for evidence_id in evidence_ids):
            refs.add(rel)
    return sorted(refs)


def detect_from_documents(
    base_registry: dict[str, Any],
    head_registry: dict[str, Any],
    head_ledger: dict[str, Any],
    *,
    base_ledger: dict[str, Any] | None = None,
    base_ref: str = "0000000000000000000000000000000000000000",
    head_ref: str = "1111111111111111111111111111111111111111",
    hashes: dict[str, str] | None = None,
    root: Path = ROOT,
    downstream_resolver: Callable[[list[str]], list[str]] | None = None,
) -> dict[str, Any]:
    policy = load_policy()
    base_ledger = base_ledger or head_ledger
    base = source_map(base_registry)
    head = source_map(head_registry)
    reserved_ids = {LEDGER_DELTA_SOURCE_ID, REGISTRY_DELTA_SOURCE_ID}
    collisions = sorted(reserved_ids & (set(base) | set(head)))
    if collisions:
        raise ValueError(
            "reserved source-delta ids present in registry: " + ", ".join(collisions)
        )
    resolver = downstream_resolver or (lambda ids: downstream_refs_for(ids, root=root))
    source_ids = (
        set(base)
        | set(head)
        | evidence_source_ids(base_ledger)
        | evidence_source_ids(head_ledger)
    )
    deltas = []

    for source_id in sorted(source_ids):
        before = base.get(source_id)
        after = head.get(source_id)
        impacted = affected_evidence_for(source_id, base_ledger, head_ledger)
        evidence_changed = evidence_changed_for_source(source_id, base_ledger, head_ledger)

        if before is None and after is not None:
            event = "ADDED"
            fields = sorted(after)
        elif before is not None and after is None:
            event = "REMOVED"
            fields = sorted(before)
        elif before is not None and after is not None:
            fields = changed_fields(before, after)
            if evidence_changed:
                fields.append("evidence_ledger")
            fields = sorted(set(fields))
            if not fields:
                continue
            event = "CHANGED"
        else:
            if not evidence_changed:
                continue
            event = "CHANGED"
            fields = ["evidence_ledger"]

        evidence_ids = [item["id"] for item in impacted]
        deltas.append({
            "id": f"SDL-{source_id}",
            "source_id": source_id,
            "event": event,
            "risk": risk_for(event, before, after, impacted, policy),
            "change_dimensions": change_dimensions(fields),
            "changed_fields": fields,
            "before": before,
            "after": after,
            "affected_evidence": impacted,
            "downstream_refs": resolver(evidence_ids),
            "classification": "UNASSESSED",
            "rationale": "",
            "reviewed_evidence_ids": [],
            "downstream_actions": [],
            "resolution": "pending",
            "replacement_evidence_ids": [],
            "decision_record": None,
            "promotion_gate": "BLOCKED",
        })

    registry_metadata_changed = registry_metadata(base_registry) != registry_metadata(head_registry)
    if registry_metadata_changed:
        all_evidence = []
        base_items = {item["id"]: item for item in evidence_items(base_ledger)}
        head_items = {item["id"]: item for item in evidence_items(head_ledger)}
        for evidence_id in sorted(set(base_items) | set(head_items)):
            before_item = base_items.get(evidence_id) or {}
            after_item = head_items.get(evidence_id) or {}
            current = after_item or before_item
            all_evidence.append({
                "id": evidence_id,
                "baseline_status": before_item.get("status", ""),
                "head_status": after_item.get("status", ""),
                "strength": current.get("strength", ""),
                "scope": current.get("scope", ""),
                "baseline_cites": False,
                "head_cites": False,
            })
        all_ids = [item["id"] for item in all_evidence]
        deltas.append({
            "id": f"SDL-{REGISTRY_DELTA_SOURCE_ID}",
            "source_id": REGISTRY_DELTA_SOURCE_ID,
            "event": "CHANGED",
            "risk": "R3",
            "change_dimensions": ["metadata"],
            "changed_fields": ["source_registry_metadata"],
            "before": {"registry_metadata": registry_metadata(base_registry)},
            "after": {"registry_metadata": registry_metadata(head_registry)},
            "affected_evidence": all_evidence,
            "downstream_refs": resolver(all_ids),
            "classification": "UNASSESSED",
            "rationale": "",
            "reviewed_evidence_ids": [],
            "downstream_actions": [],
            "resolution": "pending",
            "replacement_evidence_ids": [],
            "decision_record": None,
            "promotion_gate": "BLOCKED",
        })

    orphan_impacted = orphan_changed_evidence(base_ledger, head_ledger)
    metadata_changed = ledger_metadata(base_ledger) != ledger_metadata(head_ledger)
    if orphan_impacted or metadata_changed:
        orphan_ids = [item["id"] for item in orphan_impacted]
        deltas.append({
            "id": f"SDL-{LEDGER_DELTA_SOURCE_ID}",
            "source_id": LEDGER_DELTA_SOURCE_ID,
            "event": "CHANGED",
            "risk": risk_for("CHANGED", None, None, orphan_impacted, policy),
            "change_dimensions": ["evidence"],
            "changed_fields": ["evidence_ledger"],
            "before": {"ledger_metadata": ledger_metadata(base_ledger)},
            "after": {"ledger_metadata": ledger_metadata(head_ledger)},
            "affected_evidence": orphan_impacted,
            "downstream_refs": resolver(orphan_ids),
            "classification": "UNASSESSED",
            "rationale": "",
            "reviewed_evidence_ids": [],
            "downstream_actions": [],
            "resolution": "pending",
            "replacement_evidence_ids": [],
            "decision_record": None,
            "promotion_gate": "BLOCKED",
        })

    if hashes is None:
        hashes = {
            "base_registry_sha256": sha256(json.dumps(base_registry, sort_keys=True).encode()),
            "head_registry_sha256": sha256(json.dumps(head_registry, sort_keys=True).encode()),
            "base_evidence_ledger_sha256": sha256(json.dumps(base_ledger, sort_keys=True).encode()),
            "head_evidence_ledger_sha256": sha256(json.dumps(head_ledger, sort_keys=True).encode()),
        }

    return {
        "version": "1.0.0",
        "base_ref": base_ref,
        "head_ref": head_ref,
        "hashes": hashes,
        "head_evidence_ids": sorted(
            item["id"] for item in evidence_items(head_ledger) if item.get("id")
        ),
        "head_evidence_statuses": {
            item["id"]: item.get("status", "")
            for item in evidence_items(head_ledger)
            if item.get("id")
        },
        "deltas": deltas,
    }


def readiness_errors(
    delta: dict[str, Any],
    policy: dict[str, Any],
    head_evidence_ids: set[str] | None = None,
    head_evidence_statuses: dict[str, str] | None = None,
) -> list[str]:
    errors = []
    classification = delta.get("classification")
    resolution = delta.get("resolution")
    class_policy = policy["classifications"].get(classification)

    if not class_policy:
        return [f"unknown classification: {classification}"]
    if classification == "UNASSESSED":
        errors.append("semantic delta is UNASSESSED")
    if resolution == "pending":
        errors.append("resolution is pending")
    if resolution not in class_policy["allowed_resolutions"]:
        errors.append(f"{classification} cannot resolve as {resolution}")

    rationale = delta.get("rationale")
    if classification != "UNASSESSED":
        if not isinstance(rationale, str) or len(rationale.strip()) < policy["min_rationale_chars"]:
            errors.append(
                f"semantic assessment rationale must be at least {policy['min_rationale_chars']} characters"
            )

    live_statuses = set(policy["live_evidence_statuses"])
    live_ids = {
        item["id"]
        for item in delta.get("affected_evidence", [])
        if item.get("baseline_status") in live_statuses or item.get("head_status") in live_statuses
    }
    reviewed = set(delta.get("reviewed_evidence_ids", []))
    missing_reviews = sorted(live_ids - reviewed)
    if missing_reviews:
        errors.append("unreviewed live evidence: " + ", ".join(missing_reviews))

    actions = delta.get("downstream_actions", [])
    min_action_chars = policy["min_downstream_action_chars"]
    min_action_words = policy.get("min_downstream_action_words", 1)
    substantive_actions = [
        action for action in actions
        if isinstance(action, str)
        and action == action.strip()
        and "\n" not in action
        and "\r" not in action
        and len(action) >= min_action_chars
        and len(action.split()) >= min_action_words
    ]
    if class_policy["requires_downstream_actions"] and not substantive_actions:
        errors.append(f"{classification} requires substantive downstream actions")

    if delta.get("risk") == "R3":
        requirement = policy.get("risk_requirements", {}).get("R3", {})
        if requirement.get("requires_downstream_actions") and not substantive_actions:
            errors.append("R3 delta requires at least one substantive downstream action")

    if delta.get("event") == "REMOVED":
        allowed = set(policy["removed_allowed_classifications"])
        if classification not in allowed:
            errors.append(
                "removed source requires one of: " + ", ".join(sorted(allowed))
            )
        if live_ids:
            live_allowed = set(policy["removed_live_allowed_classifications"])
            if classification not in live_allowed:
                errors.append(
                    "removed source supporting live evidence requires one of: "
                    + ", ".join(sorted(live_allowed))
                )
        resolution_policy = policy.get("removed_allowed_resolutions", {})
        allowed_resolutions = set(resolution_policy.get(classification, []))
        if allowed_resolutions and resolution not in allowed_resolutions:
            errors.append(
                f"removed source classified {classification} requires resolution: "
                + ", ".join(sorted(allowed_resolutions))
            )

    if classification == "FALSIFY" and resolution == "superseded":
        replacements = delta.get("replacement_evidence_ids", [])
        affected_ids = {item.get("id") for item in delta.get("affected_evidence", [])}
        if not replacements:
            errors.append("FALSIFY supersession requires replacement evidence")
        else:
            reused = sorted(set(replacements) & affected_ids)
            if reused:
                errors.append(
                    "replacement evidence must be distinct from falsified/affected evidence: "
                    + ", ".join(reused)
                )
            if head_evidence_ids is not None:
                missing = sorted(set(replacements) - head_evidence_ids)
                if missing:
                    errors.append(
                        "replacement evidence does not exist in head ledger: "
                        + ", ".join(missing)
                    )
            if head_evidence_statuses is not None:
                nonlive = sorted(
                    replacement
                    for replacement in replacements
                    if head_evidence_statuses.get(replacement) not in live_statuses
                )
                if nonlive:
                    errors.append(
                        "replacement evidence must be verified or active at head: "
                        + ", ".join(nonlive)
                    )
        baseline_live = {
            item.get("id")
            for item in delta.get("affected_evidence", [])
            if item.get("baseline_status") in live_statuses
        }
        head_nonlive = {
            item.get("id")
            for item in delta.get("affected_evidence", [])
            if item.get("head_status") not in live_statuses
        }
        if baseline_live and not (baseline_live & head_nonlive):
            errors.append(
                "FALSIFY supersession must move at least one previously live affected evidence record out of live status"
            )

    return errors


def recompute_gate(
    delta: dict[str, Any],
    policy: dict[str, Any],
    head_evidence_ids: set[str] | None = None,
    head_evidence_statuses: dict[str, str] | None = None,
) -> None:
    delta["promotion_gate"] = (
        "READY"
        if not readiness_errors(
            delta, policy, head_evidence_ids, head_evidence_statuses
        )
        else "BLOCKED"
    )


def apply_assessment(report: dict[str, Any], assessment: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(report)
    source_id = assessment.get("source_id")
    matching = [d for d in result.get("deltas", []) if d.get("source_id") == source_id]
    if len(matching) != 1:
        raise ValueError(f"assessment source_id must match exactly one delta: {source_id}")

    delta = matching[0]
    allowed = {
        "classification",
        "rationale",
        "reviewed_evidence_ids",
        "downstream_actions",
        "resolution",
        "replacement_evidence_ids",
        "decision_record",
    }
    unexpected = sorted(set(assessment) - allowed - {"source_id"})
    if unexpected:
        raise ValueError("unexpected assessment fields: " + ", ".join(unexpected))
    for key in allowed:
        if key in assessment:
            delta[key] = assessment[key]

    recompute_gate(
        delta,
        load_policy(),
        set(result.get("head_evidence_ids", [])),
        result.get("head_evidence_statuses", {}),
    )
    return result


def duplicate_values(values: list[Any]) -> bool:
    return len(values) != len(set(values))


def schema_validation_errors(report: dict[str, Any]) -> list[str]:
    schema = json.loads(SCHEMA_PATH.read_text())
    validator = Draft7Validator(schema)
    errors = []
    for error in sorted(validator.iter_errors(report), key=lambda item: list(item.absolute_path)):
        location = ".".join(str(part) for part in error.absolute_path) or "<root>"
        errors.append(f"schema {location}: {error.message}")
    return errors


def validate_report(report: dict[str, Any], *, require_ready: bool = False) -> list[str]:
    policy = load_policy()
    errors: list[str] = schema_validation_errors(report)
    allowed_top = {"version", "base_ref", "head_ref", "hashes", "head_evidence_ids", "head_evidence_statuses", "deltas"}
    extra_top = sorted(set(report) - allowed_top)
    if extra_top:
        errors.append("unexpected top-level fields: " + ", ".join(extra_top))
    if report.get("version") != "1.0.0":
        errors.append("report version must be 1.0.0")
    if not isinstance(report.get("base_ref"), str) or not SHA_RE.fullmatch(report.get("base_ref", "")):
        errors.append("base_ref must be a resolved commit SHA")
    if not isinstance(report.get("head_ref"), str) or not SHA_RE.fullmatch(report.get("head_ref", "")):
        errors.append("head_ref must be a resolved commit SHA")

    expected_hash_keys = {
        "base_registry_sha256",
        "head_registry_sha256",
        "base_evidence_ledger_sha256",
        "head_evidence_ledger_sha256",
    }
    hashes = report.get("hashes")
    if not isinstance(hashes, dict):
        errors.append("hashes must be an object")
        hashes = {}
    if set(hashes) != expected_hash_keys:
        errors.append("hash keys must match the source delta schema")
    for key in expected_hash_keys:
        value = hashes.get(key, "")
        if not isinstance(value, str) or len(value) != 64 or any(c not in "0123456789abcdef" for c in value):
            errors.append(f"invalid SHA-256: {key}")

    head_evidence_ids = report.get("head_evidence_ids")
    if not isinstance(head_evidence_ids, list) or not all(
        isinstance(item, str) and item for item in head_evidence_ids
    ):
        errors.append("head_evidence_ids must be an array of non-empty strings")
        head_evidence_ids = []
    elif duplicate_values(head_evidence_ids):
        errors.append("head_evidence_ids must contain unique values")

    head_evidence_statuses = report.get("head_evidence_statuses")
    if not isinstance(head_evidence_statuses, dict) or not all(
        isinstance(key, str) and key and isinstance(value, str)
        for key, value in (head_evidence_statuses or {}).items()
    ):
        errors.append("head_evidence_statuses must map evidence ids to string statuses")
        head_evidence_statuses = {}
    if set(head_evidence_statuses) != set(head_evidence_ids):
        errors.append("head_evidence_statuses keys must equal head_evidence_ids")

    deltas = report.get("deltas")
    if not isinstance(deltas, list):
        return errors + ["deltas must be an array"]
    ids = [d.get("id") for d in deltas if isinstance(d, dict)]
    if duplicate_values(ids):
        errors.append("duplicate delta ids")

    valid_events = {"ADDED", "REMOVED", "CHANGED"}
    valid_risks = {"R1", "R2", "R3"}
    valid_resolutions = {"pending", "accepted", "scoped", "superseded", "rejected", "no-action"}
    valid_gates = {"BLOCKED", "READY"}
    required_delta_fields = {
        "id", "source_id", "event", "risk", "change_dimensions", "changed_fields",
        "before", "after", "affected_evidence", "downstream_refs", "classification",
        "rationale", "reviewed_evidence_ids", "downstream_actions", "resolution",
        "replacement_evidence_ids", "decision_record", "promotion_gate",
    }

    for delta in deltas:
        if not isinstance(delta, dict):
            errors.append("delta entries must be objects")
            continue
        missing = sorted(required_delta_fields - set(delta))
        extra = sorted(set(delta) - required_delta_fields)
        if missing:
            errors.append(f"{delta.get('id', '<unknown>')}: missing fields: {', '.join(missing)}")
            continue
        if extra:
            errors.append(f"{delta.get('id')}: unexpected fields: {', '.join(extra)}")

        delta_id = delta.get("id")
        source_id = delta.get("source_id")
        if not isinstance(delta_id, str) or not DELTA_ID_RE.fullmatch(delta_id):
            errors.append(f"{delta_id}: invalid delta id")
        if not isinstance(source_id, str) or not source_id:
            errors.append(f"{delta_id}: source_id is required")
        if delta_id != f"SDL-{source_id}":
            errors.append(f"{delta_id}: expected id SDL-{source_id}")
        if delta.get("event") not in valid_events:
            errors.append(f"{delta_id}: invalid event")
        if delta.get("risk") not in valid_risks:
            errors.append(f"{delta_id}: invalid risk")
        if delta.get("classification") not in policy["classifications"]:
            errors.append(f"{delta_id}: invalid classification")
        if delta.get("resolution") not in valid_resolutions:
            errors.append(f"{delta_id}: invalid resolution")
        if delta.get("promotion_gate") not in valid_gates:
            errors.append(f"{delta_id}: invalid promotion_gate")
        if delta.get("before") is not None and not isinstance(delta.get("before"), dict):
            errors.append(f"{delta_id}: before must be object or null")
        if delta.get("after") is not None and not isinstance(delta.get("after"), dict):
            errors.append(f"{delta_id}: after must be object or null")
        if not isinstance(delta.get("rationale"), str):
            errors.append(f"{delta_id}: rationale must be a string")
        decision_record = delta.get("decision_record")
        if decision_record is not None:
            if not isinstance(decision_record, str) or not DECISION_PATH_RE.fullmatch(decision_record):
                errors.append(
                    f"{delta_id}: decision_record must be a concrete 03-decisions/<TYPE>-NNN.(json|md) path"
                )

        for list_key in (
            "change_dimensions",
            "changed_fields",
            "downstream_refs",
            "reviewed_evidence_ids",
            "replacement_evidence_ids",
        ):
            value = delta.get(list_key)
            if not isinstance(value, list):
                errors.append(f"{delta_id}: {list_key} must be an array")
            elif duplicate_values(value):
                errors.append(f"{delta_id}: {list_key} must contain unique values")
        actions = delta.get("downstream_actions")
        min_action_chars = policy["min_downstream_action_chars"]
        if not isinstance(actions, list) or not all(
            isinstance(x, str)
            and x == x.strip()
            and len(x) >= min_action_chars
            for x in actions
        ):
            errors.append(
                f"{delta_id}: downstream_actions must contain trimmed strings of at least "
                f"{min_action_chars} characters"
            )

        affected = delta.get("affected_evidence")
        if not isinstance(affected, list):
            errors.append(f"{delta_id}: affected_evidence must be an array")
            affected = []
        affected_ids = set()
        required_affected = {
            "id", "baseline_status", "head_status", "strength", "scope",
            "baseline_cites", "head_cites",
        }
        for item in affected:
            if not isinstance(item, dict) or set(item) != required_affected:
                errors.append(f"{delta_id}: malformed affected evidence")
                continue
            affected_ids.add(item["id"])
            if not isinstance(item["baseline_cites"], bool) or not isinstance(item["head_cites"], bool):
                errors.append(f"{delta_id}: citation flags must be boolean")
        reviewed = delta.get("reviewed_evidence_ids")
        if isinstance(reviewed, list) and not set(reviewed) <= affected_ids:
            errors.append(f"{delta_id}: reviewed_evidence_ids must be a subset of affected evidence")
        replacements = delta.get("replacement_evidence_ids")
        if isinstance(replacements, list):
            missing_replacements = sorted(set(replacements) - set(head_evidence_ids))
            if missing_replacements:
                errors.append(
                    f"{delta_id}: replacement evidence does not exist in head ledger: "
                    + ", ".join(missing_replacements)
                )

        local = readiness_errors(
            delta,
            policy,
            set(head_evidence_ids),
            head_evidence_statuses,
        )
        expected_gate = "READY" if not local else "BLOCKED"
        if delta.get("promotion_gate") != expected_gate:
            errors.append(f"{delta_id}: promotion_gate must be {expected_gate}")
        if require_ready and expected_gate != "READY":
            errors.append(f"{delta_id}: not READY: {'; '.join(local)}")

    return errors


def resolve_commit(ref: str) -> str:
    if not isinstance(ref, str) or not ref or ref.startswith("-"):
        raise RuntimeError(f"invalid Git ref: {ref!r}")
    try:
        raw = subprocess.check_output(
            ["git", "rev-parse", "--verify", "--end-of-options", f"{ref}^{{commit}}"],
            cwd=ROOT,
            stderr=subprocess.STDOUT,
        )
    except subprocess.CalledProcessError as exc:
        raise RuntimeError(f"cannot resolve Git ref: {ref}") from exc
    commit = raw.decode().strip()
    if not SHA_RE.fullmatch(commit):
        raise RuntimeError(f"Git ref did not resolve to a commit SHA: {ref}")
    return commit


def git_file(commit: str, rel: str) -> bytes:
    if not SHA_RE.fullmatch(commit):
        raise RuntimeError(f"unsafe or invalid commit SHA: {commit}")
    try:
        return subprocess.check_output(
            ["git", "show", "--no-ext-diff", f"{commit}:{rel}"],
            cwd=ROOT,
            stderr=subprocess.STDOUT,
        )
    except subprocess.CalledProcessError as exc:
        raise RuntimeError(f"cannot read {rel} at {commit}") from exc


def downstream_refs_for_git(evidence_ids: list[str], commit: str) -> list[str]:
    if not evidence_ids:
        return []
    if not SHA_RE.fullmatch(commit):
        raise RuntimeError(f"unsafe or invalid commit SHA: {commit}")

    # Git grep is only a candidate-path accelerator. Its word-boundary rules do
    # not treat '-' the same way as our evidence-ID grammar, so every candidate
    # is re-read and filtered through exact_evidence_match().
    args = ["git", "grep", "-l", "-F"]
    for evidence_id in evidence_ids:
        args.extend(["-e", evidence_id])
    args.extend([commit, "--", "*.md", "*.json", "*.py", "*.yml", "*.yaml"])
    proc = subprocess.run(args, cwd=ROOT, capture_output=True, text=True)
    if proc.returncode not in (0, 1):
        raise RuntimeError(f"git grep failed for {commit}: {proc.stderr.strip()}")

    refs = set()
    prefix = commit + ":"
    for line in proc.stdout.splitlines():
        rel = line[len(prefix):] if line.startswith(prefix) else line.split(":", 1)[-1]
        if excluded_downstream_path(rel):
            continue
        text = git_file(commit, rel).decode("utf-8", errors="ignore")
        if any(exact_evidence_match(text, evidence_id) for evidence_id in evidence_ids):
            refs.add(rel)
    return sorted(refs)


def detect_git(base_ref: str, head_ref: str) -> dict[str, Any]:
    base_commit = resolve_commit(base_ref)
    head_commit = resolve_commit(head_ref)
    base_raw = git_file(base_commit, REGISTRY_PATH)
    head_raw = git_file(head_commit, REGISTRY_PATH)
    base_evidence_raw = git_file(base_commit, EVIDENCE_PATH)
    head_evidence_raw = git_file(head_commit, EVIDENCE_PATH)
    return detect_from_documents(
        load_json_bytes(base_raw),
        load_json_bytes(head_raw),
        load_json_bytes(head_evidence_raw),
        base_ledger=load_json_bytes(base_evidence_raw),
        base_ref=base_commit,
        head_ref=head_commit,
        hashes={
            "base_registry_sha256": sha256(base_raw),
            "head_registry_sha256": sha256(head_raw),
            "base_evidence_ledger_sha256": sha256(base_evidence_raw),
            "head_evidence_ledger_sha256": sha256(head_evidence_raw),
        },
        downstream_resolver=lambda ids: downstream_refs_for_git(ids, head_commit),
    )


def reference_integrity_errors(report: dict[str, Any], head_commit: str) -> list[str]:
    errors = []
    try:
        head_ledger = load_json_bytes(git_file(head_commit, EVIDENCE_PATH))
    except RuntimeError as exc:
        return [str(exc)]
    evidence_ids = {item.get("id") for item in evidence_items(head_ledger)}

    for delta in report.get("deltas", []):
        if not isinstance(delta, dict):
            continue
        delta_id = delta.get("id", "<unknown>")
        missing_replacements = sorted(
            replacement_id
            for replacement_id in delta.get("replacement_evidence_ids", [])
            if replacement_id not in evidence_ids
        )
        if missing_replacements:
            errors.append(
                f"{delta_id}: replacement evidence does not exist in head ledger: "
                + ", ".join(missing_replacements)
            )

        decision_record = delta.get("decision_record")
        if decision_record:
            if not isinstance(decision_record, str) or not DECISION_PATH_RE.fullmatch(decision_record):
                errors.append(f"{delta_id}: invalid decision-record path")
            else:
                try:
                    git_file(head_commit, decision_record)
                except RuntimeError:
                    errors.append(f"{delta_id}: decision record does not exist at head: {decision_record}")

    return errors


def commit_available(commit: str) -> bool:
    if not isinstance(commit, str) or not SHA_RE.fullmatch(commit):
        return False
    proc = subprocess.run(
        ["git", "cat-file", "-e", f"{commit}^{{commit}}"],
        cwd=ROOT,
        capture_output=True,
    )
    return proc.returncode == 0


def provenance_errors(report: dict[str, Any]) -> list[str]:
    errors = []
    base_commit = report.get("base_ref", "")
    head_commit = report.get("head_ref", "")
    if not SHA_RE.fullmatch(base_commit or "") or not SHA_RE.fullmatch(head_commit or ""):
        return ["base_ref and head_ref must be resolved commit SHAs for provenance verification"]
    try:
        base_raw = git_file(base_commit, REGISTRY_PATH)
        head_raw = git_file(head_commit, REGISTRY_PATH)
        base_evidence_raw = git_file(base_commit, EVIDENCE_PATH)
        head_evidence_raw = git_file(head_commit, EVIDENCE_PATH)
    except RuntimeError as exc:
        return [str(exc)]

    expected_hashes = {
        "base_registry_sha256": sha256(base_raw),
        "head_registry_sha256": sha256(head_raw),
        "base_evidence_ledger_sha256": sha256(base_evidence_raw),
        "head_evidence_ledger_sha256": sha256(head_evidence_raw),
    }
    if report.get("hashes") != expected_hashes:
        errors.append("stored provenance hashes do not match referenced Git inputs")

    expected = detect_from_documents(
        load_json_bytes(base_raw),
        load_json_bytes(head_raw),
        load_json_bytes(head_evidence_raw),
        base_ledger=load_json_bytes(base_evidence_raw),
        base_ref=base_commit,
        head_ref=head_commit,
        hashes=expected_hashes,
        downstream_resolver=lambda ids: downstream_refs_for_git(ids, head_commit),
    )
    immutable = (
        "id", "source_id", "event", "risk", "change_dimensions", "changed_fields",
        "before", "after", "affected_evidence", "downstream_refs",
    )
    actual_by_id = {d.get("id"): d for d in report.get("deltas", []) if isinstance(d, dict)}
    expected_by_id = {d.get("id"): d for d in expected.get("deltas", [])}
    if set(actual_by_id) != set(expected_by_id):
        errors.append("delta id set does not match referenced Git inputs")
        return errors
    for delta_id, expected_delta in expected_by_id.items():
        actual = actual_by_id[delta_id]
        for key in immutable:
            if actual.get(key) != expected_delta.get(key):
                errors.append(f"{delta_id}: immutable detected field changed: {key}")
    errors.extend(reference_integrity_errors(report, head_commit))
    return errors


def report_matches_detected(candidate: dict[str, Any], detected: dict[str, Any]) -> bool:
    if candidate.get("hashes") != detected.get("hashes"):
        return False
    if candidate.get("head_evidence_ids") != detected.get("head_evidence_ids"):
        return False
    if candidate.get("head_evidence_statuses") != detected.get("head_evidence_statuses"):
        return False
    # downstream_refs are a point-in-time review snapshot, not part of the
    # authorization key. Later docs/code may add consumers without changing
    # the source/evidence state that the report assessed.
    immutable = (
        "id", "source_id", "event", "risk", "change_dimensions", "changed_fields",
        "before", "after", "affected_evidence",
    )
    candidate_map = {d.get("id"): d for d in candidate.get("deltas", []) if isinstance(d, dict)}
    detected_map = {d.get("id"): d for d in detected.get("deltas", []) if isinstance(d, dict)}
    if set(candidate_map) != set(detected_map):
        return False
    return all(
        all(candidate_map[delta_id].get(key) == detected_delta.get(key) for key in immutable)
        for delta_id, detected_delta in detected_map.items()
    )


def gate_reports(
    base_ref: str,
    head_ref: str,
    reports_dir: Path = REPORTS_DIR,
    *,
    allow_unreachable_report_refs: bool = False,
) -> list[str]:
    detected = detect_git(base_ref, head_ref)
    if not detected["deltas"]:
        return []

    if not reports_dir.exists():
        return [f"source deltas detected but reports directory is missing: {reports_dir}"]

    failures = []
    matching_ready = []
    for path in sorted(reports_dir.glob("*.json")):
        try:
            candidate = json.loads(path.read_text())
        except Exception as exc:
            failures.append(f"{path.name}: invalid JSON: {exc}")
            continue
        if not report_matches_detected(candidate, detected):
            continue
        errors = validate_report(candidate, require_ready=True)
        errors.extend(reference_integrity_errors(candidate, detected["head_ref"]))

        base_available = commit_available(candidate.get("base_ref", ""))
        head_available = commit_available(candidate.get("head_ref", ""))
        if base_available and head_available:
            errors.extend(provenance_errors(candidate))
        elif not allow_unreachable_report_refs:
            errors.append("report provenance commits are not reachable in this checkout")

        if errors:
            failures.append(f"{path.name}: " + "; ".join(errors))
        else:
            matching_ready.append(path.name)

    if matching_ready:
        return []
    details = " | ".join(failures) if failures else "no report matches the current source/evidence hashes"
    return [
        "source deltas are not covered by a READY committed assessment report: " + details
    ]


def write_output(data: dict[str, Any], output: str | None) -> None:
    text = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
    if output:
        Path(output).write_text(text)
    else:
        print(text, end="")


def main() -> int:
    parser = argparse.ArgumentParser(description="Detect, assess, validate and gate PEOS source deltas")
    sub = parser.add_subparsers(dest="command", required=True)

    detect = sub.add_parser("detect")
    detect.add_argument("--base-ref", required=True)
    detect.add_argument("--head-ref", required=True)
    detect.add_argument("--output")

    assess = sub.add_parser("assess")
    assess.add_argument("--report", required=True)
    assess.add_argument("--assessment", required=True)
    assess.add_argument("--output")

    validate = sub.add_parser("validate")
    validate.add_argument("--report", required=True)
    validate.add_argument("--require-ready", action="store_true")
    validate.add_argument("--verify-refs", action="store_true")

    gate = sub.add_parser("gate")
    gate.add_argument("--base-ref", required=True)
    gate.add_argument("--head-ref", required=True)
    gate.add_argument("--reports-dir", default=str(REPORTS_DIR))
    gate.add_argument("--allow-unreachable-report-refs", action="store_true")

    args = parser.parse_args()

    if args.command == "detect":
        report = detect_git(args.base_ref, args.head_ref)
        write_output(report, args.output)
        return 0

    if args.command == "assess":
        report = json.loads(Path(args.report).read_text())
        provenance = provenance_errors(report)
        if provenance:
            for error in provenance:
                print("ERROR:", error, file=sys.stderr)
            return 1
        assessment = json.loads(Path(args.assessment).read_text())
        result = apply_assessment(report, assessment)
        errors = validate_report(result)
        errors.extend(reference_integrity_errors(result, result["head_ref"]))
        if errors:
            for error in errors:
                print("ERROR:", error, file=sys.stderr)
            return 1
        write_output(result, args.output)
        return 0

    if args.command == "gate":
        errors = gate_reports(
            args.base_ref,
            args.head_ref,
            Path(args.reports_dir),
            allow_unreachable_report_refs=args.allow_unreachable_report_refs,
        )
        if errors:
            print("FAIL source delta gate")
            for error in errors:
                print("-", error)
            return 1
        print("PASS source delta gate")
        return 0

    report = json.loads(Path(args.report).read_text())
    errors = validate_report(report, require_ready=args.require_ready)
    if args.verify_refs or args.require_ready:
        errors.extend(provenance_errors(report))
    if errors:
        print("FAIL source delta report")
        for error in errors:
            print("-", error)
        return 1
    ready = sum(d.get("promotion_gate") == "READY" for d in report.get("deltas", []))
    blocked = sum(d.get("promotion_gate") == "BLOCKED" for d in report.get("deltas", []))
    print(f"PASS source delta report: READY={ready} BLOCKED={blocked}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
