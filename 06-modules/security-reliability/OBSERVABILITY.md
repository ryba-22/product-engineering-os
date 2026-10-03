# Observability Brain

Use with `STAGE-20-OBSERVABILITY.md`. Instrumentation should answer operational and product questions. Start from user-visible capabilities and failure modes rather than collecting undifferentiated telemetry.

## Start with questions

Examples:
- Is the service available for the critical user task?
- Is it meeting latency/reliability objectives?
- Which release introduced the regression?
- Which dependency dominates failure?
- Are retries/queues recovering or amplifying the incident?
- Which domain error is increasing?
- Which tenant/segment is affected without exposing sensitive data?

Every dashboard/alert should answer a question or support a decision.

## Signal contract

Use complementary signals:
- **metrics** for rates, distributions, saturation and trends;
- **traces** for end-to-end causal path across services;
- **structured logs/events** for detailed state/context;
- **profiles** where performance diagnosis needs code-level evidence.

Attach shared context: service, environment, version/release, operation and correlation/request/job identifiers. Add business/domain identifiers only when privacy/cardinality constraints allow.

## SLI/SLO

Define SLI calculation precisely. Examples:
- successful eligible requests / eligible requests;
- proportion of critical jobs completed within X;
- latency percentile under valid requests.

Set SLO window/target from user/business consequence and service maturity, not from arbitrary 99.99 aspirations.

Error budget can govern release pace or reliability work when the measurement is trustworthy.

## Alerting

Alert on actionable conditions. Prefer user-impact/SLO burn or clear resource saturation with known response over every low-level symptom.

Each alert should have:
- meaning;
- severity;
- owner;
- runbook;
- first diagnostic links;
- expected response;
- dedup/silence behavior.

## Privacy and cost

Telemetry is data. Avoid sensitive payloads, secrets and uncontrolled user identifiers. Review retention and high-cardinality labels. Sampling and aggregation should preserve the questions you need to answer.

## Validation

Observability itself needs tests. Trigger a representative dependency failure, application error, queue backlog or release regression and verify operators can detect, correlate and diagnose it.

A dashboard that looks complete but cannot answer “what changed and who is affected?” is not operational evidence.
