#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft7Validator

ROOT = Path(__file__).resolve().parents[1]
POLICY_PATH = ROOT / "machine" / "memory-knowledge-policy.json"
SCHEMA_PATH = ROOT / "01-governance" / "memory-knowledge.schema.json"

EXIT_READY = 0
EXIT_INVALID = 2
EXIT_NOT_READY = 3


class ContractError(ValueError):
    pass


def _reject_duplicate_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ContractError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=_reject_duplicate_pairs,
    )


def _validate_unicode_tree(value: Any) -> None:
    stack: list[tuple[str, Any]] = [("<root>", value)]
    while stack:
        path, current = stack.pop()
        if isinstance(current, str):
            try:
                current.encode("utf-8")
            except UnicodeEncodeError as exc:
                raise ContractError(f"{path}: invalid Unicode scalar value") from exc
        elif isinstance(current, dict):
            for key, child in current.items():
                stack.append((f"{path}.{key}", child))
        elif isinstance(current, list):
            for index, child in enumerate(current):
                stack.append((f"{path}[{index}]", child))


def _semantic_validate(record: dict[str, Any], policy: dict[str, Any]) -> None:
    refs = record["canonical_refs"]
    relation = record["canonical_relation"]

    if relation == "NONE" and refs:
        raise ContractError("canonical_refs require an assessed canonical_relation")
    if relation != "NONE" and not refs:
        raise ContractError(f"{relation} requires at least one canonical_ref")
    if record["promotion_requested"] and not record.get("promotion_target"):
        raise ContractError("promotion_requested requires promotion_target")
    if record.get("promotion_target") and not record["promotion_requested"]:
        raise ContractError("promotion_target is only valid when promotion_requested=true")
    if not record["promotion_requested"]:
        stray = [
            key
            for key in ("promotion_scope", "promotion_provenance_refs", "changes_active_guidance")
            if key in record
        ]
        if stray:
            raise ContractError(
                "promotion fields require promotion_requested=true: " + ", ".join(stray)
            )
    if record["current_user_explicit"] and record["memory_class"] != "CURRENT_INPUT":
        raise ContractError("current_user_explicit requires memory_class=CURRENT_INPUT")

    is_user_intent = record["claim_class"] == "USER_INTENT"
    current_intent = (
        is_user_intent
        and record["current_user_explicit"]
        and record["memory_class"] == "CURRENT_INPUT"
    )
    if is_user_intent and record["memory_class"] == "CURRENT_INPUT" and not record["current_user_explicit"]:
        raise ContractError(
            "USER_INTENT from CURRENT_INPUT requires current_user_explicit=true"
        )
    if current_intent and relation != "NONE":
        raise ContractError(
            "current explicit USER_INTENT is not arbitrated by canonical_relation; "
            "verify attached project facts as separate claims"
        )
    if (
        is_user_intent
        and record["promotion_requested"]
        and record.get("promotion_target") == "KNOWLEDGE_BASE"
    ):
        raise ContractError(
            "USER_INTENT may be persisted project-locally but cannot directly "
            "promote to KNOWLEDGE_BASE; create a separate corroborated reusable claim"
        )
    if (
        record["promotion_requested"]
        and record.get("promotion_target") == "PROJECT_REPOSITORY"
        and record.get("changes_active_guidance") is True
    ):
        raise ContractError(
            "changes_active_guidance=true is incompatible with PROJECT_REPOSITORY promotion"
        )

    for key, allowed_key in [
        ("memory_class", "memory_classes"),
        ("claim_class", "claim_classes"),
        ("canonical_relation", "canonical_relations"),
        ("risk", "risk_levels"),
    ]:
        if record[key] not in policy[allowed_key]:
            raise ContractError(f"{key} is outside policy: {record[key]}")

    target = record.get("promotion_target")
    if target is not None and target not in policy["promotion_targets"]:
        raise ContractError(f"promotion_target is outside policy: {target}")

    allowed_schemes = set(policy.get("canonical_reference_schemes", []))
    if allowed_schemes:
        for ref in refs:
            scheme = ref.split("://", 1)[0]
            if scheme not in allowed_schemes:
                raise ContractError(f"canonical_ref scheme is not canonical: {scheme}")


