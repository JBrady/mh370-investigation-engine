# Architecture

## Layer model

`MH370-investigation-engine` is divided into three layers:

1. Evidence layer
2. Scenario layer
3. Reasoning and reporting layer

The evidence layer is neutral and source-linked. The scenario layer defines explicit explanatory structures. The reasoning layer evaluates scenarios against claims and constraints and emits deterministic reports.

## Authored versus derived directories

Authored directories:

- `sources/`
- `claims/`
- `constraints/`
- `scenarios/`

Phase 2 authored evidence layout is manual-first:

- sources live at `sources/<classification>/<source_id>/source.yaml`
- artifacts live below their source at `sources/<classification>/<source_id>/artifacts/<artifact_id>.yaml`
- claims live below their artifact at `claims/by-artifact/<artifact_id>/<claim_id>.yaml`
- artifacts may optionally include `raw_relpath` to point to a repository-relative raw file under `data/raw/`

Derived directories:

- `data/normalized/`
- `data/derived/`
- `evaluations/reports/`

`evaluations/runs/` stores run records and metadata. Generated outputs should remain reproducible from authored inputs and versioned rules.

Phase 2 normalized outputs currently include:

- deterministic per-record normalized copies for sources, artifacts, and claims
- deterministic bundle registries for sources, artifacts, and claims
- a quarantine registry for unsupported or incomplete claim drafts

## Identity and reference rules

Stable IDs are type-prefixed:

- `src_*` for sources
- `art_*` for artifacts
- `clm_*` for claims
- `lnk_*` for claim links
- `geo_*` for geographic references
- `con_*` for constraints
- `scn_*` for scenarios
- `evt_*` for timeline events
- `run_*` for evaluation runs
- `rpt_*` for reasoning reports

Cross-object references use IDs only. Human labels are never authoritative references.

Phase 1 reference validation is field-aware for core links such as:

- `source_id -> source`
- `artifact_id -> artifact`
- `claim_refs -> claim`
- `constraint_refs -> constraint`
- `scenario_refs -> scenario`

## Metadata minimalism

By default, authored YAML objects require only:

- `id`
- `entity_type`
- `schema_version`

Additional metadata is justified only where it supports provenance, deterministic processing, or contract clarity. `created_at` and `updated_at` are not required by default.

## Constraint contract

Constraints are not claims. Claims report evidence. Constraints encode bounded conditions that scenarios must satisfy, tension, violate, or explicitly dispute.

Constraint taxonomy:

- `physical`
- `temporal`
- `geometric`
- `operational`
- `search_coverage`

Constraint status:

- `hard`
- `soft`
- `disputed`
- `derived`

Phase 1 placeholder constraints use an explicit `placeholder: true` marker. This allows clearly skeletal records to exist without substantive evidentiary basis while preserving the rule that non-placeholder constraints must cite at least one basis reference.

## Phase 1 repository contract

Phase 1 is complete when the repository contains:

- the approved skeleton
- the initial schema set
- reusable schema, reference, and neutrality validation modules
- test fixtures for valid and invalid structures
- CI wiring for validation and tests
- deterministic checks for both single-document serialization and small multi-object bundle ordering

Phase 1 does not require real evidence content.

## Phase 2 ingestion foundation

The current repository includes only the manual-first ingestion foundation for Phase 2.

Implemented in Phase 2:

- source registration
- artifact registration
- claim authoring template generation
- claim ingestion and normalization
- provenance validation
- quarantine output for unsupported or incomplete claims

Not implemented yet:

- derived timeline generation
- scenario evaluation
- reasoning-engine scoring
