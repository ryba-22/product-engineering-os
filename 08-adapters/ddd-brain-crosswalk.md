> Optional integration: apply this adapter only after a compatible asset has been supplied and its version, scope and usage rights are recorded. Without it, use the bundled module contract and preserve missing evidence as unresolved.

# DDD / Event Storming Brain → Product Engineering OS crosswalk

The existing Domain-Driven Design Architect is canonical for stages **3 and 5**.

| DDD Brain concept | Product Engineering OS |
|---|---|
| FACT / EVIDENCE / BUSINESS RULE | project evidence feeding G2/G3 |
| HYPOTHESIS / ASSUMPTION | unresolved evidence with explicit confidence/scope; never promoted silently |
| DECISION | PDR/ADR/DDR as appropriate |
| OPEN QUESTION / CONTRADICTION | gate blocker or recorded uncertainty depending consequence |
| Event Storming / glossary / hotspots | G2 Domain exit artifacts |
| Context Map / aggregate hypotheses | stage 5 architecture inputs |
| architecture challenger | upstream input to System Architecture Brain |

## Boundary
DDD discovers and challenges business semantics. System Architecture chooses technical structure; database/API/UI models must not redefine domain truth by convenience.
