# Roadmap to “very strong” across all 25 stages

## Wave 0 — COMPLETE in v0.1
Shared lifecycle, routing, risk model, Clifton-complement operating profile, source registry, evidence schema/ledger, unified DR schema, 12 quality gates, 24 golden evals, validator.

## Wave 1 — COMPLETE in v0.1
Product Strategy, Product Discovery and Requirements module contracts + playbooks + canonical templates.

## Wave 2 — COMPLETE in v0.2
System Architecture + Software Engineering (frontend/backend/API/data): corpus/evidence expansion, architecture decision protocol, fitness functions, frontend state ownership, backend/API contracts, data migration/concurrency/idempotency patterns and adversarial evals.

## Wave 3 — COMPLETE in v0.3
Quality + Security + Performance: risk-based test model, threat modeling, secure SDLC, performance budgets/load/soak/profiling, dependency/supply-chain verification and runtime evidence rules.

## Wave 4 — COMPLETE in v0.4
Delivery + Observability + Resilience: reproducible builds, artifact provenance, release evidence bundle, rollout state machine, SLOs, telemetry/alerting contracts, incident response and measured restore drills.

## Wave 5 — COMPLETE in v0.5
Product Intelligence: metric trees, behavior-first event taxonomy, tracking plan, experimentation/pilot decision protocol, SRM trustworthiness gate, outcome reviews and continuous feedback loop.

## Wave 6 — COMPLETE in v1.0
Integrated existing Domain and Experience brains by explicit crosswalk, preserved local IDs and specialist ownership, and added machine-readable module/stage links.

## Wave 7 — COMPLETE in v1.0
Added stage-specific adversarial eval specifications for 25/25 lifecycle stages, source freshness audit and structural coverage validation. These checks did not yet demonstrate behavioral effectiveness.

### “Very strong” acceptance rule for any stage
A stage is very strong only when it has: authoritative/scoped corpus, atomic evidence, decision system, executable workflow, canonical artifacts, quality gate, adversarial/golden evals, and a verified integration path to upstream/downstream stages.

## Wave 8 — COMPLETE in v1.1
Deep Stage Pass: added 25 stage-specific operational playbooks, made them canonical decision-system references, bundled byte-identical copies into the standalone skill, replaced self-declared `very-strong` with `deep-structural`, and added anti-skeleton validation. Behavioral effectiveness remains a separate evidence claim.

### Behavioral “very strong” rule
A stage can be called behaviorally very strong only after representative and adversarial executions demonstrate decision quality, evidence discipline, failure handling and correct handoff. File presence, word count, IDs and linked eval specifications are necessary but not sufficient.

## Wave 9 — COMPLETE: Independent behavioral validation
Independent executor/judge separation completed on the frozen 25-stage adversarial suite. Gemini 3.1 Pro executed blinded cases; Claude Opus 4.6 independently judged them. Final result: 25/25 pass, zero hard failures, average 9.12/10. Status is scoped to this eval set; judge-identified omissions remain an explicit improvement backlog.

## Wave 10 — COMPLETE: independent replication
Repeated all 25 frozen adversarial scenarios with a fresh Gemini 3.1 Pro High executor and a separate first-party Claude Opus 4.6 judge. Result: 25/25, 0 hard failures, average 9.16/10. This is repeatability evidence for the existing independent validation; the next wave must use unseen/modified scenarios rather than another replay of the same set.
