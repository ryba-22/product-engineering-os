# Maturity — v1.0

All 25 lifecycle stages satisfy the **very-strong structural baseline** defined by this OS: scoped corpus, at least two evidence anchors, a decision system/workflow, canonical artifacts, a quality gate (or continuous governance gate), a stage-specific adversarial eval, and explicit upstream/downstream integration.

This does **not** mean every project automatically passes every gate, nor that the corpus is permanently complete. “Very strong” describes the capability of the Brain, not the state of a specific application. Source freshness, project evidence and runtime verification remain mandatory.

Run:

```bash
python scripts/audit_coverage.py
python scripts/audit_freshness.py --as-of 2026-10-02 --max-age-days 365
python -m pytest -q
python scripts/validate.py
```
