import importlib.util
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("source_delta", ROOT / "scripts" / "source_delta.py")
source_delta = importlib.util.module_from_spec(spec)
spec.loader.exec_module(source_delta)


def registry(source):
    return {"version": "1.0.0", "authority_tiers": {}, "sources": [source] if source else []}


def ledger(source_id="SRC-1", status="active"):
    return {
        "version": "1.0.0",
        "items": [{
            "id": "EVD-TEST-001",
            "statement": "A sufficiently long atomic test claim.",
            "source_ids": [source_id],
            "domains": ["test"],
            "strength": "strong",
            "scope": "test scope",
            "status": status,
        }],
    }


def source(**overrides):
    value = {
        "id": "SRC-1",
        "tier": "B",
        "name": "Source One",
        "url": "https://example.test/source",
        "domains": ["test"],
        "strength": "strong",
        "verified_at": "2026-10-01",
        "cutoff_target": "2026-09-30",
    }
    value.update(overrides)
    return value


def test_detector_never_infers_semantic_classification_and_traces_blast_radius(tmp_path):
    (tmp_path / "consumer.md").write_text("Uses EVD-TEST-001 for a decision.")
    base = registry(source())
    head = registry(source(domains=["test", "extended"], verified_at="2026-10-05"))

    report = source_delta.detect_from_documents(
        base, head, ledger(), base_ref="base", head_ref="head", root=tmp_path
    )

    assert len(report["deltas"]) == 1
    delta = report["deltas"][0]
    assert delta["event"] == "CHANGED"
    assert delta["classification"] == "UNASSESSED"
    assert delta["promotion_gate"] == "BLOCKED"
    assert delta["risk"] == "R3"
    assert delta["affected_evidence"][0]["id"] == "EVD-TEST-001"
    assert delta["downstream_refs"] == ["consumer.md"]
    assert {"scope", "freshness"} <= set(delta["change_dimensions"])


def test_added_unused_source_is_r1_but_still_blocked_until_semantic_review(tmp_path):
    report = source_delta.detect_from_documents(
        registry(None), registry(source()), {"version": "1.0.0", "items": []}, root=tmp_path
    )
    delta = report["deltas"][0]
    assert delta["event"] == "ADDED"
    assert delta["risk"] == "R1"
    assert delta["promotion_gate"] == "BLOCKED"


def test_authority_downgrade_is_r3_even_without_live_evidence(tmp_path):
    report = source_delta.detect_from_documents(
        registry(source(tier="B")),
        registry(source(tier="E")),
        {"version": "1.0.0", "items": []},
        root=tmp_path,
    )
    delta = report["deltas"][0]
    assert delta["risk"] == "R3"
    assert "authority" in delta["change_dimensions"]


def test_support_becomes_ready_only_after_live_evidence_review(tmp_path):
    report = source_delta.detect_from_documents(
        registry(source()),
        registry(source(verified_at="2026-10-05")),
        ledger(),
        root=tmp_path,
    )

    assessed = source_delta.apply_assessment(report, {
        "source_id": "SRC-1",
        "classification": "SUPPORT",
        "rationale": "Compared the revised source text; the same scoped claim is reinforced.",
        "reviewed_evidence_ids": ["EVD-TEST-001"],
        "downstream_actions": ["Reverified EVD-TEST-001 against the revised source."],
        "resolution": "accepted",
    })

    delta = assessed["deltas"][0]
    assert delta["promotion_gate"] == "READY"
    assert source_delta.validate_report(assessed, require_ready=True) == []


