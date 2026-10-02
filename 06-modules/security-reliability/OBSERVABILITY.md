# Observability Brain

## Start with questions, not dashboards
Instrumentation exists to answer operational/product questions: Is the service available? Is it meeting SLOs? Where is latency/failure introduced? Is a background process/backlog progressing? Which release changed behavior?

## Signal contract
- **metrics** for rates, distributions, saturation, queues/backlogs and SLOs;
- **logs** for discrete structured events and diagnostic context;
- **traces** for request/workflow paths across boundaries;
- correlation/request/trace IDs to connect them where appropriate.

Avoid secrets and unnecessary PII. Define retention and access.

## Alerting
Alert on actionable conditions with an owner and runbook. Prefer user-impact/SLO or strong leading indicators to raw resource noise. A dashboard without a decision/action contract is not operational readiness.
