import copy
from datetime import datetime, timezone
import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("delivery_assurance", ROOT / "scripts/delivery_assurance.py")
da = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(da)
SHA = "a" * 40
DIGEST = "sha256:" + "1" * 64
NOW = datetime(2026, 10, 8, 13, tzinfo=timezone.utc)


def project_policy():
    return {
        "schema_version": "0.1.0",
        "project": "synthetic-independent-test-project",
        "required_ci_checks": ["ci"],
        "required_artifacts": ["app"],
        "max_age_minutes": {
            "ci_gate": 1440, "approval": 1440,
            "runtime_health": 180, "recovery": 43200,
        },
    }


def trusted_test_adapter(kind, identifier, payload, record):
    # TEST DOUBLE ONLY: CLI deliberately has no such adapter.
    return True


def assess(data, now=NOW, policy=None, verifier=trusted_test_adapter, policy_verified=True):
    return da.assess_release(data, now, policy=policy if policy is not None else project_policy(),
                             verifier=verifier, policy_verified=policy_verified)


def statuses(results):
    return {r["rule_id"]: r["status"] for r in results}


def workflow(tmp_path, body):
    p = tmp_path / "ci.yml"
    p.write_text(body, encoding="utf-8")
    return p


def release(target="production"):
    return {
        "schema_version": "0.1.0",
        "release_id": "release-001",
        "source_sha": SHA,
        "target_environment": target,
        "checks": [{"id": "ci", "required": True, "status": "PASS",
                    "evidence_ref": "github/actions/run/42", "observed_at": "2026-10-08T11:00:00Z"}],
        "artifacts": [{"name": "app", "ci_digest": DIGEST, "staging_digest": DIGEST,
                       "production_digest": DIGEST}],
        "production_approval": {"status": "PASS", "evidence_ref": "github/environment/approval/7",
                                "observed_at": "2026-10-08T11:30:00Z"},
        "recovery": {"required": True, "status": "PASS", "evidence_ref": "restore/drill/9",
                     "observed_at": "2026-10-07T11:00:00Z", "expires_at": "2026-11-07T11:00:00Z"},
        "runtime_health": {"status": "PASS", "source": "runtime",
                           "evidence_ref": "runtime/health/80",
                           "observed_at": "2026-10-08T12:00:00Z"},
    }


def test_pinned_external_action_is_pass(tmp_path):
    p = workflow(tmp_path, f"name: CI\non: push\njobs:\n  ci:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@{SHA}\n")
    assert statuses(da.assess_workflow(p))["DA-GHA-001"] == "PASS"


def test_mutable_tag_is_fail(tmp_path):
    p = workflow(tmp_path, "on: pull_request\njobs:\n  ci:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v4\n")
    findings = da.assess_workflow(p)
    assert statuses(findings)["DA-GHA-001"] == "FAIL"
    assert "checkout@v4" in findings[0]["reason"]


def test_local_action_is_not_mistaken_for_external(tmp_path):
    p = workflow(tmp_path, "on: push\njobs:\n  ci:\n    steps:\n      - uses: ./internal/action\n")
    assert statuses(da.assess_workflow(p))["DA-GHA-001"] == "PASS"


def test_workflow_run_without_privileged_checkout_is_unknown_not_fail(tmp_path):
    p = workflow(tmp_path, f"on:\n  workflow_run:\n    workflows: [CI]\njobs:\n  deploy:\n    steps:\n      - uses: actions/checkout@{SHA}\n")
    assert statuses(da.assess_workflow(p))["DA-GHA-002"] == "UNKNOWN"


def test_privileged_upstream_checkout_with_secrets_fails(tmp_path):
    p = workflow(tmp_path, f"on:\n  workflow_run:\n    workflows: [CI]\njobs:\n  deploy:\n    steps:\n      - uses: actions/checkout@{SHA}\n        with:\n          ref: ${{{{ github.event.workflow_run.head_sha }}}}\n      - run: echo ${{{{ secrets.PROD_KEY }}}}\n")
    assert statuses(da.assess_workflow(p))["DA-GHA-002"] == "FAIL"


def test_production_environment_is_unknown_until_external_settings_verified(tmp_path):
    p = workflow(tmp_path, "on: push\njobs:\n  deploy:\n    environment: production\n    steps: []\n")
    assert statuses(da.assess_workflow(p))["DA-GHA-003"] == "UNKNOWN"