def test_falsify_requires_downstream_action_and_explicit_replacement_or_decision(tmp_path):
    report = source_delta.detect_from_documents(
        registry(source()),
        registry(source(verified_at="2026-10-05")),
        ledger(),
        root=tmp_path,
    )

    incomplete = source_delta.apply_assessment(report, {
        "source_id": "SRC-1",
        "classification": "FALSIFY",
        "rationale": "The revised normative text contradicts the active claim in the same scope.",
        "reviewed_evidence_ids": ["EVD-TEST-001"],
        "resolution": "superseded",
    })
    assert incomplete["deltas"][0]["promotion_gate"] == "BLOCKED"

    still_invalid = source_delta.apply_assessment(incomplete, {
        "source_id": "SRC-1",
        "downstream_actions": ["Supersede the affected claim and rerun its behavioral evaluation."],
        "replacement_evidence_ids": ["EVD-TEST-001"],
    })
    assert still_invalid["deltas"][0]["promotion_gate"] == "BLOCKED"
    assert any(
        "distinct from falsified/affected" in error
        for error in source_delta.validate_report(still_invalid, require_ready=True)
    )


def test_removed_source_supporting_live_evidence_cannot_close_as_no_action(tmp_path):
    report = source_delta.detect_from_documents(
        registry(source()),
        registry(None),
        ledger(),
        root=tmp_path,
    )

    assessed = source_delta.apply_assessment(report, {
        "source_id": "SRC-1",
        "classification": "NO_MATERIAL_CHANGE",
        "rationale": "Removal inspected.",
        "reviewed_evidence_ids": ["EVD-TEST-001"],
        "resolution": "no-action",
    })
    delta = assessed["deltas"][0]
    assert delta["risk"] == "R3"
    assert delta["promotion_gate"] == "BLOCKED"
    assert any("removed source" in e for e in source_delta.readiness_errors(
        delta, source_delta.json.loads(source_delta.POLICY_PATH.read_text())
    ))


def test_validate_rejects_tampered_ready_gate(tmp_path):
    report = source_delta.detect_from_documents(
        registry(source()),
        registry(source(verified_at="2026-10-05")),
        ledger(),
        root=tmp_path,
    )
    report["deltas"][0]["promotion_gate"] = "READY"
    errors = source_delta.validate_report(report)
    assert any("promotion_gate must be BLOCKED" in error for error in errors)


def test_challenge_pending_never_becomes_ready(tmp_path):
    report = source_delta.detect_from_documents(
        registry(source()),
        registry(source(domains=["test", "changed"])),
        ledger(),
        root=tmp_path,
    )
    assessed = source_delta.apply_assessment(report, {
        "source_id": "SRC-1",
        "classification": "CHALLENGE",
        "rationale": "The revised scope conflicts with the currently active interpretation.",
        "reviewed_evidence_ids": ["EVD-TEST-001"],
        "downstream_actions": ["Open a scoped decision record and re-run affected evals."],
        "resolution": "pending",
    })
    assert assessed["deltas"][0]["promotion_gate"] == "BLOCKED"
    assert any(
        "resolution is pending" in error
        for error in source_delta.readiness_errors(
            assessed["deltas"][0],
            source_delta.json.loads(source_delta.POLICY_PATH.read_text()),
        )
    )


def test_provenance_verification_detects_tampered_hashes():
    report = source_delta.detect_git("HEAD", "HEAD")
    assert source_delta.provenance_errors(report) == []
    report["hashes"]["head_registry_sha256"] = "0" * 64
    assert "stored provenance hashes do not match referenced Git inputs" in source_delta.provenance_errors(report)


def test_removed_source_keeps_baseline_citation_in_blast_radius(tmp_path):
    base_ledger = ledger()
    head_ledger = ledger(source_id="OTHER")
    report = source_delta.detect_from_documents(
        registry(source()),
        registry(None),
        head_ledger,
        base_ledger=base_ledger,
        root=tmp_path,
    )
    delta = next(d for d in report["deltas"] if d["source_id"] == "SRC-1")
    affected = delta["affected_evidence"]
    assert affected == [{
        "id": "EVD-TEST-001",
        "baseline_status": "active",
        "head_status": "active",
        "strength": "strong",
        "scope": "test scope",
        "baseline_cites": True,
        "head_cites": False,
    }]


