import copy
import json
from pathlib import Path
import subprocess
import sys

import pytest

from scripts.memory_knowledge_guard import ContractError, evaluate_record, validate_record


BASE = {
    "version": "1.0.0",
    "id": "MKC-TEST-001",
    "claim": "The current production deployment uses commit abc.",
    "claim_class": "PROJECT_FACT",
    "memory_class": "RETRIEVED_MEMORY",
    "risk": "R2",
    "decision_use": True,
    "current_user_explicit": False,
    "canonical_relation": "NONE",
    "canonical_refs": [],
    "promotion_requested": False,
}


def record(**overrides):
    value = copy.deepcopy(BASE)
    value.update(overrides)
    return value


def run_cli(tmp_path, payload):
    path = tmp_path / "claim.json"
    path.write_text(json.dumps(payload))
    return subprocess.run(
        [sys.executable, "scripts/memory_knowledge_guard.py", "check", str(path), "--compact"],
        capture_output=True,
        text=True,
        check=False,
    )


def test_remembered_project_fact_requires_verification_for_decision():
    result = evaluate_record(record())
    assert result["status"] == "VERIFY_REQUIRED"
    assert result["claim_admissible_for_decision"] is False


@pytest.mark.parametrize("risk", ["R3", "R4"])
def test_material_risk_unsupported_memory_fails_closed(risk):
    result = evaluate_record(record(risk=risk))
    assert result["status"] == "BLOCKED"
    assert result["promotion_gate"] == "NOT_REQUESTED"


def test_canonical_support_makes_claim_decision_ready():
    result = evaluate_record(
        record(
            canonical_relation="SUPPORTS",
            canonical_refs=["project://git/main@abc123"],
        )
    )
    assert result["status"] == "DECISION_READY"
    assert result["claim_admissible_for_decision"] is True
    assert result["authority_scope"] == "CANONICAL_CLAIM"
    assert result["action_authorized"] is False


@pytest.mark.parametrize("relation", ["CONFLICTS", "SUPERSEDES_MEMORY"])
def test_canonical_conflict_blocks_memory(relation):
    result = evaluate_record(
        record(
            canonical_relation=relation,
            canonical_refs=["project://decision/ADR-042"],
        )
    )
    assert result["status"] == "BLOCKED"


@pytest.mark.parametrize("risk", ["R2", "R3", "R4"])
def test_current_explicit_user_intent_is_authoritative_for_intent_only(risk):
    result = evaluate_record(
        record(
            claim="Use PostgreSQL for the new prototype.",
            claim_class="USER_INTENT",
            memory_class="CURRENT_INPUT",
            current_user_explicit=True,
            risk=risk,
        )
    )
    assert result["status"] == "DECISION_READY"
    assert result["authority_scope"] == "USER_INTENT_ONLY"
    assert result["action_authorized"] is False
    assert any("does not authorize" in action for action in result["required_actions"])


def test_current_intent_cannot_be_arbitrated_by_repository_conflict():
    with pytest.raises(ContractError, match="not arbitrated"):
        validate_record(
            record(
                claim_class="USER_INTENT",
                memory_class="CURRENT_INPUT",
                current_user_explicit=True,
                canonical_relation="CONFLICTS",
                canonical_refs=["project://decision/ADR-042"],
            )
        )


def test_current_user_statement_does_not_make_project_fact_authoritative():
    result = evaluate_record(
        record(
            memory_class="CURRENT_INPUT",
            current_user_explicit=True,
            claim_class="PROJECT_FACT",
        )
    )
    assert result["status"] == "VERIFY_REQUIRED"


def test_non_decision_historical_memory_can_remain_context_only():
    result = evaluate_record(
        record(
            claim="A similar migration was discussed last quarter.",
            claim_class="HISTORICAL_CONTEXT",
            decision_use=False,
            risk="R4",
        )
    )
    assert result["status"] == "CONTEXT_ONLY"
    assert result["claim_admissible_for_decision"] is False


def test_promotion_requires_durable_evidence_inputs():
    result = evaluate_record(
        record(
            decision_use=False,
            promotion_requested=True,
            promotion_target="KNOWLEDGE_BASE",
        )
    )
    assert result["status"] == "PROMOTION_REQUIRED"
    assert result["promotion_gate"] == "PENDING_EVIDENCE"
    assert any("promotion_scope" in action for action in result["required_actions"])


def test_supported_promotion_with_scope_and_provenance_reaches_owner_review():
    result = evaluate_record(
        record(
            canonical_relation="SUPPORTS",
            canonical_refs=["project://decision/ADR-042"],
            promotion_requested=True,
            promotion_target="KNOWLEDGE_BASE",
            promotion_scope="Cross-project engineering guidance",
            promotion_provenance_refs=["evidence://EVD-042"],
            changes_active_guidance=True,
        )
    )
    assert result["status"] == "DECISION_READY"
    assert result["promotion_gate"] == "READY_FOR_OWNER_REVIEW"
    assert any("Source Delta" in action for action in result["required_actions"])


