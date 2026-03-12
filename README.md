# MH370-investigation-engine

`MH370-investigation-engine` is a spec-first research repository for disciplined analysis of public evidence related to Malaysia Airlines Flight MH370.

The repository is built around three strict layers:

- Evidence: neutral, source-linked records of public evidence
- Scenario evaluation: explicit scenario definitions evaluated against evidence and constraints
- Reasoning and reporting: deterministic, inspectable compatibility outputs

## Non-goals

This repository is intentionally conservative in its early phases.

- No autonomous agent behavior
- No hypothesis generation
- No optimizer or search-loop logic
- No black-box model scoring
- No narrative conclusions presented as facts

## Method contract

- Claims must remain atomic, source-linked, and neutral
- Claims may be `observation` or `inference`, but not hypotheses
- Constraints are first-class objects and are distinct from claims
- Non-placeholder constraints must cite an evidentiary basis
- Scenarios reference claims and constraints; they do not rewrite evidence
- Derived outputs are generated views, not hand-authored truth
- Compatibility is reported in explainable bands rather than pseudo-probabilities

## Repository shape

Phase 0 and Phase 1 establish the contract layer:

- `docs/`: architecture, methodology, glossary, and reasoning contracts
- `specs/`: JSON Schema contracts authored in YAML
- `src/mh370_investigation_engine/`: reusable validation and utility code
- `tests/`: schema, integrity, and determinism checks
- `claims/`, `constraints/`, `scenarios/`: authored analytical inputs
- `data/normalized/`, `data/derived/`: deterministic generated outputs

## Validation posture

The initial implementation enforces:

- schema validation
- field-aware reference integrity validation
- neutrality validation
- deterministic serialization and bundle-ordering checks

CI is expected to fail on repository contract violations.
