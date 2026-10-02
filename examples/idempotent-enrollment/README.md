# Worked example: retry-safe enrollment

This synthetic, local case demonstrates a complete bounded development task. No production system, personal data or external specialist asset is involved.

## Request
An enrollment form can be submitted twice after a timeout. Prevent duplicate enrollment while permitting one pupil to enroll in different courses.

## Product brief and scope
Outcome: retrying the same pupil/course request stores one enrollment. Risk: R1 (reversible local demonstration). Modules: Requirements, Software Engineering and Quality Engineering. No new UI, billing, notifications, deployment or analytics.

## Evidence and requirements
EVD-EX-001: the append-only baseline stores two records after two identical calls; reproduced by evaluate.py. EVD-EX-002: candidate acceptance checks are executable in the same script. These are project-local observations, not external research claims.

AC1: first valid enrollment returns created. AC2: identical retry returns already_enrolled and keeps exactly one row. AC3: a different course is allowed. AC4: missing or blank identifiers raise ValueError without data changes. AC5: surrounding whitespace does not create duplicates.

## ADR-EX-001
Choose a database UNIQUE(pupil, course) constraint with an atomic insert. An application-only check followed by insert would leave a race window. SQLite is used solely to make the demonstration reproducible without services. Production identifiers, authorization, lifecycle rules and cross-process concurrency require project-specific design and verification.

## Implementation and verification
See enrollment.py. Run `python3 examples/idempotent-enrollment/evaluate.py` from the repository root. It executes the baseline and candidate, then prints every acceptance result and exits nonzero on failure.

## Closure
Implemented and locally verified against AC1–AC5. Not deployed. Production health and product success remain UNVERIFIED. See EVALUATION.md for actual observations and limits.