def test_blocked_conflict_never_gets_persist_action():
    result = evaluate_record(
        record(
            canonical_relation="CONFLICTS",
            canonical_refs=["project://decision/ADR-099"],
            promotion_requested=True,
            promotion_target="KNOWLEDGE_BASE",
            promotion_scope="Reusable guidance",
            promotion_provenance_refs=["evidence://EVD-099"],
        )
    )
    assert result["status"] == "BLOCKED"
    assert result["promotion_gate"] == "BLOCKED"
    assert not any("Persist" in action or "owner review" in action for action in result["required_actions"])
    assert any("Do not persist" in action for action in result["required_actions"])


def test_r3_decision_blocks_promotion_before_write():
    result = evaluate_record(
        record(
            risk="R3",
            promotion_requested=True,
            promotion_target="PROJECT_REPOSITORY",
            promotion_scope="Project-local decision",
            promotion_provenance_refs=["evidence://EVD-100"],
        )
    )
    assert result["status"] == "BLOCKED"
    assert result["promotion_gate"] == "BLOCKED"
    assert any("before any promotion" in action for action in result["required_actions"])


def test_low_risk_decision_verifies_before_promotion():
    result = evaluate_record(
        record(
            risk="R2",
            promotion_requested=True,
            promotion_target="PROJECT_REPOSITORY",
            promotion_scope="Project-local fact",
            promotion_provenance_refs=["evidence://EVD-101"],
        )
    )
    assert result["status"] == "VERIFY_REQUIRED"
    assert result["promotion_gate"] == "PENDING_EVIDENCE"
    assert any("Verify the decision-relevant claim" in action for action in result["required_actions"])


def test_reusable_guidance_promoted_locally_is_marked_project_local():
    result = evaluate_record(
        record(
            claim_class="REUSABLE_GUIDANCE",
            canonical_relation="SUPPORTS",
            canonical_refs=["knowledge://RULE-01"],
            promotion_requested=True,
            promotion_target="PROJECT_REPOSITORY",
            promotion_scope="One project override",
            promotion_provenance_refs=["evidence://EVD-102"],
        )
    )
    assert result["promotion_gate"] == "READY_FOR_OWNER_REVIEW"
    assert any("project-local only" in action for action in result["required_actions"])


def test_relation_requires_canonical_reference():
    with pytest.raises(ContractError, match="requires at least one canonical_ref"):
        validate_record(record(canonical_relation="SUPPORTS"))


def test_refs_without_relation_are_rejected():
    with pytest.raises(ContractError, match="canonical_refs require"):
        validate_record(record(canonical_refs=["project://README.md"]))


def test_non_uri_canonical_ref_is_rejected():
    with pytest.raises(ContractError):
        validate_record(
            record(
                canonical_relation="SUPPORTS",
                canonical_refs=["README.md"],
            )
        )


def test_current_user_explicit_requires_current_input():
    with pytest.raises(ContractError, match="CURRENT_INPUT"):
        validate_record(record(current_user_explicit=True))


def test_promotion_target_requires_request():
    with pytest.raises(ContractError, match="only valid"):
        validate_record(record(promotion_target="PROJECT_REPOSITORY"))


def test_promotion_request_requires_target():
    with pytest.raises(ContractError, match="requires promotion_target"):
        validate_record(record(promotion_requested=True))


def test_cli_ready_returns_zero(tmp_path):
    proc = run_cli(
        tmp_path,
        record(
            canonical_relation="SUPPORTS",
            canonical_refs=["project://decision/ADR-001"],
        ),
    )
    assert proc.returncode == 0
    assert json.loads(proc.stdout)["status"] == "DECISION_READY"


@pytest.mark.parametrize(
    "payload",
    [
        record(),
        record(risk="R3"),
        record(decision_use=False),
        record(
            decision_use=False,
            promotion_requested=True,
            promotion_target="KNOWLEDGE_BASE",
        ),
    ],
)
def test_cli_non_ready_states_return_three(tmp_path, payload):
    proc = run_cli(tmp_path, payload)
    assert proc.returncode == 3


