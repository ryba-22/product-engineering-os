# Cross-lifecycle risk model

Risk controls how much evidence, review, verification and reversibility the OS requires. Risk is not a permanent project label; classify the current decision/change and raise the class when new information increases consequence or irreversibility.

| Risk | Meaning | Typical examples | Default evidence burden |
|---|---|---|---|
| R0 | Cosmetic / negligible consequence | copy, spacing, internal naming | focused review; no invented evidence |
| R1 | Low, reversible product/engineering change | small UI refinement, non-critical report | existing evidence + targeted verification |
| R2 | Material workflow/data change with bounded recovery | new workflow, moderate migration, external integration | explicit requirements, decision record, risk-based tests, rollout evidence |
| R3 | High-impact or difficult-to-reverse change | money, identity, critical data mutation, large migration, broad rollout | strong evidence chain, adversarial verification, explicit rollback/recovery and approval |
| R4 | Safety/legal/security-critical or catastrophic failure potential | sensitive access control, destructive irreversible migration, severe compliance/safety boundary | specialist review where needed, strongest available evidence, independent verification and explicit acceptance authority |

## Classification dimensions

Do not classify from change size alone. Evaluate:

- **Consequence:** harm to users, money, data integrity, privacy, security, contractual obligations or operations.
- **Blast radius:** one user/object versus a whole tenant, institution, region or product.
- **Reversibility:** simple revert, compensating action, complex migration or irreversible external effect.
- **Detectability:** whether failure is obvious immediately or can remain latent.
- **Uncertainty:** how much of the behavior, workload or domain rule is still inferred.
- **Coupling:** number of services, integrations, schemas, teams or rollout dependencies involved.
- **Novelty:** familiar pattern with strong evidence versus new mechanism or first use in this context.

A small code diff can still be R3/R4 if it changes authorization, billing, destructive data handling or a hard-to-detect invariant.

## Evidence burden by risk

Higher risk changes require more than “more documents.” They need stronger evidence at the failure mechanism that matters.

- R0: review the exact surface changed.
- R1: verify the affected scenario and regression boundary.
- R2: connect requirement → decision → implementation → tests → release evidence.
- R3: add adversarial cases, concurrency/failure behavior, migration/recovery and staged rollout where applicable.
- R4: require explicit independent/specialist validation when the team/model cannot honestly establish the guarantee alone.

## Escalation triggers

Raise risk when any of these appears: destructive mutation; authorization boundary; external money/message/action; multi-step migration; retry ambiguity; cross-system dual write; hidden failure; large data volume; regulated/sensitive data; no safe rollback; unknown production behavior.

Lowering risk requires evidence, not optimism. Record why the consequence/blast radius/reversibility is actually smaller.

## Runtime rule

Risk classification controls routing and stop-analysis. Low-risk reversible work should not be trapped in heavyweight process. High-risk work must not use “agile” or “small diff” as a reason to skip verification.

Every material decision record should state the current risk class and the fact that would cause reclassification.