@pytest.mark.parametrize("body", ["[unclosed", "[]", "jobs: 123"])
def test_invalid_or_unsupported_yaml_never_passes(tmp_path, body):
    p = workflow(tmp_path, body)
    assert da.assess_workflow(p)[0]["status"] == "FAIL"


def test_clean_release_is_review_eligible_not_automatically_deploy_authorized():
    findings = assess(release(), NOW)
    assert da.aggregate(findings) == "ELIGIBLE_FOR_REVIEW"
    assert all(f["status"] in {"PASS", "NOT_APPLICABLE"} for f in findings)


def test_skipped_mandatory_gate_blocks():
    data = release()
    data["checks"][0]["status"] = "FAIL"
    assert da.aggregate(assess(data, NOW)) == "BLOCKED"


def test_missing_gate_evidence_is_unknown_not_pass():
    data = release()
    del data["checks"][0]["evidence_ref"]
    assert statuses(assess(data, NOW))["DA-REL-001"] == "UNKNOWN"


def test_missing_mandatory_gates_never_gives_green():
    data = release()
    data["checks"] = []
    assert da.aggregate(assess(data, NOW)) == "UNVERIFIED"


def test_production_digest_drift_blocks():
    data = release()
    data["artifacts"][0]["production_digest"] = "sha256:" + "2" * 64
    assert statuses(assess(data, NOW))["DA-REL-002"] == "FAIL"


def test_missing_production_digest_is_unknown():
    data = release()
    del data["artifacts"][0]["production_digest"]
    assert statuses(assess(data, NOW))["DA-REL-002"] == "UNKNOWN"


def test_missing_production_approval_is_unknown():
    data = release()
    del data["production_approval"]
    assert statuses(assess(data, NOW))["DA-REL-003"] == "UNKNOWN"


def test_approval_declared_pass_without_external_proof_is_unknown():
    data = release()
    del data["production_approval"]["observed_at"]
    assert statuses(assess(data, NOW))["DA-REL-003"] == "UNKNOWN"


def test_expired_recovery_proof_fails():
    data = release()
    data["recovery"]["expires_at"] = "2026-10-07T20:00:00Z"
    assert statuses(assess(data, NOW))["DA-REL-004"] == "FAIL"


def test_missing_runtime_health_is_unknown():
    data = release()
    del data["runtime_health"]
    assert statuses(assess(data, NOW))["DA-REL-005"] == "UNKNOWN"


def test_pipeline_success_cannot_be_runtime_health():
    data = release()
    data["runtime_health"]["source"] = "pipeline"
    assert statuses(assess(data, NOW))["DA-REL-005"] == "UNKNOWN"


def test_waiver_requires_owned_scoped_timed_risk_acceptance():
    data = release()
    data["production_approval"]["status"] = "WAIVED"
    assert statuses(assess(data, NOW))["DA-REL-000"] == "FAIL"
    data["production_approval"]["risk_acceptance"] = {
        "owner": "Business owner", "scope": "pilot only",
        "reason": "documented temporary exception", "expires_at": "2026-10-10T12:00:00Z"}
    result = assess(data, NOW)
    assert statuses(result)["DA-REL-003"] == "WAIVED"
    assert da.aggregate(result) == "REVIEW_REQUIRED"


def test_wrong_source_sha_rejected_by_schema():
    data = release()
    data["source_sha"] = "main"
    assert statuses(assess(data, NOW))["DA-REL-000"] == "FAIL"


def test_staging_release_has_no_production_approval_assumption():
    data = release("staging")
    del data["production_approval"]
    del data["runtime_health"]
    for a in data["artifacts"]:
        del a["production_digest"]
    assert statuses(assess(data, NOW))["DA-REL-003"] == "NOT_APPLICABLE"
    assert da.aggregate(assess(data, NOW)) == "ELIGIBLE_FOR_REVIEW"


def test_cli_is_advisory_and_outputs_machine_readable_verdict(tmp_path, capsys):
    p = workflow(tmp_path, "on: push\njobs:\n  ci:\n    steps:\n      - uses: actions/checkout@v4\n")
    assert da.main(["workflows", str(p)]) == 0
    import json
    data = json.loads(capsys.readouterr().out)
    assert data["mode"] == "ADVISORY"
    assert data["verdict"] == "BLOCKED"
    assert data["findings"][0]["rule_id"] == "DA-GHA-001"