def test_report_validation_rejects_invalid_semantic_enum(tmp_path):
    report = source_delta.detect_from_documents(
        registry(source()),
        registry(source(verified_at="2026-10-05")),
        ledger(),
        root=tmp_path,
    )
    report["deltas"][0]["classification"] = "MAGIC"
    assert any("invalid classification" in error for error in source_delta.validate_report(report))


def test_baseline_live_status_still_requires_review_after_same_commit_archival(tmp_path):
    report = source_delta.detect_from_documents(
        registry(source()),
        registry(None),
        ledger(source_id="OTHER", status="archived"),
        base_ledger=ledger(status="active"),
        root=tmp_path,
    )
    assessed = source_delta.apply_assessment(report, {
        "source_id": "SRC-1",
        "classification": "NO_MATERIAL_CHANGE",
        "rationale": "The removal and archival were inspected.",
        "reviewed_evidence_ids": [],
        "resolution": "no-action",
    })
    errors = source_delta.readiness_errors(
        assessed["deltas"][0],
        source_delta.json.loads(source_delta.POLICY_PATH.read_text()),
    )
    assert any("unreviewed live evidence: EVD-TEST-001" in error for error in errors)
    assert assessed["deltas"][0]["promotion_gate"] == "BLOCKED"


def test_unknown_strength_transition_fails_closed_as_r3(tmp_path):
    report = source_delta.detect_from_documents(
        registry(source(strength="strong")),
        registry(source(strength="future-strength")),
        {"version": "1.0.0", "items": []},
        root=tmp_path,
    )
    assert report["deltas"][0]["risk"] == "R3"


def test_removed_live_source_cannot_be_closed_as_support(tmp_path):
    report = source_delta.detect_from_documents(
        registry(source()),
        registry(None),
        ledger(),
        root=tmp_path,
    )
    assessed = source_delta.apply_assessment(report, {
        "source_id": "SRC-1",
        "classification": "SUPPORT",
        "rationale": "The source disappeared but the old claim still appears substantively correct.",
        "reviewed_evidence_ids": ["EVD-TEST-001"],
        "downstream_actions": ["Investigated the missing source and preserved the affected claim."],
        "resolution": "accepted",
    })
    errors = source_delta.readiness_errors(assessed["deltas"][0], source_delta.load_policy())
    assert any("removed source supporting live evidence requires" in error for error in errors)
    assert assessed["deltas"][0]["promotion_gate"] == "BLOCKED"


def test_evidence_only_change_emits_source_delta(tmp_path):
    base = ledger(status="candidate")
    head = ledger(status="active")
    report = source_delta.detect_from_documents(
        registry(source()),
        registry(source()),
        head,
        base_ledger=base,
        root=tmp_path,
    )
    delta = next(d for d in report["deltas"] if d["source_id"] == "SRC-1")
    assert delta["event"] == "CHANGED"
    assert delta["changed_fields"] == ["evidence_ledger"]
    assert delta["change_dimensions"] == ["evidence"]
    assert delta["risk"] == "R3"


def test_downstream_matching_does_not_match_evidence_id_prefix(tmp_path):
    (tmp_path / "prefix.md").write_text("Uses EVD-TEST-0010 only.")
    (tmp_path / "exact.md").write_text("Uses EVD-TEST-001 for the decision.")
    assert source_delta.downstream_refs_for(["EVD-TEST-001"], root=tmp_path) == ["exact.md"]


def test_detect_git_stores_resolved_commit_shas():
    report = source_delta.detect_git("HEAD", "HEAD")
    assert source_delta.SHA_RE.fullmatch(report["base_ref"])
    assert source_delta.SHA_RE.fullmatch(report["head_ref"])
    assert report["base_ref"] == report["head_ref"]


def test_report_validation_handles_null_rationale_without_crashing(tmp_path):
    report = source_delta.detect_from_documents(
        registry(source()),
        registry(source(verified_at="2026-10-05")),
        ledger(),
        root=tmp_path,
    )
    delta = report["deltas"][0]
    delta["classification"] = "SUPPORT"
    delta["rationale"] = None
    delta["reviewed_evidence_ids"] = ["EVD-TEST-001"]
    delta["downstream_actions"] = ["Reverified affected evidence."]
    delta["resolution"] = "accepted"
    source_delta.recompute_gate(delta, source_delta.load_policy())
    errors = source_delta.validate_report(report)
    assert any("rationale must be a string" in error for error in errors)


