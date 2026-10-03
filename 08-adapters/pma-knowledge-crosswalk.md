> Optional integration: PMA is a versioned public knowledge graph. PEOS must consume only the public machine registry and must never depend on PMA private/raw-source directories.

# Polska Myśl Architektoniczna → Product Engineering OS

## Separation of responsibilities

PMA is the **knowledge plane**. It stores concepts, heuristics, software archetypes, failure patterns, case-study syntheses and AI-engineering knowledge.

PEOS is the **execution plane**. It owns routing, gates, decision records, execution, verification and closure.

## Runtime contract

1. Import the PMA public registry with `scripts/import_pma_registry.py`.
2. Record the PMA Git SHA in the imported snapshot.
3. Route by PEOS stage/problem class; do not load the whole knowledge graph.
4. Use PMA entries as candidate/verified guidance according to their own lifecycle and provenance.
5. Hard constraints and higher-authority PEOS sources remain authoritative.
6. PMA knowledge can propose a heuristic or archetype; PEOS still requires project evidence before freezing a decision.

## Typical routing

Domain Discovery / Domain Architecture:
- problem-classification heuristics;
- linguistic boundaries;
- unit-of-change and consistency;
- software archetypes;
- case studies.

System Architecture:
- architecture drivers;
- connascence/coupling;
- failure-pattern analysis;
- integration and transactional atomicity.

Quality / AI Brain:
- evolutionary eval;
- software-factory feedback loops;
- observability and context engineering.

## Publication boundary

The imported registry must declare `publication_boundary: public-only`.
Any entry pointing at `private/` or `assets-private/` is rejected by the importer.

## Local development

Default sibling checkout:

`../Polska-Mysl-Architektoniczna-Obsidian`

Override with `--source` or `PMA_PATH`.