def test_cli_invalid_json_returns_two(tmp_path):
    path = tmp_path / "invalid.json"
    path.write_bytes(b"\xff")
    proc = subprocess.run(
        [sys.executable, "scripts/memory_knowledge_guard.py", "check", str(path), "--compact"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 2
    assert json.loads(proc.stdout)["status"] == "INVALID"


def test_kb_promotion_with_unknown_active_guidance_is_pending():
    result = evaluate_record(
        record(
            claim_class="REUSABLE_GUIDANCE",
            canonical_relation="SUPPORTS",
            canonical_refs=["knowledge://RULE-UNKNOWN"],
            promotion_requested=True,
            promotion_target="KNOWLEDGE_BASE",
            promotion_scope="Cross-project guidance",
            promotion_provenance_refs=["evidence://EVD-UNKNOWN"],
        )
    )
    assert result["status"] == "DECISION_READY"
    assert result["promotion_gate"] == "PENDING_EVIDENCE"
    assert result["source_delta_required"] == "UNKNOWN"
    assert "changes_active_guidance" in result["missing_promotion_inputs"]


def test_current_user_intent_cannot_directly_promote_to_knowledge_base():
    with pytest.raises(ContractError, match="cannot directly promote"):
        evaluate_record(
            record(
                claim="Make this the global default.",
                claim_class="USER_INTENT",
                memory_class="CURRENT_INPUT",
                current_user_explicit=True,
                risk="R4",
                promotion_requested=True,
                promotion_target="KNOWLEDGE_BASE",
                promotion_scope="Global reusable guidance",
                promotion_provenance_refs=["chat://current/input"],
                changes_active_guidance=False,
            )
        )


def test_current_user_intent_can_be_persisted_project_locally_without_action_authority():
    result = evaluate_record(
        record(
            claim="Use this workflow in this project.",
            claim_class="USER_INTENT",
            memory_class="CURRENT_INPUT",
            current_user_explicit=True,
            risk="R4",
            promotion_requested=True,
            promotion_target="PROJECT_REPOSITORY",
            promotion_scope="Current project only",
            promotion_provenance_refs=["chat://current/input"],
        )
    )
    assert result["status"] == "DECISION_READY"
    assert result["promotion_gate"] == "READY_FOR_OWNER_REVIEW"
    assert result["authority_scope"] == "USER_INTENT_ONLY"
    assert result["action_authorized"] is False
    assert result["source_delta_required"] is False


def test_cli_escaped_lone_surrogate_is_invalid(tmp_path):
    payload = record(claim="\ud800")
    path = tmp_path / "surrogate.json"
    path.write_text(json.dumps(payload, ensure_ascii=True), encoding="utf-8")
    proc = subprocess.run(
        [sys.executable, "scripts/memory_knowledge_guard.py", "check", str(path), "--compact"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 2
    assert json.loads(proc.stdout)["status"] == "INVALID"
    assert "Traceback" not in proc.stderr


def test_cli_surrogate_in_canonical_ref_is_invalid(tmp_path):
    payload = record(
        canonical_relation="SUPPORTS",
        canonical_refs=["project://decision/\ud800"],
    )
    path = tmp_path / "surrogate-ref.json"
    path.write_text(json.dumps(payload, ensure_ascii=True), encoding="utf-8")
    proc = subprocess.run(
        [sys.executable, "scripts/memory_knowledge_guard.py", "check", str(path), "--compact"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 2
    assert json.loads(proc.stdout)["status"] == "INVALID"


def test_cli_deeply_nested_json_fails_closed_as_invalid(tmp_path):
    path = tmp_path / "deep.json"
    path.write_text("[" * 1500 + "0" + "]" * 1500, encoding="utf-8")
    proc = subprocess.run(
        [sys.executable, "scripts/memory_knowledge_guard.py", "check", str(path), "--compact"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 2
    assert json.loads(proc.stdout)["status"] == "INVALID"
    assert "Traceback" not in proc.stderr


@pytest.mark.parametrize(
    "field,value",
    [
        ("promotion_scope", "Unexpected scope"),
        ("promotion_provenance_refs", ["evidence://EVD-STRAY"]),
        ("changes_active_guidance", False),
    ],
)
def test_promotion_fields_require_promotion_request(field, value):
    with pytest.raises(ContractError, match="promotion fields require"):
        validate_record(record(**{field: value}))


def test_computed_status_must_exist_in_policy():
    policy = json.loads(Path("machine/memory-knowledge-policy.json").read_text())
    policy["statuses"].remove("VERIFY_REQUIRED")
    with pytest.raises(ContractError, match="computed status is outside policy"):
        evaluate_record(record(), policy=policy)


def test_computed_promotion_gate_must_exist_in_policy():
    policy = json.loads(Path("machine/memory-knowledge-policy.json").read_text())
    policy["promotion_gates"].remove("NOT_REQUESTED")
    with pytest.raises(ContractError, match="computed promotion_gate is outside policy"):
        evaluate_record(
            record(
                canonical_relation="SUPPORTS",
                canonical_refs=["project://decision/ADR-POLICY"],
            ),
            policy=policy,
        )


def test_current_input_user_intent_requires_explicit_flag():
    with pytest.raises(ContractError, match="requires current_user_explicit=true"):
        validate_record(
            record(
                claim="Use this workflow.",
                claim_class="USER_INTENT",
                memory_class="CURRENT_INPUT",
                current_user_explicit=False,
            )
        )


@pytest.mark.parametrize("memory_class", ["CURRENT_INPUT", "RETRIEVED_MEMORY", "AGENT_SUMMARY"])
def test_any_user_intent_record_is_forbidden_from_direct_kb_promotion(memory_class):
    kwargs = dict(
        claim="Make this global guidance.",
        claim_class="USER_INTENT",
        memory_class=memory_class,
        current_user_explicit=memory_class == "CURRENT_INPUT",
        canonical_relation="NONE" if memory_class == "CURRENT_INPUT" else "SUPPORTS",
        canonical_refs=[] if memory_class == "CURRENT_INPUT" else ["project://decision/ADR-INTENT"],
        promotion_requested=True,
        promotion_target="KNOWLEDGE_BASE",
        promotion_scope="Global guidance",
        promotion_provenance_refs=["chat://conversation/intent"],
        changes_active_guidance=False,
    )
    with pytest.raises(ContractError, match="cannot directly promote"):
        validate_record(record(**kwargs))


def test_duplicate_json_keys_are_invalid_exit_two(tmp_path):
    payload = record(
        risk="R4",
        canonical_relation="SUPPORTS",
        canonical_refs=["project://decision/ADR-DUP"],
    )
    raw = json.dumps(payload)
    raw = raw.replace(
        '"canonical_relation": "SUPPORTS"',
        '"canonical_relation": "CONFLICTS", "canonical_relation": "SUPPORTS"',
        1,
    )
    path = tmp_path / "duplicate.json"
    path.write_text(raw, encoding="utf-8")
    proc = subprocess.run(
        [sys.executable, "scripts/memory_knowledge_guard.py", "check", str(path), "--compact"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 2
    result = json.loads(proc.stdout)
    assert result["status"] == "INVALID"
    assert "duplicate JSON key" in result["error"]


def test_project_local_promotion_cannot_claim_active_global_guidance_change():
    with pytest.raises(ContractError, match="incompatible with PROJECT_REPOSITORY"):
        validate_record(
            record(
                claim_class="REUSABLE_GUIDANCE",
                canonical_relation="SUPPORTS",
                canonical_refs=["knowledge://RULE-PROJECT"],
                promotion_requested=True,
                promotion_target="PROJECT_REPOSITORY",
                promotion_scope="Project-local override",
                promotion_provenance_refs=["evidence://EVD-PROJECT"],
                changes_active_guidance=True,
            )
        )


def test_chat_uri_cannot_be_canonical_support():
    with pytest.raises(ContractError, match="scheme is not canonical"):
        validate_record(
            record(
                canonical_relation="SUPPORTS",
                canonical_refs=["chat://conversation/123"],
            )
        )


def test_pending_kb_promotion_returns_non_ready_exit_three(tmp_path):
    payload = record(
        claim_class="REUSABLE_GUIDANCE",
        canonical_relation="SUPPORTS",
        canonical_refs=["knowledge://RULE-PENDING"],
        promotion_requested=True,
        promotion_target="KNOWLEDGE_BASE",
        promotion_scope="Cross-project guidance",
        promotion_provenance_refs=["evidence://EVD-PENDING"],
    )
    proc = run_cli(tmp_path, payload)
    assert proc.returncode == 3
    result = json.loads(proc.stdout)
    assert result["status"] == "DECISION_READY"
    assert result["promotion_gate"] == "PENDING_EVIDENCE"
    assert result["source_delta_required"] == "UNKNOWN"


def test_computed_authority_scope_must_exist_in_policy():
    policy = json.loads(Path("machine/memory-knowledge-policy.json").read_text())
    policy["authority_scopes"].remove("CANONICAL_CLAIM")
    with pytest.raises(ContractError, match="computed authority_scope is outside policy"):
        evaluate_record(
            record(
                canonical_relation="SUPPORTS",
                canonical_refs=["project://decision/ADR-AUTHORITY"],
            ),
            policy=policy,
        )


def test_non_ascii_output_is_transport_safe(tmp_path):
    payload = record(
        canonical_relation="SUPPORTS",
        canonical_refs=["project://decision/ADR-UTF8"],
        promotion_requested=True,
        promotion_target="PROJECT_REPOSITORY",
        promotion_scope="Projekt — decyzja lokalna",
        promotion_provenance_refs=["evidence://EVD-UTF8"],
    )
    proc = run_cli(tmp_path, payload)
    assert proc.returncode == 0
    result = json.loads(proc.stdout)
    assert result["promotion_scope"] == "Projekt — decyzja lokalna"
