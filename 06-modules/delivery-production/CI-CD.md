# Delivery Engineering — CI/CD

Use with `STAGE-18-CI-CD.md`. CI/CD is an evidence-producing system that turns a source state into an attributable release artifact.

## Goal

Move one immutable, attributable change through repeatable gates. The pipeline should answer:
- what source/dependencies produced this artifact?
- which checks ran and on what version?
- what was skipped/retried?
- can the same artifact be promoted?
- what migration/configuration must accompany it?

## Default gate chain

A typical sequence:

`source policy → static/lint → unit/property → contract/integration → security/dependency → build → artifact digest/provenance → release tests → candidate`

Order cheap deterministic checks early. Keep expensive environment-dependent checks later but before the release decision where risk requires them.

## Build once

Prefer producing an immutable artifact once and promoting it between environments. Rebuilding for staging/production can produce different dependencies/bytes and break traceability between tested and deployed code.

Record:
- commit SHA;
- build ID;
- dependency lock/provenance;
- artifact digest;
- build environment/toolchain version where material.

## Secrets and configuration

CI jobs use least privilege. Separate environment configuration from build output. Validate required configuration shape without echoing secret values. Prefer short-lived credentials/identity federation where available.

## Database changes

Pipeline/release logic should understand migration compatibility:
- expand before code that depends on new schema;
- mixed-version window;
- backfill/long-running job;
- contract old schema later.

Do not assume rollback is safe after an irreversible migration.

## Flakiness and infrastructure failures

A retry due to CI infrastructure is different from a flaky product test. Record distinction. Quarantine product flakiness only with owner/issue/expiry.

Repeated “rerun until green” destroys the evidence value of the pipeline.

## Provenance and approvals

Manual approval should expose decision-relevant evidence: exact artifact, failed/skipped checks, migrations, risk, rollout/rollback. Approval without evidence is ceremonial friction.

## Delivery metrics

Use lead/throughput and instability/failure metrics to improve the delivery system, interpreted in context. Do not game frequency at the expense of reliability or split changes artificially.

The pipeline is complete when it can produce a release candidate whose identity and evidence survive intact into rollout.
