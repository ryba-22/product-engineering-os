# Research-first solution selection

**Scope:** Material recommendations concerning product, domain, UX, interaction, architecture, technology and engineering process. This is an extension of existing PEOS decision protocols, not another framework, CI gate or approval authority.

## Principle

**Problem → observed evidence → decision drivers → credible options → trade-offs and failure modes → critical challenge → verdict → recommendation.**

A known component, popular architectural pattern, previous solution, "best practice" or clean implementation is a **candidate**, not proof of fit. A proposal must answer: *Why this option for this problem, under these constraints, and why not the other credible options?*

### Decision preparation

1. **Problem and user outcome.** Specify who needs to do what, what currently prevents it, and the cost of failure. Distinguish a symptom from the cause.
2. **Reality and confidence.** Cite current code, observed tasks, data, production evidence, documents or established contracts. Distinguish FACT / HYPOTHESIS / ASSUMPTION / DECISION / OPEN QUESTION. Do not turn prior assistant suggestions into facts.
3. **Drivers, constraints and ownership.** Consider business invariants, task frequency, information density, time, scale, safety/privacy, reversibility, coupling, change locality, consistency, retry/recovery and operations *as relevant*. No universal weighted ranking.
4. **Options.** Compare materially different approaches including **option 0: preserve the current solution / do nothing**. Examine the simplest credible approach and a structurally different alternative when useful. Usually 2–5 realistic options; do not manufacture options to satisfy a quota.
5. **Consequences.** Explain correctness, effort, maintainability, accessibility, migration, operational burden, failure modes and accepted disadvantages for each serious option. Distinguish **implemented ≠ verified ≠ useful in production**.
6. **Falsification and switching.** State what evidence would overturn the selection, under which changed drivers another option would be preferable, and how effectiveness will be verified.
7. **Critical lenses.** Challenge important decisions from product/domain, architecture/engineering and UX/interaction perspectives; involve security, operations or visual UI when their constraints matter. Analytical lenses are **not actual review or approval by named people**. Reuse existing owners and project authorities.
8. **Verdict.** Choose: `RECOMMEND`, `RECOMMEND WITH CONDITIONS`, `EXPERIMENT FIRST`, `INSUFFICIENT EVIDENCE`, `REJECT` or `KEEP CURRENT SOLUTION`. Only then state a recommended implementation.

## Bias diagnostics

- **Justified reuse:** same task and driving constraints, still-valid evidence. Reusing the pattern is reasonable.
- **Unexamined default:** a drawer, card, modal, dashboard, queue, event, service, repository abstraction or extra reviewer appears without a demonstrated need.
- **Solution-driven design:** the implementation mechanism precedes the actual business/user problem.
- **Accidental complexity:** unnecessary states, layers, permissions, dependencies, retries, review steps or navigational contexts.
- **Overengineering:** a present cost is justified by hypothetical future scale instead of current evidence.
- **Context mismatch:** a successful pattern in one system is copied to a different domain or workflow without examining differences.
- **Reverse dogma:** rejecting a potentially suitable option only because others previously overused it.

Repeated use alone is not evidence of bias. To diagnose a prior recommendation, connect **proposed pattern → specific problem → alternatives considered → accepted trade-offs → actual outcome**. Record unknowns instead of inventing decision history.

## Proportionality and existing authority

- **R0/R1:** short, reasoned selection is enough; no ritual research, ADR or review ceremony for ordinary reversible work.
- **R2:** explicit option comparison, constraints and evidence. Use the existing [decision template](../03-decisions/DECISION-RECORD-TEMPLATE.md) when a durable record adds value.
- **R3/R4:** stronger evidence, risk-specific failure analysis and actual approval according to the project's existing security/business/release contracts. This method never waives those controls or creates mandatory human GitHub reviewers.
- **Accepted decisions:** reference their context and revisit triggers; research again only if drivers, evidence or constraints materially changed.
- **Uncertainty:** prefer the smallest safe experiment that could distinguish options to performative certainty.
- **Stop research:** when a realistic option meets hard constraints with acceptable risk, alternatives have switching criteria, and further desk work is unlikely to change the choice. See [BRAIN stop-analysis gate](../BRAIN.md).

Do not create duplicate decision records, new CI rules, an alternative SZTAB workflow or a parallel knowledge repository to implement this guidance. Project-specific decisions stay in the project. Reusable method stays in PEOS.

## Examples

**Queue details UI.** First define whether users compare multiple records, navigate rapidly, edit in context or inspect occasionally. Compare a better row, inline expansion, dedicated detail page, modal and master-detail/Inspector **as distinct options**, considering URL state, focus, accessibility, mobile space and security. A drawer is not intrinsically wrong or right. See [UX Architecture](../06-modules/experience/STAGE-07-UX-ARCHITECTURE.md) and [Interaction Design](../06-modules/experience/STAGE-08-INTERACTION-DESIGN.md).

**Durable background work.** First identify the invariant and timeout/duplicate/partial-success risks. Consider eliminating the long operation, bounded synchronous processing, a transactional DB job, a message broker and workflow orchestration only if plausible. A queue does not imply event-driven architecture. See [Architecture Decision Protocol](../06-modules/system-architecture/DECISION-PROTOCOL.md).

**Engineering controls.** Before another quality gate, identify the actual failure the current checks missed, its consequence, the oracle, bypass risks, maintenance cost and whether an existing control could be improved instead.

## Compact review note (inside the existing ADR if one exists)

```text
Outcome / actor / failure cost:
Current facts and evidence; unknowns:
Drivers / constraints / risk / reversibility:
Options, including zero, and why they pass/fail:
Key trade-offs / retry, failure and recovery:
What would falsify the choice / revisit conditions:
Critical perspectives (analytical vs actual reviewers):
Verdict / decision owner / verification / STOP:
```

## Verify this method

Evaluate its use on a small mixed sample of real R2+ decisions: was the zero/simple option considered; were rejected options justified by drivers; did a critical perspective challenge the first idea; was the experiment or recommendation falsifiable; and did decision quality improve without needless process? If it becomes a ceremonial checklist, simplify it.

**Related:** [PEOS risk model](risk-model.md), [architecture decision protocol](../06-modules/system-architecture/DECISION-PROTOCOL.md), [existing decision-record template](../03-decisions/DECISION-RECORD-TEMPLATE.md), [cross-project audit](../docs/research/solution-bias-audit-2026-10-12.md).
