# Project Constitution Discovery

A Project Constitution is the small set of project-specific rules that materially constrain implementation and verification.

It separates three states that are often conflated:

observed convention -> approved rule -> executable enforcement

## Discovery sources

Use independent evidence where available:
- tool/config files;
- source-code patterns;
- project documentation/instructions;
- CI/CD workflows;
- recent review/PR evidence when the host can access it;
- existing architecture tests, linters and policy checks.

The bundled local scanner covers repository-local evidence only. External PR/review evidence is an optional enrichment, not silently assumed.

## Confidence is not authority

Confidence measures how strongly the repository evidence supports the observation. It does not turn an observation into a rule.

Every candidate remains one of:
- candidate — observed, not approved;
- approved — owner accepted it as intended project policy;
- enforced — a machine check or hard runtime boundary proves compliance;
- rejected — evidence reflected accident/history rather than desired policy;
- superseded — replaced by a newer decision.

## Conflict rule

Conflicting evidence must be surfaced rather than averaged away. Examples:
- formatter config and docs disagree;
- CI runs a check that local instructions omit;
- code patterns conflict across bounded areas.

The owner decides which rule is canonical and where its scope applies.

## Executable discovery

Run:

    python3 scripts/discover_project_constitution.py /absolute/path/to/repo

To persist the candidate dossier outside the target repository:

    python3 scripts/discover_project_constitution.py /absolute/path/to/repo \
      --output-dir /path/to/evidence/project-constitution

Outputs are observations and evidence pointers. Promote them into an approved constitution only after review.

## Ownership and lifecycle

Discovery should be repeated when the repository changes enough that old observations may no longer describe intended practice: a new framework, CI migration, ownership boundary, formatter/linter replacement, testing strategy change or repeated review guidance are all re-evaluation triggers. The constitution owner decides whether a candidate becomes approved, rejected or scoped to only part of the repository.

Approval should prefer a narrow statement that can be falsified. For example, "all production TypeScript is strict" is easier to verify than "use good TypeScript practices". When an approved rule is important enough to block delivery, add an executable enforcement mechanism such as compiler configuration, lint rule, architecture test, CI check or repository policy. Record the enforcement beside the rule rather than relying on prose alone.

## Failure modes

Avoid three common errors. First, do not promote the most frequent code shape when the repository contains historical debt. Second, do not resolve conflicting evidence by averaging confidence scores; conflict requires an owner decision and scope. Third, do not let a generated constitution override stronger project facts, domain rules, security boundaries or explicit decisions. Constitution discovery reduces context reconstruction cost; it does not replace engineering judgment or evidence ownership.