def validate_record(
    record: dict[str, Any],
    *,
    policy: dict[str, Any] | None = None,
    schema: dict[str, Any] | None = None,
) -> None:
    policy = policy or _load_json(POLICY_PATH)
    schema = schema or _load_json(SCHEMA_PATH)

    _validate_unicode_tree(record)
    errors = sorted(Draft7Validator(schema).iter_errors(record), key=lambda e: list(e.path))
    if errors:
        rendered = "; ".join(
            f"{'.'.join(map(str, err.path)) or '<root>'}: {err.message}" for err in errors
        )
        raise ContractError(rendered)

    _semantic_validate(record, policy)


def _promotion_state(
    record: dict[str, Any],
    status: str,
) -> tuple[str, list[str], list[str], bool | str]:
    if not record["promotion_requested"]:
        return "NOT_REQUESTED", [], [], False

    target = record["promotion_target"]
    missing: list[str] = []
    scope = (record.get("promotion_scope") or "").strip()
    provenance = record.get("promotion_provenance_refs") or []

    if not scope:
        missing.append("promotion_scope")
    if not provenance:
        missing.append("promotion_provenance_refs")

    if target == "KNOWLEDGE_BASE":
        active_change = record.get("changes_active_guidance")
        source_delta_required: bool | str = (
            True if active_change is True else False if active_change is False else "UNKNOWN"
        )
        if active_change is None:
            missing.append("changes_active_guidance")
        if record["canonical_relation"] != "SUPPORTS":
            missing.append("canonical_support")
    else:
        source_delta_required = False

    if status == "BLOCKED":
        return "BLOCKED", [
            "Resolve the blocking conflict or missing material evidence before any promotion.",
            "Do not persist the blocked remembered claim as canonical knowledge.",
        ], missing, source_delta_required

    if status in {"VERIFY_REQUIRED", "PROMOTION_REQUIRED", "CONTEXT_ONLY"} or missing:
        actions = [
            "Promotion is not ready; recover/verify required evidence before writing canonical knowledge."
        ]
        if missing:
            actions.append("Missing promotion inputs: " + ", ".join(sorted(set(missing))) + ".")
        if status == "VERIFY_REQUIRED":
            actions.append("Verify the decision-relevant claim against the owning durable source first.")
        if source_delta_required == "UNKNOWN":
            actions.append(
                "Determine whether Active reusable guidance changes before promotion can proceed."
            )
        return "PENDING_EVIDENCE", actions, sorted(set(missing)), source_delta_required

    actions = [
        f"Promotion inputs are structurally ready for owner review in {target}.",
        "The owner must still validate semantic fidelity before writing the durable artifact.",
    ]
    if target == "KNOWLEDGE_BASE" and source_delta_required is True:
        actions.append("Run Source Delta before changing existing Active reusable guidance.")
    elif target == "PROJECT_REPOSITORY" and record["claim_class"] == "REUSABLE_GUIDANCE":
        actions.append(
            "Treat PROJECT_REPOSITORY promotion as project-local only; global reuse requires Knowledge Base governance."
        )
    return "READY_FOR_OWNER_REVIEW", actions, [], source_delta_required