def test_reviewed_evidence_must_be_subset_of_affected(tmp_path):
    report = source_delta.detect_from_documents(
        registry(source()),
        registry(source(verified_at="2026-10-05")),
        ledger(),
        root=tmp_path,
    )
    report["deltas"][0]["reviewed_evidence_ids"] = ["EVD-NOT-AFFECTED"]
    errors = source_delta.validate_report(report)
    assert any("subset of affected evidence" in error for error in errors)


def test_report_matching_requires_same_detected_structure(tmp_path):
    detected = source_delta.detect_from_documents(
        registry(source()),
        registry(source(verified_at="2026-10-05")),
        ledger(),
        root=tmp_path,
    )
    candidate = source_delta.apply_assessment(detected, {
        "source_id": "SRC-1",
        "classification": "SUPPORT",
        "rationale": "The source was rechecked and the same scoped statement remains supported.",
        "reviewed_evidence_ids": ["EVD-TEST-001"],
        "downstream_actions": ["Reverified the affected evidence record."],
        "resolution": "accepted",
    })
    assert source_delta.report_matches_detected(candidate, detected)
    candidate["deltas"][0]["event"] = "ADDED"
    assert not source_delta.report_matches_detected(candidate, detected)


def _git(repo, *args):
    return subprocess.check_output(["git", *args], cwd=repo, text=True).strip()


def _write_knowledge_repo(repo, src, evd):
    (repo / "01-governance").mkdir(parents=True, exist_ok=True)
    (repo / "02-evidence").mkdir(parents=True, exist_ok=True)
    (repo / "01-governance" / "source-registry.json").write_text(
        json.dumps(registry(src), indent=2) + "\n"
    )
    (repo / "02-evidence" / "evidence-ledger.json").write_text(
        json.dumps(evd, indent=2) + "\n"
    )


