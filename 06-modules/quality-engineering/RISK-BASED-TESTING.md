# Quality Engineering Brain — risk-based testing

## Principle
Do not optimize for test count or a fixed pyramid. Start from what can fail, consequence, detectability and the guarantee required.

## Mapping
- pure rule/invariant → unit/property test;
- DB constraint/transaction/locking → real database integration/concurrency test;
- API compatibility → contract/schema test;
- cross-component workflow → integration/E2E;
- browser behavior → Playwright/browser verification;
- accessibility → automated scan + keyboard/manual AT as needed;
- migration → apply/upgrade/reconciliation test on representative data;
- provider side effect → adapter/integration + idempotency/retry evidence;
- operational recovery → drill, not just code review.

## Exit contract
For each material risk: failure mode, consequence, test/evidence method, environment, oracle/pass criteria, and residual uncertainty. A passing test that cannot fail for the target defect is not evidence.