def evaluate_record(
    record: dict[str, Any],
    *,
    policy: dict[str, Any] | None = None,
    schema: dict[str, Any] | None = None,
) -> dict[str, Any]:
    policy = policy or _load_json(POLICY_PATH)
    validate_record(record, policy=policy, schema=schema)

    relation = record["canonical_relation"]
    risk = record["risk"]
    claim_class = record["claim_class"]
    decision_use = record["decision_use"]
    current_intent = (
        claim_class == "USER_INTENT"
        and record["current_user_explicit"]
        and record["memory_class"] == "CURRENT_INPUT"
    )

    reasons: list[str] = []
    actions: list[str] = []

    if current_intent:
        status = "DECISION_READY"
        reasons.append("Latest explicit current input is authoritative for user intent and requested scope.")
        actions.extend([
            "Use this authority only for intent/scope; verify attached objective project facts separately.",
            "Decision-ready intent does not authorize a consequential tool action or bypass approval.",
        ])
    elif relation in {"CONFLICTS", "SUPERSEDES_MEMORY"}:
        status = "BLOCKED"
        reasons.append("Canonical evidence conflicts with or supersedes the remembered claim.")
        actions.extend([
            "Inspect scope, date/environment and authority before resolving the conflict.",
            "Do not silently prefer memory over canonical evidence.",
        ])
    elif decision_use and risk in set(policy["material_risks"]) and relation == "NONE":
        status = "BLOCKED"
        reasons.append("A material-risk decision cannot rely on unsupported remembered project context.")
        actions.append("Resolve current canonical evidence before progressing the decision.")
    elif relation == "SUPPORTS":
        status = "DECISION_READY"
        reasons.append("The remembered claim is corroborated by declared canonical evidence.")
        actions.append("Keep the canonical references attached to the decision or handoff.")
    elif decision_use:
        status = "VERIFY_REQUIRED"
        reasons.append("The claim affects a decision but has no corroborating canonical evidence.")
        actions.append("Use memory as a locator and verify the claim against the owning durable source.")
    elif record["promotion_requested"]:
        status = "PROMOTION_REQUIRED"
        reasons.append("Remembered context cannot become durable policy or project truth by repetition.")
    else:
        status = "CONTEXT_ONLY"
        reasons.append("The claim is not being used as a decision premise and may remain labeled context.")
        actions.append("Re-evaluate if the claim becomes decision-relevant.")

    promotion_gate, promotion_actions, missing_inputs, source_delta_required = _promotion_state(
        record, status
    )
    actions.extend(promotion_actions)

    if status not in set(policy["statuses"]):
        raise ContractError(f"computed status is outside policy: {status}")
    if promotion_gate not in set(policy["promotion_gates"]):
        raise ContractError(f"computed promotion_gate is outside policy: {promotion_gate}")

    authority_scope = (
        "USER_INTENT_ONLY"
        if current_intent and status == "DECISION_READY"
        else "CANONICAL_CLAIM"
        if relation == "SUPPORTS" and status == "DECISION_READY"
        else "NONE"
    )
    if authority_scope not in set(policy.get("authority_scopes", [])):
        raise ContractError(f"computed authority_scope is outside policy: {authority_scope}")

    return {
        "id": record["id"],
        "status": status,
        "claim_admissible_for_decision": status == "DECISION_READY",
        "authority_scope": authority_scope,
        "action_authorized": False,
        "promotion_gate": promotion_gate,
        "promotion_target": record.get("promotion_target"),
        "promotion_scope": record.get("promotion_scope"),
        "promotion_provenance_refs": record.get("promotion_provenance_refs", []),
        "missing_promotion_inputs": missing_inputs,
        "source_delta_required": source_delta_required,
        "claim_class": claim_class,
        "risk": risk,
        "canonical_refs": record["canonical_refs"],
        "reasons": reasons,
        "required_actions": actions,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate a remembered claim against the PEOS Memory ↔ Knowledge Base Contract."
    )
    sub = parser.add_subparsers(dest="command", required=True)
    check = sub.add_parser("check")
    check.add_argument("input", type=Path)
    check.add_argument("--compact", action="store_true")
    args = parser.parse_args()

    try:
        record = _load_json(args.input)
        result = evaluate_record(record)
        rendered = json.dumps(result, ensure_ascii=True, indent=None if args.compact else 2)
    except (OSError, UnicodeError, json.JSONDecodeError, ContractError, RecursionError) as exc:
        rendered = json.dumps({"status": "INVALID", "error": str(exc)}, ensure_ascii=True)
        print(rendered)
        return EXIT_INVALID

    print(rendered)
    claim_ready = result["status"] == "DECISION_READY"
    promotion_ready = result["promotion_gate"] in {"NOT_REQUESTED", "READY_FOR_OWNER_REVIEW"}
    return EXIT_READY if claim_ready and promotion_ready else EXIT_NOT_READY


if __name__ == "__main__":
    raise SystemExit(main())
