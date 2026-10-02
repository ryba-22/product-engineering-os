# 25-stage lifecycle

The lifecycle is not a waterfall. Stages can loop, run in parallel when independent, or be skipped when existing evidence satisfies the corresponding gate. Skipping requires evidence, not convenience.

| # | Stage | Primary module | Canonical exit evidence |
|---:|---|---|---|
| 1 | Problem / idea / business goal | product-strategy | gate-linked artifact/evidence |
| 2 | User / Product Discovery | product-discovery | gate-linked artifact/evidence |
| 3 | Domain Discovery | domain | gate-linked artifact/evidence |
| 4 | Requirements / specification | requirements | gate-linked artifact/evidence |
| 5 | Domain Architecture | domain | gate-linked artifact/evidence |
| 6 | System Architecture | system-architecture | gate-linked artifact/evidence |
| 7 | UX Architecture | experience | gate-linked artifact/evidence |
| 8 | Interaction design | experience | gate-linked artifact/evidence |
| 9 | Accessibility | experience | gate-linked artifact/evidence |
| 10 | Visual UI | experience | gate-linked artifact/evidence |
| 11 | Design System | experience | gate-linked artifact/evidence |
| 12 | Frontend implementation | software-engineering | gate-linked artifact/evidence |
| 13 | Backend / API | software-engineering | gate-linked artifact/evidence |
| 14 | Database / persistence | software-engineering | gate-linked artifact/evidence |
| 15 | Testing | quality-engineering | gate-linked artifact/evidence |
| 16 | Security | security-reliability | gate-linked artifact/evidence |
| 17 | Performance | quality-engineering | gate-linked artifact/evidence |
| 18 | CI/CD | delivery-production | gate-linked artifact/evidence |
| 19 | Deployment / rollout | delivery-production | gate-linked artifact/evidence |
| 20 | Observability | security-reliability | gate-linked artifact/evidence |
| 21 | Backup / DR / incidents | security-reliability | gate-linked artifact/evidence |
| 22 | Product analytics | product-intelligence | gate-linked artifact/evidence |
| 23 | Experimentation | product-intelligence | gate-linked artifact/evidence |
| 24 | Feedback → next iteration | product-intelligence | gate-linked artifact/evidence |
| 25 | Knowledge governance | knowledge-governance | gate-linked artifact/evidence |

## State semantics
`UNKNOWN → EXPLORED → DECIDED → IMPLEMENTED → VERIFIED → RELEASED → OBSERVED → MEASURED → LEARNED`

The OS must not collapse these states. A later state requires its own evidence.
