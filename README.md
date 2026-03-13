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

Phase 0, Phase 1, and the Phase 2 ingestion foundation now cover:

- `docs/`: architecture, methodology, glossary, and reasoning contracts
- `specs/`: JSON Schema contracts authored in YAML
- `src/mh370_investigation_engine/`: reusable validation, ingestion, and utility code
- `tests/`: schema, integrity, determinism, and ingestion checks
- `claims/`, `constraints/`, `scenarios/`: authored analytical inputs
- `sources/`: authored source and artifact records
- `data/normalized/`, `data/derived/`: deterministic generated outputs
- `tools/ingest/`, `tools/normalize/`, `tools/validate/`: thin wrappers around the Phase 2 ingestion foundation

## Phase 2 foundation

The repository now includes a manual-first ingestion foundation for:

- source registration
- artifact registration
- claim authoring template generation
- claim ingestion and normalization
- provenance validation
- quarantine output for incomplete or unsupported claim drafts
- deterministic normalized bundles for sources, artifacts, and claims

Artifact records may optionally include `raw_relpath` to point at an in-repo raw artifact file under `data/raw/`.

## Validation posture

The current implementation enforces:

- schema validation
- field-aware reference integrity validation
- neutrality validation
- provenance validation
- deterministic serialization and bundle-ordering checks

CI is expected to fail on repository contract violations.
