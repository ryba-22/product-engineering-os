# Product Engineering OS

An evidence-driven framework for taking software products from an initial idea to verified delivery and measurable outcomes.

Product Engineering OS helps an AI assistant or engineering team connect product goals, domain rules, architecture, user experience, implementation, testing, release and operations. It provides instructions, templates, schemas, quality gates and evaluation scenarios. It is not an autonomous agent service or a deployment tool.

## Who it is for

- Individuals building or improving a software product.
- Teams coordinating product, design and engineering decisions.
- AI-assisted development workflows that need explicit evidence and completion criteria.

The universal edition does not assume a particular organization, personality profile, technology stack or hosting provider.

## Core principle

Follow the relationship between an idea, evidence, decisions, implementation, verification, production observations and learning.

Keep these states distinct:

`IMPLEMENTED → TESTED → VERIFIED → DEPLOYED → HEALTHY → SUCCESSFUL`

Passing a structural check does not prove production health or product success. Record missing evidence and blockers explicitly.

## Closed learning-loop contract

For material business behavior, Product Engineering OS makes three cross-lifecycle mechanisms explicit:

- **ATDD / Example Mapping before implementation** — bind business rules to concrete examples/counterexamples and an executable oracle; preserve example IDs into tests/evals and production observations.
- **Production Learning Loop** — compare expected vs observed behavior, classify material deltas, then propagate supported learning to domain/requirements/decisions/tests/evals/knowledge before closure.
- **AI Security/Governance** — classify data/provider boundaries and constrain agent/tool capabilities with least privilege and enforceable approval rather than relying on personas or prompt instructions.

The terminal product claim is **Definition of Value**: `HEALTHY ≠ SUCCESSFUL`. If outcome evidence is absent, use `UNVERIFIED OUTCOME`.

## Operator runtime layer

The OS now includes a risk-derived operator runtime contract without turning process state into product truth:

- 00-core/operator-front-door.md routes a plain problem statement into risk, missing evidence, modules, execution profile and lane/workflow shape.
- 00-core/execution-profiles.md maps R0–R4 to FAST / STANDARD / EVIDENCE_HEAVY.
- 01-governance/project-constitution.md and scripts/discover_project_constitution.py discover repository-local candidate conventions while preserving observed != approved != enforced.
- 07-templates/VERIFICATION-MATRIX.md separates completeness, tests, code review, pragmatic review, reality check and production readiness.

These mechanisms are evidence/risk driven. They intentionally do not introduce mandatory approval at every lifecycle phase.

## Quick start

1. Read [BRAIN.md](BRAIN.md) for the runtime instructions.
2. State the desired outcome, scope, constraints and acceptance criteria.
3. Classify risk using [00-core/risk-model.md](00-core/risk-model.md).
4. Select only the modules you need using [00-core/routing.md](00-core/routing.md).
5. Copy the relevant templates into your project and record evidence and decisions.
6. Execute the smallest useful step, verify it and collect the evidence required by the next quality gate.
7. For production work, review release health and outcome measures before claiming success.

Stop researching once additional research is unlikely to change the decision. Use reversible experiments to resolve remaining uncertainty when appropriate.

## Example request

> Use Product Engineering OS to improve the account settings workflow. First inspect the existing implementation and decisions. Define the outcome and risk, select the minimum required modules, implement a small change, and verify the acceptance criteria. Report evidence, remaining blockers and the next action.

## Modules

| Module | Main concern |
| --- | --- |
| Product Strategy | Problem, outcome and constraints |
| Product Discovery | User context and product risks |
| Domain | Business language, rules and boundaries |
| Requirements | Scenarios, acceptance criteria and quality requirements |
| System Architecture | Structure, tradeoffs and failure modes |
| Experience | UX, interactions, accessibility and design systems |
| Software Engineering | Frontend, backend, APIs and persistence |
| Quality Engineering | Tests, guarantees and performance |
| Security & Reliability | Threats, observability, recovery and incidents |
| Delivery & Production | CI/CD, release and rollout evidence |
| Product Intelligence | Metrics, experiments and feedback |
| Knowledge Governance | Sources, freshness, conflicts and decisions |

## Knowledge depth model

Product Engineering OS deliberately separates four layers:

1. **Runtime/orchestration** — `BRAIN.md`, routing, risk and stop-analysis.
2. **Module contracts** — short `MODULE.md` files that define responsibility, inputs, outputs and gates.
3. **Deep stage playbooks** — 25 stage-specific files under `06-modules/**/STAGE-*.md` containing the actual operational method: decision questions, workflow, rules, evidence standard, failure modes, exit criteria and handoff.
4. **Evidence and verification** — source registry, atomic evidence ledger, decision records, templates, gates and evals.

Templates are intentionally short because they are forms to fill. Evidence statements are intentionally atomic because they are graph nodes. Neither is intended to carry the full method. The stage playbooks are the primary knowledge layer for execution.

