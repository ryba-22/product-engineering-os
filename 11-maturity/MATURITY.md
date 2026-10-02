# Coverage, depth and behavioral validation

Product Engineering OS uses three different claims and does not collapse them:

1. **Structural coverage** — required files, IDs, schemas, evidence links, gates and integration references exist.
2. **Deep structural coverage** — every lifecycle stage also has a substantive stage-specific playbook with decision questions, workflow, decision rules, evidence standard, canonical outputs, failure modes, exit conditions and handoff.
3. **Behavioral effectiveness** — the runtime has been executed against representative/adversarial cases and the results have been independently or repeatably assessed.

As of v1.1, all 25 lifecycle stages are **deep-structural**. The stage playbooks are validated for minimum depth and required operational sections. This is materially stronger than the earlier skeleton-only coverage.

This still does **not** prove general behavioral effectiveness. Existing golden evals are specifications unless accompanied by executed results. The worked idempotent-enrollment example is self-assessed, not an independent benchmark.

The maturity report must therefore never use a green structural test as proof that the Brain made a good real-world decision. Behavioral claims require executed evidence with version, inputs, outputs, evaluator and limitations.

Optional specialist corpora remain conditional until the exact assets are supplied, versioned and reviewed. The bundled stage playbooks provide native fallback depth so Domain and Experience stages no longer depend only on crosswalk files.

Run `python scripts/validate.py`, `python scripts/audit_coverage.py`, `python scripts/audit_freshness.py` and `pytest` before a release.
