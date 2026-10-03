# Module map

- Product Strategy — problem/outcome/constraints.
- Product Discovery — user/context evidence and product-risk reduction.
- Domain — Event Storming/DDD semantics and boundaries.
- Requirements — traceable requirements, scenarios, NFRs, acceptance.
- System Architecture — quality attributes, failure modes, structure and ADRs.
- Experience — UX/interaction/accessibility/visual/design-system decisions.
- Software Engineering — frontend/backend/API/data implementation contracts.
- Quality Engineering — risk-based testing and performance evidence.
- Security & Reliability — secure SDLC, threat model, SLO/observability/DR/incidents.
- Delivery & Production — CI/CD, provenance, release and rollout evidence.
- Product Intelligence — analytics, experimentation and feedback loop.
- Knowledge Governance — provenance, freshness, conflicts, supersession and evals.

Use only the modules required by the current outcome and missing evidence.

## Stage depth

After selecting a module, load the matching canonical stage playbook from `references/stages/`. MODULE contracts route work; stage playbooks contain the deeper operational method. Load only stages needed for the current outcome.
