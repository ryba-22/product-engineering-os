# Production Learning Record

## Observation ID / date / owner
## Linked outcome / release / rule / example / decision
## Version / exposure / population / time window

### Expected
What did the current model, rule, example, SLO or outcome hypothesis predict?

### Observed
What actually happened? Preserve trace/query/dashboard/support evidence and limitations.

### Delta
Describe the mismatch without explaining it.

### Classification
- [ ] implementation defect
- [ ] domain-model gap / unknown rule
- [ ] stale or incorrect requirement
- [ ] data/source-of-truth issue
- [ ] instrumentation defect
- [ ] operator/workflow friction
- [ ] expected exception missing from model
- [ ] new population/context
- [ ] security/reliability incident
- [ ] outcome hypothesis falsified
- [ ] unresolved

## Consequence / recurrence / confidence
## Next evidence action

## Propagation
| Artifact | NO_CHANGE / UPDATE_REQUIRED / SUPERSEDE / NEW_EVAL / UNKNOWN | Owner / link |
|---|---|---|
| Domain model / rules | | |
| Example Map / acceptance | | |
| Decision records | | |
| Automated tests | | |
| Golden/adversarial evals | | |
| Knowledge records | | |
| Observability / runbook | | |

## Re-verification / next production observation
## Definition of Value status: VERIFIED | UNVERIFIED | FALSIFIED | NOT-YET-MEASURABLE


## Machine-readable companion

For material production evidence, mirror this record in JSON using:

- contract: `machine/production-evidence-contract.json`
- schema: `machine/production-evidence.schema.json`
- validator: `python3 scripts/production_evidence.py <record.json> --check`

The machine record must identify the expectation, release, observation scope/window, evidence references, instrumentation quality, outcome/guardrails/segment harm, delta classification, learning effect, propagation owners and closure state.

Do not manually promote `HEALTHY` to `SUCCESSFUL`. Use the validator-derived value state.
