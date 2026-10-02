# Cross-lifecycle risk model

| Risk | Meaning | Typical examples | Evidence burden |
|---|---|---|---|
| R0 | Cosmetic / negligible consequence | copy, spacing | lightweight review |
| R1 | Reversible product behavior | small UI behavior, internal setting | focused tests + verification |
| R2 | Consequential but repairable | workflow change, routine data mutation | integration evidence + rollback/recovery path |
| R3 | High consequence | finance, permissions, bulk send, production migration | explicit decision record, failure analysis, end-to-end evidence, operator gate |
| R4 | Critical / irreversible | safety-critical, destructive data loss, legal-critical irreversible action | strongest available evidence, independent review, rehearsed recovery, explicit human authorization |

Risk is evaluated on consequence, reversibility, blast radius, uncertainty and detectability. The highest material dimension wins; do not average away a critical constraint.
