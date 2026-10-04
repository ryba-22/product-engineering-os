# AI Security and Governance

AI-assisted engineering changes the trust boundary: prompts, repository content, production data, tool outputs and model responses may cross systems controlled by different providers or identities. Governance should therefore constrain capabilities and data flows rather than rely on agent names, good intentions or prompt instructions.

## Core model

Treat these as different controls:

`persona ≠ identity ≠ capability ≠ authorization`

An agent called “reviewer” is not read-only unless its available tools and credentials make it read-only. A model told “do not access production” is not technically constrained if the runtime still exposes production write credentials.

Use four connected policies:

`DATA CLASSIFICATION × MODEL/PROVIDER POLICY × AGENT CAPABILITIES × HUMAN APPROVAL`

## Data classification

Projects should define their own labels and legal obligations. A useful default classification is:

- **PUBLIC** — intentionally public information;
- **INTERNAL** — non-public operational or engineering information with limited consequence if disclosed;
- **CONFIDENTIAL** — proprietary code, architecture, contracts, business-sensitive information;
- **PERSONAL/SENSITIVE** — personal or otherwise regulated/sensitive records requiring stricter handling;
- **HIGH-RISK/RESTRICTED** — secrets, credentials, production write tokens, high-consequence data or material that policy forbids from external model/tool exposure.

Classification applies to prompts, retrieved context, tool output, attachments, logs and generated artifacts. Redaction is a transformation that also needs validation; it does not automatically declassify data.

## Model and provider policy

For each allowed model/provider/runtime record:
- permitted data classes;
- retention/training/privacy assumptions that have actually been verified;
- geographic/organizational constraints when relevant;
- allowed tasks and risk classes;
- context/logging behavior;
- approval or exception owner;
- verification/review date.

If provider behavior is unknown, the policy status is `UNVERIFIED`, not implicitly safe.

Model routing should consider consequence as well as capability/cost. High-risk data may require a more constrained runtime even when a cloud model would reason better.

## Agent capability matrix

Define agents by executable authority. Typical capability rows include:
- read repository;
- write repository/worktree;
- execute local commands;
- read internal knowledge;
- web access;
- read staging/production logs;
- read production database;
- write production database;
- send external messages;
- create/merge PR;
- deploy staging;
- deploy production;
- modify infrastructure/secrets;
- approve its own high-risk action.

Values should be `ALLOW`, `DENY`, `APPROVAL`, or `CONDITIONAL(policy-id)`.

Default to least privilege. Separate investigation from mutation when possible. A production investigator can often be useful with read-only logs/data and no deployment or database-write capability.

## Tool contract and egress

A tool is part of the security boundary. Record:
- data it can read/write;
- scope restrictions;
- authentication identity;
- whether output can contain secrets/personal data;
- whether calls leave the controlled environment;
- audit/logging behavior;
- destructive operations and recovery semantics;
- output-size/redaction/filtering contract where context leakage matters.

Prefer structured, bounded outputs over dumping raw production logs or full tables into model context. This is both a security and context-budget control.

## Approval policy

Human approval is useful only if the approver receives enough evidence to make a decision and the runtime prevents bypass. Require explicit approval for high-consequence operations such as production mutation, destructive data changes, secret/config changes, external communication or irreversible releases when project risk warrants it.

An approval should bind to a concrete action/version/diff, not to an open-ended session.

## Auditability

For material agent actions preserve enough evidence to answer:
- which identity/agent acted;
- which model/runtime and policy version applied;
- what tools/capabilities were available;
- what data class was processed;
- what action/result occurred;
- which human approval or exception applied;
- which artifact/commit/deployment resulted.

Do not log secrets merely for audit completeness.

## Decision rules

- Prompt instructions are not authorization controls.
- Read-only credentials are stronger evidence than a read-only intention.
- Tool availability should be risk-scoped before execution, not audited only afterward.
- External connectors/providers must be treated as separate trust boundaries until verified otherwise.
- Model quality does not justify sending data outside an allowed boundary.
- An agent must not approve its own high-risk exception unless the project explicitly defines and justifies that control model.
- Security policy should fail closed on unknown data/provider compatibility for material risk.

## Failure modes

One global API key; production and development credentials mixed; “internal agent” with unrestricted egress; personal data copied into prompts without classification; security dependent on agent persona; raw log/database dumps into context; hidden capabilities; approvals that do not bind to a concrete change; provider assumptions not versioned or revalidated.

## Exit evidence

AI governance is sufficient for the current scope when relevant data classes are known, each model/provider is allowed for the intended class/task, agent capabilities are explicit and least-privilege, high-risk actions have enforceable approval rules, and material actions can be reconstructed without exposing additional sensitive data.