def test_gate_blocks_unassessed_source_change_and_accepts_committed_ready_report(tmp_path, monkeypatch):
    repo = tmp_path / "repo"
    repo.mkdir()
    subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
    subprocess.run(["git", "config", "user.email", "test@example.test"], cwd=repo, check=True)
    subprocess.run(["git", "config", "user.name", "Source Delta Test"], cwd=repo, check=True)

    active_ledger = ledger()
    _write_knowledge_repo(repo, source(tier="B"), active_ledger)
    (repo / "consumer.md").write_text("Decision consumes EVD-TEST-001.\n")
    (repo / "prefix.md").write_text("Only EVD-TEST-001-legacy appears here.\n")
    subprocess.run(["git", "add", "."], cwd=repo, check=True)
    subprocess.run(["git", "commit", "-q", "-m", "base"], cwd=repo, check=True)
    base = _git(repo, "rev-parse", "HEAD")

    _write_knowledge_repo(repo, source(tier="E"), active_ledger)
    subprocess.run(["git", "add", "."], cwd=repo, check=True)
    subprocess.run(["git", "commit", "-q", "-m", "downgrade source"], cwd=repo, check=True)
    knowledge_head = _git(repo, "rev-parse", "HEAD")

    monkeypatch.setattr(source_delta, "ROOT", repo)
    reports_dir = repo / "01-governance" / "source-deltas"

    detected = source_delta.detect_git(base, knowledge_head)
    assert detected["base_ref"] == base
    assert detected["head_ref"] == knowledge_head
    assert detected["deltas"][0]["risk"] == "R3"
    assert detected["deltas"][0]["downstream_refs"] == ["consumer.md"]
    assert source_delta.gate_reports(base, knowledge_head, reports_dir)

    invalid_replacement = source_delta.apply_assessment(detected, {
        "source_id": "SRC-1",
        "classification": "FALSIFY",
        "rationale": "The authority change is treated as falsifying the current claim for this test.",
        "reviewed_evidence_ids": ["EVD-TEST-001"],
        "downstream_actions": ["Supersede the affected claim and rerun its downstream behavioral checks."],
        "replacement_evidence_ids": ["EVD-DOES-NOT-EXIST"],
        "resolution": "superseded",
    })
    assert invalid_replacement["deltas"][0]["promotion_gate"] == "BLOCKED"
    assert any(
        "replacement evidence does not exist" in error
        for error in source_delta.validate_report(invalid_replacement, require_ready=True)
    )

    assessed = source_delta.apply_assessment(detected, {
        "source_id": "SRC-1",
        "classification": "SUPPORT",
        "rationale": "Reviewed the authority change and retained the claim only with explicit downstream revalidation.",
        "reviewed_evidence_ids": ["EVD-TEST-001"],
        "downstream_actions": ["Revalidate every downstream use before relying on the downgraded source."],
        "resolution": "accepted",
    })
    assert assessed["deltas"][0]["promotion_gate"] == "READY"
    assert source_delta.validate_report(assessed, require_ready=True) == []
    assert source_delta.provenance_errors(assessed) == []

    reports_dir.mkdir(parents=True)
    report_path = reports_dir / "SDL-TEST.json"
    report_path.write_text(json.dumps(assessed, indent=2) + "\n")
    subprocess.run(["git", "add", "."], cwd=repo, check=True)
    subprocess.run(["git", "commit", "-q", "-m", "add source delta report"], cwd=repo, check=True)
    report_head = _git(repo, "rev-parse", "HEAD")

    assert source_delta.gate_reports(base, report_head, reports_dir) == []

    forged = json.loads(report_path.read_text())
    forged["base_ref"] = "a" * 40
    forged["head_ref"] = "b" * 40
    fake_reports = tmp_path / "fake-reports"
    fake_reports.mkdir()
    (fake_reports / "SDL-FORGED.json").write_text(json.dumps(forged, indent=2) + "\n")
    assert source_delta.gate_reports(base, report_head, fake_reports)
    assert source_delta.gate_reports(
        base,
        report_head,
        fake_reports,
        allow_unreachable_report_refs=True,
    ) == []

    (repo / "later-consumer.md").write_text("New consumer references EVD-TEST-001.\n")
    subprocess.run(["git", "add", "."], cwd=repo, check=True)
    subprocess.run(["git", "commit", "-q", "-m", "add downstream consumer"], cwd=repo, check=True)
    docs_head = _git(repo, "rev-parse", "HEAD")
    assert source_delta.gate_reports(base, docs_head, reports_dir) == []


def test_r3_cannot_use_blank_decision_or_short_action_as_escape(tmp_path):
    report = source_delta.detect_from_documents(
        registry(source()),
        registry(source(verified_at="2026-10-05")),
        ledger(),
        root=tmp_path,
    )
    assessed = source_delta.apply_assessment(report, {
        "source_id": "SRC-1",
        "classification": "SUPPORT",
        "rationale": "The revised source was inspected and still supports the same scoped statement.",
        "reviewed_evidence_ids": ["EVD-TEST-001"],
        "downstream_actions": ["x"],
        "decision_record": " ",
        "resolution": "accepted",
    })
    delta = assessed["deltas"][0]
    assert delta["promotion_gate"] == "BLOCKED"
    errors = source_delta.validate_report(assessed, require_ready=True)
    assert any("downstream_actions" in error or "substantive downstream action" in error for error in errors)
    assert any("decision_record" in error for error in errors)