def test_expired_waiver_is_fail_not_review_required():
    data = release()
    data["production_approval"]["status"] = "WAIVED"
    data["production_approval"]["risk_acceptance"] = {
        "owner": "Approver", "scope": "pilot only",
        "reason": "Emergency risk acceptance", "expires_at": "2026-10-07T12:00:00Z"}
    assert statuses(assess(data, NOW))["DA-REL-003"] == "FAIL"


def test_future_dated_evidence_cannot_prove_current_gate():
    data = release()
    data["checks"][0]["observed_at"] = "2026-10-09T11:00:00Z"
    assert statuses(assess(data, NOW))["DA-REL-001"] == "UNKNOWN"


def test_production_recovery_requirement_cannot_be_self_disabled():
    data = release()
    data["recovery"]["required"] = False
    assert statuses(assess(data, NOW))["DA-REL-004"] == "UNKNOWN"


def test_malformed_steps_are_unknown(tmp_path):
    p = workflow(tmp_path, "on: push\njobs:\n  ci:\n    steps: oops\n")
    assert da.assess_workflow(p)[0]["status"] == "FAIL"


def test_comment_only_dangerous_text_does_not_make_workflow_run_fail(tmp_path):
    p = workflow(tmp_path, f"# github.event.workflow_run.head_sha and secrets.PROD_KEY\non:\n  workflow_run:\n    workflows: [CI]\njobs:\n  build:\n    steps:\n      - uses: actions/checkout@{SHA}\n")
    assert statuses(da.assess_workflow(p))["DA-GHA-002"] == "UNKNOWN"


def test_short_docker_digest_rejected(tmp_path):
    p = workflow(tmp_path, "on: push\njobs:\n  ci:\n    steps:\n      - uses: docker://alpine@sha256:abcd\n")
    assert statuses(da.assess_workflow(p))["DA-GHA-001"] == "FAIL"


def test_invalid_observation_timestamp_rejected():
    data = release()
    data["runtime_health"]["observed_at"] = "yesterday"
    assert statuses(assess(data, NOW))["DA-REL-000"] == "FAIL"


def test_rule_catalog_matches_implemented_rule_ids():
    import json
    ids = {r["id"] for r in json.loads(da.RULES.read_text())["rules"]}
    assert ids == {"DA-REL-006", "DA-GHA-000", "DA-GHA-001", "DA-GHA-002", "DA-GHA-003",
                   "DA-REL-000", "DA-REL-001", "DA-REL-002", "DA-REL-003",
                   "DA-REL-004", "DA-REL-005"}

@pytest.mark.parametrize("section,key", [
    ("checks", "DA-REL-001"),
    ("production_approval", "DA-REL-003"),
    ("recovery", "DA-REL-004"),
    ("runtime_health", "DA-REL-005"),
])
def test_required_control_cannot_self_exempt_with_not_applicable(section, key):
    data = release()
    item = data["checks"][0] if section == "checks" else data[section]
    item["status"] = "NOT_APPLICABLE"
    assert any(f["rule_id"] == key and f["status"] == "FAIL"
               for f in assess(data, NOW))


# VERIFY-01 reproductions and negative tests; these must not pass by checking declarations alone.

def test_verify01_fabricated_references_are_unverified_even_when_status_says_pass():
    data = release()
    findings = da.assess_release(data, NOW, policy=project_policy())
    assert da.aggregate(findings) == "UNVERIFIED"
    assert all(x["status"] != "PASS" for x in findings)
    assert statuses(findings)["DA-REL-006"] == "UNKNOWN"


def test_verify01_unverified_project_policy_never_grants_review_eligibility():
    data = release()
    findings = assess(data, policy_verified=False)
    assert da.aggregate(findings) == "UNVERIFIED"
    assert statuses(findings)["DA-REL-006"] == "UNKNOWN"


def test_verify01_no_policy_returns_unverified_even_with_test_verifier():
    data = release()
    findings = da.assess_release(data, NOW, verifier=trusted_test_adapter, policy_verified=True)
    assert da.aggregate(findings) == "UNVERIFIED"
    assert statuses(findings)["DA-REL-001"] == "UNKNOWN"
    assert statuses(findings)["DA-REL-002"] == "UNKNOWN"


