# Routing protocol

Use the current outcome, missing evidence and risk to choose modules.

| Question | Primary module |
|---|---|
| Why should this exist / what outcome matters? | product-strategy |
| Who has the problem / what do they actually need? | product-discovery |
| How does the business domain behave? | domain |
| What exactly must the product/system satisfy? | requirements |
| How should the technical system be structured? | system-architecture |
| How should people understand and operate it? | experience |
| How should it be implemented in frontend/backend/data? | software-engineering |
| How do we prove behavior/performance? | quality-engineering |
| How do we keep it secure, reliable and recoverable? | security-reliability |
| How do we build/release/roll out it safely? | delivery-production |
| Did it create the intended outcome and what next? | product-intelligence |
| Which knowledge is canonical/fresh/superseded? | knowledge-governance |

### Routing rule
A module may consume another module's artifact, but it must not silently replace that module's judgment. For example, system architecture consumes domain boundaries but does not infer business rules; UX consumes requirements but does not invent policy; analytics measures an outcome but does not redefine the outcome without a product decision.