Short-file policy is executable: `scripts/audit_content_depth.py` fails when a substantive Markdown knowledge file falls below the depth floor unless it belongs to an explicitly concise category such as a module contract, template, adapter/crosswalk or skill router.

`11-maturity/stage-coverage.json` distinguishes **deep-structural** coverage from behavioral effectiveness. Structural/depth checks can prove the knowledge package is present and connected; only executed evaluations can support behavioral claims.


## Current behavioral evidence

The v1.2 runtime completed INDEP-RUN-2026-10-04-02: **28/28 pass, 0 hard failures, 9.57/10 average** using Anthropic Claude Opus 5.5 as the blinded executor and OpenAI GPT-6 Luna via GitHub Copilot CLI as the independent judge. That frozen run remains historical evidence for v1.2.

The current v1.3 operator-runtime change materially modifies BRAIN.md and lifecycle gates, so its behavioral status is **revalidation-required**. The repository deliberately does not project the v1.2 score onto the changed runtime. Structural/local tests can validate implementation mechanics; a fresh independent behavioral run is required before restoring an independent-validation claim.

## Package layout

| Path | Contents |
| --- | --- |
| `BRAIN.md` | Runtime and closure instructions |
| `00-core/` | Lifecycle, routing, risk and operating profile |
| `01-governance/` | Source registry and knowledge lifecycle |
| `02-evidence/` | Evidence schema and ledger |
| `03-decisions/` | Decision record schema and template |
| `04-gates/` | Quality gate definitions |
| `05-evals/` | Evaluation scenarios and expected behavior |
| `06-modules/` | Module contracts and specialist playbooks |
| `07-templates/` | Project artifact templates |
| `08-adapters/` | Optional specialist integration contracts |
| `09-roadmap/` | Development roadmap |
| `10-source-notes/` | Source note guidance |
| `11-maturity/` | Internal coverage and maturity metadata |
| `machine/` | Machine-readable integration mapping |
| `skills/product-engineering-os/` | Portable skill instructions |
| `scripts/` | Validation and audit utilities |
| `tests/` | Structural and contract tests |

## Using the skill

The portable skill is located at `skills/product-engineering-os/SKILL.md`. Import that directory using your host application's supported skill mechanism, or give an assistant access to the package and ask it to follow BRAIN.md.

The skill includes a compact runtime and module map. Keep the full package accessible when its templates, schemas and deeper references are needed. Installation and available tools depend on the host application; this archive does not install or activate itself.

## Optional integrations

Specialist UI, domain and craft assets are optional and are not bundled. Adapter records are integration placeholders, not proof that the external asset is installed, verified or accessible.

When using an integration, record its actual location, version, scope and usage rights. Without it, use the bundled module contract and preserve missing evidence as unresolved. Do not claim equivalent specialist depth.

## Validation

Use Python 3. From the package root, run:

```bash
python3 scripts/validate.py
python3 scripts/audit_coverage.py
python3 scripts/audit_freshness.py
```

To run the test suite, install pytest in your development environment and run:

```bash
python3 -m pytest tests -q
```

These checks assess package structure, references and contract assertions. They do not execute all evaluation scenarios against a model or certify a product's correctness, security or production readiness.

## Language

Documentation, skill instructions, templates and evaluation scenarios are written in English. Code identifiers, comments and machine-readable field names are also in English. Project outputs may use any language requested by the team.

## Evidence and limitations

Source verification dates and maturity labels are inherited metadata, not a fresh independent audit or certification. Recheck decision-critical sources and their applicability before relying on them. Optional integration records have no verification date until a concrete asset is reviewed.

The framework does not provide tools, credentials, background execution or automatic access to external systems. Agent delegation, deployment and other actions require capabilities and authorization in the host environment.

## Privacy

Keep confidential project information, credentials and personal data outside
this reusable package. Review project-specific artifacts before sharing them.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE).

## Third-party materials

External sources are referenced for context and attribution. No third-party
books, PDFs or specialist knowledge packages are included.

The MIT License applies to this project's original content. Referenced
third-party materials remain subject to their respective licenses and terms.

## Worked example and executed evaluation

Start with [retry-safe enrollment](examples/idempotent-enrollment/README.md). It includes a request, bounded scope, evidence, acceptance criteria, a decision, implementation and local verification. Run `python3 examples/idempotent-enrollment/evaluate.py` and read [the evaluation](examples/idempotent-enrollment/EVALUATION.md). This is one self-assessed case, not a model benchmark. The 81 golden scenarios are a specification corpus; they have not all been executed against a model.

GitHub Actions runs structural checks, source freshness, pytest and the example on pushes and pull requests. Unconnected optional integrations are reported separately; missing, future-dated or stale required sources fail the freshness audit.
