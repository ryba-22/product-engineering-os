# Architecture fitness functions

A fitness function is an executable or inspectable constraint that detects architecture drift.

Use only where the property is important enough to justify ongoing enforcement.

| Concern | Example fitness function |
|---|---|
| Dependency direction | architecture test forbids feature → infrastructure shortcut imports |
| API compatibility | contract diff blocks unapproved breaking changes |
| Data ownership | write access to owned tables is restricted to the owning module/service |
| Migration safety | migration lint + forward/backward compatibility test on representative schema |
| Reliability | SLO/error-budget telemetry and synthetic checks |
| Performance | p95/p99 or user-centric budget gate under defined workload |
| Security | authorization matrix tests, secret scan, dependency policy, ASVS-derived checks |
| Accessibility | rendered DOM scan + keyboard/manual acceptance for critical flows |

Do not create a fitness function merely because it is measurable. Tie it to an accepted architecture/quality decision.
