# Risk & Decision Intelligence — research-backed implementation plan

**Prepared:** 2026-10-12
**Status:** PROPOSED / DOCUMENTED ONLY — no product implementation, no production integration, no new mandatory gate
**Owner of reusable method:** Product Engineering OS (PEOS)
**Owners of specific decisions and evidence:** adopting project and its authorized decision owners
**Target planning horizon:** discovery/pilot 2026-10-12 through 2026-10-18; later phases conditional, not committed dates
**Goal anchor:** turn ten observed classes of cognitive, engineering and process risk into reusable, falsifiable, proportionate controls inside PEOS, and demonstrate improvement on representative real decisions without adding unjustified process overhead.
**STOP for this deliverable:** research synthesized, ownership/boundaries defined, phased implementation and evidence-based acceptance specified, durable plan linked in PEOS. Do not implement the planned system merely because the plan exists.

## 0. Executive decision and current evidence

**DECISION (proposed):** extend PEOS with **Risk & Decision Intelligence (RDI)** as a thin, read-only diagnostic capability built on its existing decision, routing, risk, evidence and evaluation contracts. Do not create a parallel framework, autonomous gatekeeper, new mandatory GitHub reviewer, single composite quality score or separate repository.

**FACT — inspected on 2026-10-12:** 
- `00-core/research-first-decisions.md` already defines problem-first reasoning, zero/simplest option, falsification, risk-based proportionality and stop-analysis.
- `00-core/adaptive-workflow-router.md` and `machine/workflow-router.json` already route work using task class, R0–R4 and mandatory concerns.
- `00-core/risk-model.md` already sets consequence, reversibility, detectability, uncertainty and evidence burden.
- `03-decisions/DECISION-RECORD-TEMPLATE.md` already contains evidence, options, validation and revisit triggers.
- `06-modules/delivery-production/delivery-assurance/README.md` / [DA-01 issue #14](https://github.com/ryba-22/product-engineering-os/issues/14) already own **release evidence**. They are advisory, non-authoritative and distinguish trusted from self-attested claims.
- `01-governance/source-delta-pipeline.md`, the evidence ledger, knowledge lifecycle, production learning loop and behavioral evals already exist.
- `scripts/audit_package_index.py` requires any added file to be recorded in `PACKAGE-INDEX.json`. `.github/workflows/validate.yml` is an existing validation workflow. Avoid a second mandatory check.
- At inspection, PEOS had other open issues (#17, #18, #20) and PRs (#7, #11, #13, #16, #19). They relate to delivery assurance, roadmap mapping or knowledge governance; inspect diffs before touching overlapping files.

**HYPOTHESIS:** the largest incremental benefit is not new checklists. It is: (1) distinguish a **risk signal** from a **substantiated diagnosis**, (2) connect the signal to the existing decision record and authoritative evidence, (3) test false positives and behavior, (4) measure prevented rework relative to overhead.

**ASSUMPTION:** first consumers are humans and AI assistants during R2+ domain, architecture, UX and process decisions; R0/R1 work remains lightweight. Confirm this in the pilot.

**OPEN QUESTIONS:** actual prevalence of ten risks; stable ground-truth labels; whether the simple checklist beats an automated checker; cost per decision; which warnings change behavior; availability of project-safe observations.

## 1. Research synthesis (sources and their limits)

Research reviewed on **2026-10-12**, outside the existing PEOS historical research-corpus cutoff of 2026-09-30. These sources inform this dated operational plan; **do not silently import them into the frozen registry or claim that prior corpus verified them**.

| ID | Primary source | Verified insight | Translation to RDI | Limitation |
| --- | --- | --- | --- | --- |
| EXT-01 | [NIST AI RMF Core: GOVERN/MAP/MEASURE/MANAGE](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/) | AI risk management is contextual, continuous and involves governance, mapping, measurement and management; functions are not a mandatory ordered checklist. | Risk definitions need purpose, context, owner, measure, response and re-evaluation trigger; do not mandate every control for every task. | Voluntary broad guidance, not a PEOS-specific detector accuracy standard. |
| EXT-02 | [NIST AI RMF Playbook](https://airc.nist.gov/airmf-resources/playbook/) and [MEASURE](https://airc.nist.gov/airmf-resources/playbook/measure/) | Suggested actions are selective; risks that cannot be measured should be documented. | Support UNKNOWN/NOT_APPLICABLE, confidence and unmeasurable risks; no invented precision. | Guidance does not certify RDI outcomes. |
| EXT-03 | [NIST AI 600-1 (2024)](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence) | GenAI needs context-specific risk identification, evaluation and mitigation. | Human/AI decisions are socio-technical and require provenance plus use-case evaluation, not prompt-only safety guarantees. | Risk profile, not evidence that one LLM evaluator can reliably judge another. |
| EXT-04 | [SPACE, Forsgren et al., CACM (2021)](https://cacm.acm.org/practice/the-space-of-developer-productivity/) | Productivity has multiple dimensions (satisfaction, performance, activity, collaboration, flow); one activity metric is insufficient. | Avoid PR count, number of warnings or checks passed as success metrics. | Conceptual research, not a prescribed universal KPI target. |
| EXT-05 | [DORA delivery metrics guide, updated 2026-01-05](https://dora.dev/guides/dora-metrics/) | Throughput and instability must be considered together; single-metric targets invite gaming and cross-context comparisons mislead. | Pair faster decisions with stability/rework measures and project-local context; do not turn RDI warnings into a numeric rank. | DORA metrics describe delivery, not direct causal effects of this module. |
| EXT-06 | [Google SRE: Eliminating Toil](https://sre.google/workbook/eliminating-toil/) | Repeated operational overhead should be measured and reduced at source, not merely automated. | Measure analyst/agent time, false-alarm handling and ceremony introduced by RDI. | Site reliability work is an analogy, not proof for developer decision reviews. |
| EXT-07 | [GitHub: protected branches/status checks](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches) | Required checks alter merge rights and can block work; check provenance and exact candidate matter. | Advisory mode first; owner-authorized project-specific escalation only; no silent required-check changes. | Platform docs describe mechanisms, not which governance level PEOS should choose. |
| EXT-08 | [SLSA](https://slsa.dev/) | Provenance and integrity of software supply chain matter. | Evidence records must preserve source, version, timestamp, scope and immutable identity where appropriate. | RDI is NOT SLSA provenance or a release attestation service; re-use DA-01 for release claims. |
| EXT-09 | [Parasuraman & Riley, Humans and Automation (1997), bibliography at MIT](https://web.mit.edu/16.459/www/Autorefs.htm) | Classic human-automation literature distinguishes appropriate use from misuse, disuse and abuse. | Require counter-evidence and human decision ownership for automation-bias diagnosis. | Historical conceptual anchor; not contemporary measured RDI effectiveness. |
| INT-01 | [PEOS solution-bias audit, 2026-10-12](../docs/research/solution-bias-audit-2026-10-12.md) | A bounded, evidence-limited cross-project sample found plausible unexamined defaults and documented justified exceptions. | Reuse the sample as candidate examples, not as labels of actual systemic bias or live defects. | Historical assistant/PR records are not full production outcome evidence. |

**Research judgement:** NIST supports contextual governance and measurable uncertainty, DORA/SPACE caution against single-score optimization, SRE cautions against control-generated toil, and GitHub/SLSA show trust-boundary problems. None validates an automatic “this decision is biased” classifier. Such performance is an **empirical hypothesis to test**, not a capability to advertise.

## 2. Problem, non-goals, stakeholders and alternatives

### The real problem
When agents and teams produce fast architecture/UX/process recommendations, known failure patterns may go unnoticed: a solution chosen before the problem, a green check misrepresented as production success, a new audit not connected to a decision, or optimization of a local metric that harms the entire workflow. Conversely, aggressive checkers can generate their own failures: false allegations, compliance theater, delays and unnecessary abstract layers.

### Desired outcomes
1. More material decisions have explicit problem, credible options, source-backed premises, failure conditions and ownership.
2. Unsupported certainty and unexamined changes of goal are challenged *before* irreversible action.
3. Warnings are actionable and can be refuted; low-risk work is not penalized.
4. We can show whether adoption improves decisions without merely increasing documents or agent activity.

### Non-goals
- No automatic determination of a person's cognitive bias or motives.
- No autonomous merge/release/financial/security go/no-go.
- No production secrets, personal records or confidential domain evidence copied into public PEOS.
- No parallel ADR/evidence registry, new universal CI gate, mandatory independent GitHub reviewers, new agent role hierarchy or automated production mutation.
- No replacing DA-01, DORA, PEOS R0–R4 or existing project-owned controls.
- No score ranking engineers, projects or AI models.

### Alternatives and decision
| Option | Benefits | Cost / failure | Verdict |
| --- | --- | --- | --- |
| 0. Do nothing | Zero new overhead; existing PEOS contracts cover much of the problem | Inconsistent application, no comparative behavior evidence | Credible for R0/R1 and as experimental control group |
| A. Add prose-only checklist to existing docs | Cheapest to adopt; minimal implementation | Hard to trace real use and false positives | **Stage 1 baseline**, keep if adequate |
| B. Thin machine-readable catalog + advisory CLI + scenario evals | Falsifiable checks, reusable semantics, no new authority | Schema/maintenance/test cost | **Conditional target** if A fails to address observed pilot cases |
| C. Autonomous GitHub quality gate / scoring dashboard | High automation and visibility | Unknown classifier accuracy, gaming, false blocks, permissions and process fatigue | **Reject now**; reconsider only with high-quality independent outcome evidence |

**Switching rule:** if lightweight prose improves outcomes at lower cost than automation, **stop at A**. If signals cannot be adjudicated reliably, retain human-oriented playbooks and record automation as not justified.

## 3. Domain model, ownership and trust boundaries

**Do not equate:** risk signal ≠ diagnosis; missing record ≠ bad reasoning; confidence ≠ probability of truth; evidence link ≠ verified evidence; test PASS ≠ product success; quality metric ≠ objective; advisory finding ≠ approved decision.

- **RiskDefinition** (PEOS-owned, versioned reusable knowledge): `id`, name, mechanism, harms, applicability, warning signals, alternative explanations, disconfirming evidence, control links, safe responses, example IDs, maturity/limitations, maintainers and revisit trigger.
- **DecisionCase** (project-owned): original user goal/STOP, actors, current constraints, options, decision authority, accepted trade-offs and immutable case reference. The project remains source of truth.
- **Assessment** (derived, replaceable): case ref + risk-definition version + evaluator/tool identity + observation refs + inference + confidence limitations + result + evaluation timestamp. Never becomes business truth.
- **ControlResult** (scoped execution fact): applicable control, exactly what was checked, expected/actual/unknown, independent reference and decision impact. Do not conflate the check with a risk diagnosis.
- **OutcomeObservation** (project-owned): after a decision, did a meaningful error, rework or wasted review get avoided? Counterfactual certainty is generally unavailable; note observational limitations.

### Diagnostic result contract
**Applicability:** `APPLICABLE | NOT_APPLICABLE | UNKNOWN_APPLICABILITY`. 
**Observation:** `SIGNAL_OBSERVED | SIGNAL_NOT_OBSERVED | INSUFFICIENT_EVIDENCE | CONFLICTING_EVIDENCE`.
**Control:** `PASS | FAIL | UNKNOWN | NOT_APPLICABLE` — only where the control has a clear oracle.
**Action:** `NO_ACTION | ASK_FOR_EVIDENCE | REVIEW_DECISION | RUN_EXPERIMENT | ESCALATE_TO_EXISTING_OWNER`.

Avoid a single mixed `PASS/FAIL` that silently equates missing documents with bad decisions. Conflicts preserve both sources and provenance. Waivers, when relevant, remain governed by existing project authority; do not self-approve from a JSON field.

### Boundary rules
- PEOS owns the **method, risk taxonomy, portable schema, examples and eval definitions**.
- Adopting repo owns **business facts, ADRs, operator decisions, privacy, CI/deployment and live outcome evidence**.
- DA-01 owns **release candidate evidence**; RDI may link to DA-01 but may not replicate or override its verdict.
- Knowledge Governance owns **source freshness, conflicts and promotion**; don't create a competing source registry.
- AI evaluator output is an **untrusted analysis** unless linked to independently verifiable sources. No source access or missing tool capability is reported as UNKNOWN, never concealed.
- Agent instructions are process guidance, not execution authorization; run read-only by default and use existing owner approvals for actions.

## 4. Ten risk contracts — treatment, false positives and evaluation

The following are **proposed heuristics**, not proven detectors. Use the minimum subset relevant to an actual task.

| ID | Risk & primary PEOS owner | Candidate warning signal | Legitimate counterexample / falsification | Advisory control and oracle |
| --- | --- | --- | --- | --- |
| RDI-01 | **Solution bias**; Research-first / decision record | Named technology/component without problem, drivers or credible zero/simple option | Current decision remains valid, or trivial reversible change with sufficient context | Ask “why this, why not simpler?” Compare 0/simple/credible alternative. Oracle: explicit constraints and actual option rationale, not fixed option count. |
| RDI-02 | **Audit theater**; documentation closure / Product Intelligence | Review creates new reviews without named decision, defect, learning or risk change | Compliance/legal periodic verification with explicit accountable outcome | Trace audit → finding → owner/action/closure or documented NO_ACTION. Oracle: observable consequence, not issue count. |
| RDI-03 | **False confidence**; Evidence / DA-01 boundary | “verified/deployed/successful” inferred only from green tests or assertions | Claim expressly restricted to test scope, exact SHA and trusted evidence | Require evidence appropriate to claimed lifecycle stage; unknown inputs produce UNKNOWN. Oracle: independent appropriate evidence. |
| RDI-04 | **Goal drift**; BRAIN / task contract | New initiative or unrequested gates replace original outcome/STOP | User explicitly reprioritized objective with recorded scope update | Compare original goal to proposed work and critical path; request owner change only for material scope drift. Oracle: original request and explicit amendments. |
| RDI-05 | **Complexity bias**; Architecture / research-first | New layer/service/framework without current driver and comparative cost | Proven scale, safety or ownership need already supports new structure | Justify added state, coupling, recovery and maintenance; consider minimal alternative. Oracle: actual driver and consequence model. |
| RDI-06 | **Automation bias**; Evidence / AI governance | AI statement used as objective fact without trustworthy source or independent check | AI used as brainstorm only; no consequential claim | Trace output → source/observation → trust boundary. Oracle: provenance and authority, not model confidence. |
| RDI-07 | **Knowledge accumulation**; Knowledge Governance | Many artifacts with no retrieved use, decision or supersession | Regulatory/reference documentation intentionally retained for infrequent needs | Trace knowledge → adoption/decision/test/learning, or justify archive. Oracle: actual citation/use; no document count target. |
| RDI-08 | **Metric gaming**; Product Intelligence | Proxy target rises while user outcome/reliability declines | Legitimate activity metric used as diagnostic alongside guards | Pair leading and outcome/guardrail metrics; examine change in behavior and gaming incentive. Oracle: coherent multi-metric context. |
| RDI-09 | **Local optimization**; Product/Architecture/Operations | Component measure improves while end-to-end wait, error or recovery worsens | Bounded local improvement with verified system-wide neutral impact | Trace workflow, owner, bottleneck and upstream/downstream effects. Oracle: end-to-end observation or justified experiment. |
| RDI-10 | **Process fatigue**; Adaptive Router / Risk Model | Same heavyweight gates imposed on all risk levels; repeated low-value manual work | High-risk legal/safety obligations genuinely demand extra checks | Explain included/skipped stages, time-to-decision and control benefit. Oracle: R0–R4 requirements + task facts, not gate count. |

For each entry define at least: normal case, true signal, benign signal (false-positive trap), missing-evidence case, contradictory-evidence case and one decision that should **not** be reopened. Version cases and expected outcomes. Only classify actual prior work when records are adequate.

### Pilot scenarios that must challenge the detector
- Existing accepted ADR justifies a queue; no new research is needed merely because a queue appears.
- A trivial CSS text change has no multi-option record; do not flag it as process or solution failure.
- GitHub CI is green while production evidence is absent; reject the claim “healthy in production”, but accept “tests passed on SHA X”.
- An AI proposes new mandatory reviewers despite explicit owner refusal; flag the proposed change as goal/process drift, but do not weaken mandatory authorization/security controls.
- There is no audit action because the audit found no issues; no fake issue is required.
- A user changes the goal deliberately; honor the amended anchor, do not accuse the agent.
- A metric is used diagnostically, not as a performance target; do not call metric gaming without behavioral evidence.
- A multi-step transactional process has proven recovery constraints; do not require a simpler synchronous rewrite.
- A missing reference cannot be retrieved due to access controls; return UNKNOWN rather than hallucinating or FAIL.
- A score improves only because evaluator output changed; do not count that as product value.

## 5. Implementation design — reuse before building

### Files and interfaces (proposed, subject to baseline inventory)
Keep existing root contracts canonical. Introduce **only** what the pilot demonstrates is needed:

```text
09-roadmap/risk-decision-intelligence-2026-10-12.md     # this plan
00-core/research-first-decisions.md                      # existing; link, no duplicate rules
00-core/adaptive-workflow-router.md                      # existing; risk-based selection
00-core/risk-model.md                                    # existing R0-R4
03-decisions/DECISION-RECORD-TEMPLATE.md                 # existing decision truth
02-evidence/                                               # existing evidence contracts
05-evals/                                                  # existing behavioral evaluations
[future, conditional]
machine/risk-intelligence/catalog.json                    # ten versioned definitions
machine/risk-intelligence/risk-definition.schema.json
05-evals/risk-intelligence/                                # labeled pilot cases and rubric
scripts/risk_intelligence.py                               # read-only advisory CLI
tests/test_risk_intelligence.py                             # schema, negative, adversarial tests
docs/risk-intelligence/                                    # short usage note and lessons
```

The future names are **not yet existing files**. Avoid automatically creating them all. First review overlapping existing schemas and index policy. No new runtime service, database or event bus is required for a versioned static catalog.

### Smallest CLI contract (only if justified)
```text
python scripts/risk_intelligence.py check path/to/decision-case.json --risk RDI-03
python scripts/risk_intelligence.py eval --cases 05-evals/risk-intelligence/
```
Read-only, deterministic static checks first. Emit JSON: `schema_version`, `case_ref`, `risk_id/version`, `applicability`, `observation`, `control_result`, `source_refs`, `limitations`, `suggested_action`. An explicit static signal can be detected; subjective interpretation must be marked INFERENCE. No inferred privileged access. No network or repo mutation by default. Errors or unavailable sources cannot become positive verdicts.

### GitHub integration (defer)
If pilot is valuable: emit an **opt-in advisory** summary for a selected PR, pinned to exact head SHA and matching input revision. Avoid write access until genuinely needed. Reuse existing CI, protection and DA-01; project owner alone decides whether any future advisory is adopted. Never change repository rulesets, require reviewers or block merge as an automatic consequence of introducing RDI.

### Web UI (defer)
Static, searchable and accessible catalog is enough (progressive disclosure, keyboard navigation, relevant examples, limitations, links to canonical source). GitHub Pages is a presentation surface, not the source of truth. No dashboard with a fake 0–100 “engineering correctness” rating.

## 6. Work breakdown, acceptance and dependencies

### Phase P0 — baseline & overlap analysis (first, required)
**Work:** inventory relevant PEOS contracts, issue #14 and active PRs; map existing rules to ten risks; inspect validation/index rules; capture 5–10 sanitized historic decisions representing positive and negative cases; identify owner and confidentiality constraints. Do not reopen closed decisions without a new falsifying fact.

**Output:** inventory matrix `risk → canonical file → gap → evidence → proposed delta`; samples with adequate provenance, else synthetic fixtures; no code.
**Exit:** each of 10 risks has exactly one canonical PEOS home and an honest gap decision. No competing gate or archive. **STOP** if existing docs alone solve observed needs.

### Phase P1 — minimal playbook pilot (required before code)
**Work:** using existing ADR/research-first fields, apply the proposed controls manually to 5–10 representative R2+ decisions and 3–5 R0/R1 counterexamples. Capture baseline recommendation and assisted recommendation independently where possible. Include “do nothing” control. Do not assign fabricated historic reviewer approval.

**Output:** labeled case sheet, false-positive notes, operator effort and real changes in decision reasoning.
**Exit:** identify at least two concrete error classes that the existing method misses *and* a plausible reduction in costly mistakes, or decide KEEP CURRENT SOLUTION. **No schema just for completeness.**

### Phase P2 — catalog & contract (conditional)
**Work:** model ten risks as data using a compact schema; explicit applicability, known counterexamples and provenance. Add minimal validation to existing validation workflow and package index. Reuse evidence IDs, ADR and knowledge provenance semantics.

**Output:** 10 versioned definitions, schema, 10 positive + 10 benign counterexample cases minimum, one UNKNOWN and one conflicting-source case for each risk where practical.
**Exit:** structural validator PASS; no forced score; all diagnostics have disconfirming evidence; no duplicated authority. Actual executed tests required before claiming tested.

### Phase P3 — bounded advisory evaluation (conditional)
**Work:** implement read-only CLI; deterministic checks for presence/scope/provenance, optional AI interpretation only where rule-based checking is insufficient; distinguish both explicitly. Red-team source spoofing, stale evidence, wrong SHA, self-justifying audit, legitimate zero-action, inaccessible repo, prompt injection and repeated messages.

**Output:** machine-readable advisory output, tests/evals with ground truth and provenance, error/unknown behavior.
**Exit:** no false PASS from untrusted material; no automatic action; blind holdout performance independently evaluated; known limitations published. Do not certify general cognitive-bias detection.

### Phase P4 — field experiment and value gate (conditional)
**Work:** run on a small, diverse opt-in sample. Compare unsupported claims discovered, decision reversals for valid reasons, actual escaped defects/rework where observable, added analysis time, wrong warnings and operator trust. Use project-specific outcomes, not cross-project league tables. Add source conflict review and rollback/disable path.

**Output:** `pilot-report` with sample selection, failures, effort, confirmed usefulness, confounders and explicit decision: STOP / SIMPLIFY / ADAPT / EXPAND.
**Exit:** benefit must outweigh false-positive + time costs for the intended risk class. If not, revert to prose-only method.

### Phase P5 — optional GitHub/Pages integration (deferred)
**Work:** only after P4 passes, evaluate (0) docs, (A) CLI, (B) advisory PR comment, (C) Pages. Integrate the smallest option that helps actual user workflow. Guard data exposure: only sanitized portable rules on Pages.
**Exit:** accessibility and provenance verified, optionality documented, opt-out supported; no change to project's release authority.

## 7. Proposed 2026-10-12 to 2026-10-18 weekly plan (not execution claims)

| Date | Work slice | Deliverable | STOP test |
| --- | --- | --- | --- |
| Mon 12 Oct | Research + repository overlap + plan | This dated proposal; references and existing-contract map | No implementation required by this request |
| Tue 13 Oct | P0 inventory on actual default branch/PRs | Ten-row ownership/gap matrix and case-selection protocol | Abort duplicate contracts |
| Wed 14 Oct | P1 pilot on representative decisions | Scored-by-evidence (not people) case outcomes, counterexamples | Need real signal beyond existing research-first |
| Thu 15 Oct | Decide whether P2 is justified | Proposal to implement compact catalog/schema **or** keep documents | No code if no observed incremental benefit |
| Fri 16 Oct | If authorized and P1 supports it: minimal P2 slice | First 2–3 definitions + validations/evals, not ten by quota | No mandatory PR/release gate |
| Sat–Sun 17–18 Oct | Synthesize pilot, document decision and next work | Verifiable checkpoint with supported status and unanswered questions | Do not declare production value from local tests |

**Capacity note:** this is a sequencing proposal, not an estimate, promised completion or automatic authorization for future work. P3–P5 intentionally have no delivery date. First prototype only if P1 evidence warrants it.

## 8. Evaluation design and thresholds

### Before any implementation
- Freeze scenario definitions and expected outputs **before** changing the prompt or detector.
- Include real sanitized examples and synthetic adversarial cases. Do not infer “truth” from prior AI reports.
- Independent evaluation when feasible: reviewer of behavior sees the scenario and decision criteria without the candidate's self-reported PASS. An LLM-as-judge is a hypothesis generator; record model identity and judge limitations.
- Ground truth must be an accountable human/project contract or directly inspectable fact; disputed cases are UNKNOWN, not conveniently removed.
- Partition development cases and unseen holdouts; do not tune on holdouts then claim unseen generalization. Preserve failures and exact revisions.

### Outcome metrics (multi-dimensional; no gamified universal composite)
- **Precision of actionable warnings** = verified true actionable warnings / all reviewed actionable warnings; report raw denominator and unknown count.
- **False-positive burden** = false or irrelevant warnings and minutes spent addressing them per assessed decision.
- **Missed material risks** = independently labeled material cases not flagged / labeled material cases (with caveat on sample bias).
- **Evidence discipline** = material factual claims with correct source/scope/provenance; do not count sheer citation density.
- **Decision effect** = proportion where an independently supported alternative, experiment or correction changed actual decision quality; use narrative cases as well as counts.
- **Process cost** = human/agent time and extra stages per risk class; separately track time-to-outcome, not just analysis duration.
- **Product/system guardrails** = no degradation in actual reliability, end-to-end delivery or owner autonomy attributable to the new controls.
- **Coverage** = applicability across the ten risk definitions, reported separately from accuracy or effectiveness.

**Pre-registered pilot threshold proposal (not empirically validated):** after ≥10 material decisions and ≥5 low-risk/benign examples, require 0 unsafe autonomous actions, 0 false-positive blocking actions (advisory-only), meaningful improvement in at least 2 independently adjudicated decisions, and median incremental review effort ≤10 minutes for R2 decisions. Use precision/recall as descriptive evidence; avoid making a hard numeric requirement from such a small sample. If no significant benefit, keep prose-only controls. Thresholds may be changed **before** running pilot, with owner and rationale, never retrospectively to manufacture PASS.

### Adversarial and regression requirements
1. Missing evidence != FAIL of decision or PASS of system.
2. Self-asserted source != independently trusted evidence.
3. A passed unit test != production health.
4. Existing justified architecture != bias.
5. Explicit user change of goal != goal drift.
6. No finding != obligation to create a corrective ticket.
7. R0/R1 don't inherit R3/R4 ceremony.
8. Project-level authorized gate cannot be waived by advisory output.
9. Malicious PR text / tool result cannot authorize action or override policy.
10. Evaluation output includes version, exact case, sources and limitations.
11. Re-running the same case should not create duplicate project actions.
12. Source conflict is reported, not resolved by picking the most convenient claim.

## 9. Delivery controls, risks and recovery

| New risk from RDI itself | Failure mode | Preventive control / recovery |
| --- | --- | --- |
| Audit theater of RDI | Every warning produces a review of another review | Measure outcome; allow NO_ACTION; uninstall/disable when no benefit |
| Metric gaming | Warnings or pass percentage become targets | Do not report ranking; monitor downstream product consequences |
| False authority | AI detects “bias” and changes accepted decisions | Advisory wording, refutation path, owner keeps decision |
| Scope creep | Risk atlas becomes new PEOS architecture | Separate conditional phases, no service/DB, explicit STOP |
| Privacy leak | Real project evidence copied to reusable public docs | Anonymize or use synthetic fixtures; refs only, no secrets/data |
| Rule conflicts | DA-01 and RDI emit contradictory release verdicts | DA-01 owns release evidence; RDI links only; source/owner conflict review |
| Stale rules | Heuristic survives after underlying practice changes | Version, reviewed_at, source URL, applicability and revisit trigger |
| Hallucinated evidence | AI invents URLs, tests or approvals | Show raw evidence/provenance, UNKNOWN on inaccessible source |
| Time overhead | Low-risk tasks slowed by questions | Risk routing, bypass for inapplicable rules, cost measurement |
| Vendor/model overfitting | Evaluator seems accurate on familiar cases | Holdouts, external or human adjudication, disclosed limitations |

**Recovery:** advisory checker can be disabled without modifying repository protections, financial data, release policy or primary PEOS contracts. Preserve published findings only with accurate provenance and retention policy; invalidate stale decisions on new evidence, do not erase contradictory history.

## 10. Ownership, decisions and checkpoint

- **Product owner / adopting project's authority:** prioritizes scope, may reject advice, controls project-level actions, accepts residual risk.
- **PEOS maintainer:** owns portable semantics, schema/eval and compatibility with current PEOS.
- **Engineering/domain/UX/security perspectives:** analytical perspectives for evaluating cases; never impersonate actual people, approvals or completed independent reviews.
- **Repository maintainer:** decides merge/CI and whether optional integration is installed; never presumed from RDI score.
- **Evidence producer/assessor:** must identify source, scope, observation and limitations; cannot elevate own assertions to independent proof.

Decision ledger for this plan:
- D-RDI-01 **PROPOSED**: one in-repo module rather than standalone repository.
- D-RDI-02 **PROPOSED**: risk signal / applicability / control result / action are separate concepts.
- D-RDI-03 **PROPOSED**: documentation/manual pilot before automation.
- D-RDI-04 **PROPOSED**: advisory only; existing project gates and approvals prevail.
- D-RDI-05 **OPEN**: is a ten-entry machine catalog worth its maintenance cost?
- D-RDI-06 **OPEN**: which pilot outcome reliably demonstrates value vs ceremony?
- D-RDI-07 **OPEN**: is any GitHub integration better than on-demand CLI/knowledge?
- D-RDI-08 **OPEN**: precise confidentiality boundary for cross-project examples.

**Next checkpoint:** complete P0 and P1, then issue a yes/no evidence-backed decision whether to create any code. That is the real gate. No speculative “build everything” mandate.

## 11. Acceptance for the plan itself (2026-10-12)

- [x] Existing PEOS owners, overlaps and validator/index constraints identified from inspected repo files.
- [x] Ten candidate risks mapped to actionable controls, benign counterexamples and ownership.
- [x] Contemporary external references separated from prior frozen PEOS corpus, with source-specific caveats.
- [x] Alternatives include zero and prose-only, with switching criteria.
- [x] Phased plan, weekly priorities, readiness/exit gates, outcome measures and rollback defined.
- [x] Scope excludes automatic deployment, process-gate escalation and unsupported bias diagnosis.
- [ ] Pilot performed — **NOT DONE**.
- [ ] Catalog/CLI/PR/UI implemented — **NOT DONE**.
- [ ] Behavioral improvement verified in actual projects — **NOT DONE**.

**STOP: plan documentation only.** Execution requires a later task; no claim of completed pilot or automatic approval from this document.