def test_removed_unused_source_cannot_be_extend(tmp_path):
    report = source_delta.detect_from_documents(
        registry(source()),
        registry(None),
        {"version": "1.0.0", "items": []},
        root=tmp_path,
    )
    assessed = source_delta.apply_assessment(report, {
        "source_id": "SRC-1",
        "classification": "EXTEND",
        "rationale": "The source was removed, so extending from it would be semantically invalid.",
        "reviewed_evidence_ids": [],
        "downstream_actions": ["Record the source removal and review any future replacement separately."],
        "resolution": "accepted",
    })
    assert assessed["deltas"][0]["promotion_gate"] == "BLOCKED"
    assert any(
        "removed source requires one of" in error
        for error in source_delta.readiness_errors(assessed["deltas"][0], source_delta.load_policy())
    )


def test_orphan_evidence_change_emits_reserved_ledger_delta(tmp_path):
    base = {"version": "1.0.0", "items": []}
    head = {
        "version": "1.0.0",
        "items": [{
            "id": "EVD-ORPHAN-001",
            "statement": "An orphan claim used to test ledger-only change detection.",
            "source_ids": [],
            "domains": ["test"],
            "strength": "strong",
            "scope": "test scope",
            "status": "active",
        }],
    }
    report = source_delta.detect_from_documents(
        registry(source()),
        registry(source()),
        head,
        base_ledger=base,
        root=tmp_path,
    )
    delta = next(d for d in report["deltas"] if d["source_id"] == "EVIDENCE-LEDGER")
    assert delta["event"] == "CHANGED"
    assert delta["risk"] == "R3"
    assert delta["affected_evidence"][0]["id"] == "EVD-ORPHAN-001"
    assert delta["promotion_gate"] == "BLOCKED"


def test_ledger_metadata_change_emits_reserved_ledger_delta(tmp_path):
    base = {"version": "1.0.0", "items": []}
    head = {"version": "1.1.0", "items": []}
    report = source_delta.detect_from_documents(
        registry(source()),
        registry(source()),
        head,
        base_ledger=base,
        root=tmp_path,
    )
    delta = next(d for d in report["deltas"] if d["source_id"] == "EVIDENCE-LEDGER")
    assert delta["risk"] == "R2"
    assert delta["before"]["ledger_metadata"]["version"] == "1.0.0"
    assert delta["after"]["ledger_metadata"]["version"] == "1.1.0"


def test_schema_is_executable_and_rejects_short_action(tmp_path):
    report = source_delta.detect_from_documents(
        registry(source()),
        registry(source(verified_at="2026-10-05")),
        ledger(),
        root=tmp_path,
    )
    report["deltas"][0]["downstream_actions"] = ["x"]
    errors = source_delta.schema_validation_errors(report)
    assert any("downstream_actions" in error for error in errors)


def test_registry_metadata_change_emits_r3_synthetic_delta(tmp_path):
    base_registry = registry(source())
    base_registry["authority_tiers"] = {"B": "first-party"}
    head_registry = registry(source())
    head_registry["authority_tiers"] = {"B": "untrusted reinterpretation"}

    report = source_delta.detect_from_documents(
        base_registry,
        head_registry,
        ledger(),
        base_ledger=ledger(),
        root=tmp_path,
    )

    delta = next(d for d in report["deltas"] if d["source_id"] == "SOURCE-REGISTRY")
    assert delta["risk"] == "R3"
    assert delta["changed_fields"] == ["source_registry_metadata"]
    assert delta["affected_evidence"][0]["id"] == "EVD-TEST-001"
    assert delta["promotion_gate"] == "BLOCKED"


def test_falsify_cannot_replace_evidence_with_itself(tmp_path):
    report = source_delta.detect_from_documents(
        registry(source()),
        registry(source(verified_at="2026-10-05")),
        ledger(),
        root=tmp_path,
    )
    assessed = source_delta.apply_assessment(report, {
        "source_id": "SRC-1",
        "classification": "FALSIFY",
        "rationale": "The revised source falsifies the prior claim and requires explicit supersession.",
        "reviewed_evidence_ids": ["EVD-TEST-001"],
        "downstream_actions": ["Supersede the prior claim and rerun the affected behavioral verification."],
        "replacement_evidence_ids": ["EVD-TEST-001"],
        "resolution": "superseded",
    })
    errors = source_delta.readiness_errors(
        assessed["deltas"][0],
        source_delta.load_policy(),
        set(assessed["head_evidence_ids"]),
        assessed["head_evidence_statuses"],
    )
    assert assessed["deltas"][0]["promotion_gate"] == "BLOCKED"
    assert any("distinct from falsified/affected" in error for error in errors)
    assert any("previously live affected evidence" in error for error in errors)


