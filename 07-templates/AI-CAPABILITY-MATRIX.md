# AI Governance / Capability Matrix

## Scope / owner / review date
## Data classification used
PUBLIC | INTERNAL | CONFIDENTIAL | PERSONAL/SENSITIVE | HIGH-RISK/RESTRICTED

## Model / provider policy
| Runtime / model | Allowed data classes | Allowed tasks / risk | Retention/privacy evidence | Egress boundary | Approval/exception | Verified at |
|---|---|---|---|---|---|---|

## Agent capability matrix
Use `ALLOW`, `DENY`, `APPROVAL`, or `CONDITIONAL(policy-id)`.

| Agent / role | Repo read | Repo write | Command exec | Web | Prod logs | Prod DB read | Prod DB write | External message | Merge | Deploy staging | Deploy prod | Secrets/infra |
|---|---|---|---|---|---|---|---|---|---|---|---|---|

## Tool contracts
| Tool | Identity/credential | Read scope | Write scope | Egress | Sensitive-output risk | Bounded/redacted output | Audit evidence |
|---|---|---|---|---|---|---|---|

## Approval rules
| Action | Trigger/risk | Required approver | Evidence shown | Bound artifact/version |
|---|---|---|---|---|

## Exceptions / expiry / revisit triggers
