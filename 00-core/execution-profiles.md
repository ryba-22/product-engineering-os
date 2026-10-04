# Risk-derived execution profiles

Execution profile is derived from the current change risk and evidence needs. It is not a permanent project mode and it does not replace stage routing.

| Profile | Default risk | Use when | Minimum burden |
|---|---|---|---|
| FAST | R0-R1 | reversible, localized work with known behavior and no consequential boundary | exact-surface review, targeted executable verification, applicable project rules |
| STANDARD | R2 | material workflow/data/integration change with bounded recovery | traceable requirement/decision, implementation plan, verification matrix, integration evidence |
| EVIDENCE_HEAVY | R3-R4 | money, identity, destructive/latent failure, difficult rollback, sensitive or broad effects | strong evidence chain, adversarial verification, recovery/rollback, independent review/approval, production-readiness evidence |

## Selection algorithm

1. Classify the current change with risk-model.md.
2. Start from the default profile above.
3. Escalate one profile when uncertainty, coupling, novelty or hidden failure is materially higher than the nominal consequence suggests.
4. Never downgrade because the code diff is small.
5. Record the profile in the task contract together with the risk evidence and the condition that would cause reclassification.

## FAST is not "skip process"

FAST removes ceremony, not guarantees. A FAST task still needs:
- a stated outcome;
- a current baseline;
- applicable enforced project rules;
- a targeted check proving the changed property;
- explicit escalation if the change crosses a money, identity, security, destructive data, external side-effect or hard-to-detect boundary.

## Verification defaults

| Dimension | FAST | STANDARD | EVIDENCE_HEAVY |
|---|---|---|---|
| Completeness vs task contract | required | required | required |
| Targeted/unit/contract tests | required when behavior changes | required | required + adversarial cases |
| Full regression suite | only when cheap/material | normally required | required |
| Code/contract review | focused | required | independent |
| Pragmatic / over-engineering review | when abstraction increased | recommended | required when architecture changed |
| Reality check | when user/business behavior changed | required | required + independent evidence where possible |
| Production readiness | release-affecting only | release-affecting | required for production-affecting work |
| Recovery / rollback | not normally | when applicable | required |