def test_falsify_requires_live_distinct_replacement_and_actual_supersession(tmp_path):
    base_registry = {
        "version": "1.0.0",
        "authority_tiers": {},
        "sources": [source(), source(id="SRC-2", name="Source Two")],
    }
    head_registry = json.loads(json.dumps(base_registry))
    head_registry["sources"][0]["verified_at"] = "2026-10-05"
    base_ledger = {
        "version": "1.0.0",
        "items": [
            {
                "id": "EVD-TEST-001",
                "statement": "The original claim is long enough for the test.",
                "source_ids": ["SRC-1"],
                "domains": ["test"],
                "strength": "strong",
                "scope": "test scope",
                "status": "active",
            }
        ],
    }
    head_ledger = {
        "version": "1.0.0",
        "items": [
            {
                **base_ledger["items"][0],
                "status": "superseded",
            },
            {
                "id": "EVD-TEST-002",
                "statement": "The replacement claim is long enough for the test.",
                "source_ids": ["SRC-2"],
                "domains": ["test"],
                "strength": "strong",
                "scope": "test scope",
                "status": "active",
            },
        ],
    }
    report = source_delta.detect_from_documents(
        base_registry,
        head_registry,
        head_ledger,
        base_ledger=base_ledger,
        root=tmp_path,
    )
    assessed = source_delta.apply_assessment(report, {
        "source_id": "SRC-1",
        "classification": "FALSIFY",
        "rationale": "The reverified source invalidates the original scoped claim and a distinct replacement is active.",
        "reviewed_evidence_ids": ["EVD-TEST-001"],
        "downstream_actions": ["Migrate consumers to EVD-TEST-002 and rerun the affected behavioral checks."],
        "replacement_evidence_ids": ["EVD-TEST-002"],
        "resolution": "superseded",
    })
    assert next(d for d in assessed["deltas"] if d["source_id"] == "SRC-1")["promotion_gate"] == "READY"


def test_removed_live_challenge_cannot_close_as_rejected(tmp_path):
    report = source_delta.detect_from_documents(
        registry(source()),
        registry(None),
        ledger(),
        root=tmp_path,
    )
    assessed = source_delta.apply_assessment(report, {
        "source_id": "SRC-1",
        "classification": "CHALLENGE",
        "rationale": "The source disappeared while live evidence still depends on it and needs resolution.",
        "reviewed_evidence_ids": ["EVD-TEST-001"],
        "downstream_actions": ["Resolve the missing source and migrate or rescope the dependent claim."],
        "resolution": "rejected",
    })
    assert assessed["deltas"][0]["promotion_gate"] == "BLOCKED"
    assert any(
        "requires resolution" in error
        for error in source_delta.readiness_errors(
            assessed["deltas"][0],
            source_delta.load_policy(),
            set(assessed["head_evidence_ids"]),
            assessed["head_evidence_statuses"],
        )
    )


def test_eval_contracts_remain_in_blast_radius_but_raw_outputs_do_not():
    assert source_delta.excluded_downstream_path("05-evals/golden-evals.json") is False
    assert source_delta.excluded_downstream_path(
        "05-evals/independent-run-v3/executor-raw-1.json"
    ) is True


def test_ci_uses_pr_head_and_default_branch_merge_base():
    workflow = (ROOT / ".github" / "workflows" / "validate.yml").read_text()
    assert "PR_HEAD_SHA" in workflow
    assert 'git merge-base "origin/$DEFAULT_BRANCH" "$HEAD_SHA"' in workflow
    assert '[ "$REF_NAME" != "$DEFAULT_BRANCH" ]' in workflow