def test_verify01_optional_failed_check_cannot_bypass_trusted_required_gate():
    data = release()
    data["checks"] = [{"id": "financial-reconciliation", "required": False, "status": "FAIL"}]
    policy = project_policy()
    policy["required_ci_checks"] = ["financial-reconciliation"]
    findings = assess(data, policy=policy)
    assert da.aggregate(findings) == "BLOCKED"
    assert any(x["rule_id"] == "DA-REL-001" and x["status"] == "FAIL" for x in findings)


def test_verify01_expected_required_gate_missing_cannot_be_green():
    data = release()
    policy = project_policy()
    policy["required_ci_checks"].append("financial-reconciliation")
    findings = assess(data, policy=policy)
    assert da.aggregate(findings) == "UNVERIFIED"
    assert any("financial-reconciliation" in x["reason"] and x["status"] == "UNKNOWN" for x in findings)


def test_verify01_missing_worker_migrator_artifacts_cannot_be_green():
    data = release()
    policy = project_policy()
    policy["required_artifacts"] = ["app", "worker", "migrator"]
    findings = assess(data, policy=policy)
    assert da.aggregate(findings) == "UNVERIFIED"
    assert len([x for x in findings if x["rule_id"] == "DA-REL-002" and x["status"] == "UNKNOWN"]) == 2


@pytest.mark.parametrize("entry", ["check", "artifact"])
def test_verify01_duplicate_identifiers_are_rejected(entry):
    data = release()
    if entry == "check":
        data["checks"].append(copy.deepcopy(data["checks"][0]))
    else:
        data["artifacts"].append(copy.deepcopy(data["artifacts"][0]))
    assert statuses(assess(data))["DA-REL-000"] == "FAIL"


def test_verify01_years_old_runtime_health_is_not_current_proof():
    data = release()
    data["runtime_health"]["observed_at"] = "2020-01-01T00:00:00Z"
    assert statuses(assess(data))["DA-REL-005"] == "FAIL"


def test_verify01_old_ci_evidence_expires_with_project_policy():
    data = release()
    data["checks"][0]["observed_at"] = "2026-09-01T00:00:00Z"
    assert statuses(assess(data))["DA-REL-001"] == "FAIL"


def test_verify01_old_approval_expires_with_project_policy():
    data = release()
    data["production_approval"]["observed_at"] = "2026-09-01T00:00:00Z"
    assert statuses(assess(data))["DA-REL-003"] == "FAIL"


def test_verify01_missing_workflow_trigger_fails_closed(tmp_path):
    p = workflow(tmp_path, f"jobs:\n  ci:\n    steps:\n      - uses: actions/checkout@{SHA}\n")
    findings = da.assess_workflow(p)
    assert findings[0]["rule_id"] == "DA-GHA-000"
    assert da.aggregate(findings) == "BLOCKED"


def test_verify01_duplicate_trigger_mapping_keys_are_rejected(tmp_path):
    p = workflow(tmp_path, f"on: push\non: workflow_dispatch\njobs:\n  ci:\n    steps:\n      - uses: actions/checkout@{SHA}\n")
    findings = da.assess_workflow(p)
    assert da.aggregate(findings) == "BLOCKED"
    assert "Duplicate" in findings[0]["reason"]


def test_verify01_duplicate_nested_keys_are_rejected(tmp_path):
    p = workflow(tmp_path, "on: push\njobs:\n  ci:\n    steps:\n      - uses: actions/checkout@v4\n        uses: actions/setup-python@v5\n")
    assert statuses(da.assess_workflow(p))["DA-GHA-000"] == "FAIL"


def test_verify01_secret_in_other_job_does_not_prove_same_job_risk(tmp_path):
    p = workflow(tmp_path, f'''on:
  workflow_run:
    workflows: [CI]
jobs:
  checkout:
    steps:
      - uses: actions/checkout@{SHA}
        with:
          ref: ${{{{ github.event.workflow_run.head_sha }}}}
  unrelated:
    steps:
      - run: echo ${{{{ secrets.UNRELATED_TOKEN }}}}
''')
    findings = da.assess_workflow(p)
    assert statuses(findings)["DA-GHA-002"] == "UNKNOWN"
    assert da.aggregate(findings) == "UNVERIFIED"


def test_verify01_same_job_checkout_secret_still_fails(tmp_path):
    p = workflow(tmp_path, f'''on:
  workflow_run:
    workflows: [CI]
jobs:
  checkout:
    steps:
      - uses: actions/checkout@{SHA}
        with:
          ref: ${{{{ github.event.workflow_run.head_sha }}}}
      - run: echo ${{{{ secrets.SENSITIVE }}}}
''')
    assert statuses(da.assess_workflow(p))["DA-GHA-002"] == "FAIL"


def test_verify01_dynamic_environment_keeps_approval_unknown(tmp_path):
    p = workflow(tmp_path, """on: push
jobs:
  deploy:
    environment: ${{ inputs.environment }}
    steps: []
""")
    assert statuses(da.assess_workflow(p))["DA-GHA-003"] == "UNKNOWN"


def test_verify01_policy_invalid_shape_fails():
    policy = project_policy()
    policy["required_ci_checks"] = []
    assert statuses(assess(release(), policy=policy))["DA-REL-006"] == "FAIL"


def test_verify01_policy_duplicate_expected_gates_fails():
    policy = project_policy()
    policy["required_ci_checks"] = ["ci", "ci"]
    assert statuses(assess(release(), policy=policy))["DA-REL-006"] == "FAIL"


def test_verify01_self_declared_false_on_unlisted_check_does_not_grant_green():
    data = release()
    data["checks"].append({"id": "critical-missing", "required": False, "status": "FAIL"})
    assert da.aggregate(assess(data)) == "BLOCKED"


def test_verify01_stale_restore_proof_even_before_own_expiry_fails_policy_limit():
    data = release()
    data["recovery"]["observed_at"] = "2026-08-01T00:00:00Z"
    assert statuses(assess(data))["DA-REL-004"] == "FAIL"


def test_verify01_exception_unverified_cannot_be_review_waiver():
    data = release()
    data["production_approval"]["status"] = "WAIVED"
    data["production_approval"]["risk_acceptance"] = {
        "owner": "Risk owner", "scope": "single release",
        "reason": "Temporary documented exception", "expires_at": "2026-10-10T12:00:00Z"}
    findings = da.assess_release(data, NOW, policy=project_policy())
    assert statuses(findings)["DA-REL-003"] == "UNKNOWN"
    assert da.aggregate(findings) == "UNVERIFIED"


def test_verify01_external_verifier_fail_is_unknown_not_pass():
    assert statuses(assess(release(), verifier=lambda *args: False))["DA-REL-003"] == "UNKNOWN"


def test_verify01_local_cli_never_claims_authoritative_pass(tmp_path, capsys):
    import json
    rec = tmp_path / "release.json"
    pol = tmp_path / "policy.json"
    rec.write_text(json.dumps(release()))
    pol.write_text(json.dumps(project_policy()))
    assert da.main(["release", str(rec), "--policy", str(pol), "--as-of", "2026-10-08T13:00:00Z"]) == 0
    output = json.loads(capsys.readouterr().out)
    assert output["verdict"] == "UNVERIFIED"
    assert output["mode"] == "ADVISORY"
    assert output["findings"][0]["rule_id"] == "DA-REL-006"


def test_verify01_new_rule_is_in_catalog():
    import json
    catalog = json.loads(da.RULES.read_text())
    assert catalog["version"] == "0.2.0"
    assert any(r["id"] == "DA-REL-006" for r in catalog["rules"])


def test_verify01_deploy_like_job_without_environment_is_unverified(tmp_path):
    p = workflow(tmp_path, f"on: workflow_dispatch\njobs:\n  deploy_prod:\n    steps:\n      - uses: actions/checkout@{SHA}\n")
    assert statuses(da.assess_workflow(p))["DA-GHA-003"] == "UNKNOWN"


def test_verify01_simple_ci_without_environment_is_not_production_claim(tmp_path):
    p = workflow(tmp_path, f"on: pull_request\njobs:\n  test:\n    steps:\n      - uses: actions/checkout@{SHA}\n")
    assert statuses(da.assess_workflow(p))["DA-GHA-003"] == "NOT_APPLICABLE"
