# AGENTS.md

## Repo purpose

`MH370-investigation-engine` is a spec-first public-evidence investigation system for MH370.

It is not a conspiracy repo, not a narrative-writing repo, and not an autonomous research agent.

The repository is designed to:
- structure known public evidence
- separate observation from inference
- keep hypotheses out of the evidence layer
- model first-class constraints
- evaluate explicit scenarios against evidence and constraints
- produce deterministic, inspectable compatibility outputs

## Current goal

Protect and extend the Phase 0 / Phase 1 contracts plus the Phase 2 manual-first ingestion foundation without broadening scope.

The repo currently proves that it can:
- define the evidence / scenario / reasoning split
- enforce initial schema contracts
- validate field-aware reference integrity for core cross-object links
- validate structural neutrality boundaries
- register sources and artifacts through a manual-first flow
- generate non-ingestable claim authoring templates
- ingest manual claim drafts into authored claim records
- quarantine incomplete or unsupported claim drafts
- build deterministic normalized bundles for sources, artifacts, and claims
- validate claim provenance and source/artifact consistency
- run deterministic contract tests in CI

The current milestone is the Phase 2 ingestion foundation without real corpus ingestion.

That means the repo currently contains:
- architecture and methodology docs
- initial schema set
- placeholder authored YAMLs for constraints and scenarios
- validation modules
- manual-first ingestion modules and thin tool wrappers
- schema, integrity, determinism, and ingestion tests

Current placeholder constraint policy:
- Phase 1 placeholder constraints are explicitly marked with `placeholder: true`
- non-placeholder constraints must cite at least one evidentiary basis reference

The most likely next milestone is the first narrow real Phase 2 corpus:
- one official source family only
- manual-first source and artifact registration against real records
- manual-first claim extraction against one approved official corpus
- no scenario evaluation changes unless required by the ingestion contract
- no broad source expansion until the first corpus is working end to end

## Scope boundaries

Do not broaden scope unless explicitly asked.

Out of scope by default:
- autonomous agent behavior
- hypothesis generation
- optimizer or search-loop logic
- black-box or probabilistic scoring
- narrative analysis output
- broad source ingestion beyond the approved evidence-first plan
- UI work
- non-deterministic workflows

## Important files

- `README.md`
- `AGENTS.md`
- `docs/vision.md`
- `docs/architecture.md`
- `docs/methodology.md`
- `docs/reasoning-engine.md`
- `docs/glossary.md`
- `specs/source-schema.yaml`
- `specs/artifact-schema.yaml`
- `specs/claim-schema.yaml`
- `specs/claim-link-schema.yaml`
- `specs/constraint-schema.yaml`
- `specs/scenario-schema.yaml`
- `specs/geo-reference-schema.yaml`
- `specs/timeline-event-schema.yaml`
- `specs/evaluation-contract.yaml`
- `specs/reasoning-report-schema.yaml`
- `specs/scoring-rules.yaml`
- `specs/registry-schema.yaml`
- `claims/canonical-claims.yaml`
- `claims/contradictions.yaml`
- `constraints/fuel-envelope.yaml`
- `constraints/satellite-arc.yaml`
- `constraints/radar-coverage.yaml`
- `scenarios/scenario-registry.yaml`
- `scenarios/deliberate-diversion.yaml`
- `scenarios/ghost-flight.yaml`
- `scenarios/hijack.yaml`
- `scenarios/mechanical-plus-incapacitation.yaml`
- `scenarios/hybrid.yaml`
- `src/mh370_investigation_engine/ids.py`
- `src/mh370_investigation_engine/yaml_io.py`
- `src/mh370_investigation_engine/schema_loader.py`
- `src/mh370_investigation_engine/ingestion/manual_foundation.py`
- `src/mh370_investigation_engine/validation/schema_validation.py`
- `src/mh370_investigation_engine/validation/reference_validation.py`
- `src/mh370_investigation_engine/validation/neutrality_validation.py`
- `src/mh370_investigation_engine/validation/provenance_validation.py`
- `tools/ingest/register_source.py`
- `tools/ingest/register_artifact.py`
- `tools/ingest/make_claim_template.py`
- `tools/ingest/ingest_claims.py`
- `tools/normalize/normalize_evidence.py`
- `tools/validate/validate_provenance.py`
- `tests/integrity/test_reference_integrity.py`
- `tests/integrity/test_neutrality_rules.py`
- `tests/integrity/test_deterministic_serialization.py`
- `tests/phase2/test_manual_ingestion.py`

## Development rules

- Prefer small, surgical changes
- Preserve deterministic behavior
- Keep authored vs derived boundaries explicit
- Do not put scenario reasoning into evidence objects
- Do not turn placeholders into substantive MH370 analysis unless explicitly asked
- Do not weaken provenance requirements casually
- Do not loosen schemas or validation rules without a concrete reason
- Keep documentation factual, reproducible, and method-oriented

## Method rules

- Claims must remain atomic, source-linked, and neutral
- Claims may be `observation` or `inference`, but not hypotheses
- Classification and status are separate concepts and must remain separate
- Constraints are first-class objects and are not claims
- Non-placeholder constraints must carry evidentiary basis references
- Scenarios reference claims and constraints; they do not rewrite evidence
- Derived outputs are generated views, not hand-authored truth
- Compatibility outputs must be explainable and inspectable

## Phase 2 default workflow

If the user asks to continue or expand Phase 2, default to this workflow unless they explicitly redirect it:

1. Stay evidence-first.
   - Start with one official source family only.
   - Do not start with broad media ingestion.
   - Do not start with scenario scoring changes.
2. Register source before artifact.
   - A source record must exist before artifact records are authored under it.
3. Register artifact before claim extraction.
   - Claims must link to both `source_id` and `artifact_id`.
4. Use manual-first claim authoring.
   - Parser support is acceptable for metadata extraction.
   - `llm_assisted` should not become the default ingestion path.
5. Keep claims neutral.
   - No scenario assumptions.
   - No winner language.
   - No “therefore the aircraft must have...” style reasoning in claims.
6. Preserve quarantine discipline.
   - Unsupported or insufficiently anchored statements should be quarantined, not merged into canonical bundles.
7. Treat canonical bundles as derived.
   - Do not manually author `claims/canonical-claims.yaml` as a long-term truth source.
   - Do not manually author contradiction summaries as a substitute for derivation logic.
8. Re-run validation after each meaningful change to schemas, authored YAML, or validation logic.

Reference validation is field-aware for the core Phase 1 links. Do not weaken this into prefix-only existence checks.

## Source priority

When Phase 2 begins, prefer this order unless the user explicitly changes it:

1. official reports
2. technical analyses directly tied to official or public evidence
3. debris identification and search-operation records
4. only later, credible secondary reporting

Avoid early ingestion of noisy media or speculation-heavy material.

## Ingestion guardrails

- Do not ingest a source unless its repository classification is clear
- Do not author claims without an artifact locator
- Do not collapse multiple assertions into one claim
- Do not encode scenario conclusions into claim text
- Do not turn placeholder constraints into substantive constraints without evidence basis
- Do not treat `claims/canonical-claims.yaml` or `claims/contradictions.yaml` as hand-maintained truth once derivation exists

## Session bootstrap

If the user says `Bootstrap yourself`, or says to read `AGENTS.md` and follow it, do this before proposing changes:

1. Read:
   - `README.md`
   - `docs/vision.md`
   - `docs/architecture.md`
   - `docs/methodology.md`
   - `docs/reasoning-engine.md`
   - `docs/glossary.md`
2. Read the current contract layer:
   - `specs/source-schema.yaml`
   - `specs/artifact-schema.yaml`
   - `specs/claim-schema.yaml`
   - `specs/claim-link-schema.yaml`
   - `specs/constraint-schema.yaml`
   - `specs/scenario-schema.yaml`
   - `specs/geo-reference-schema.yaml`
   - `specs/timeline-event-schema.yaml`
   - `specs/evaluation-contract.yaml`
   - `specs/reasoning-report-schema.yaml`
   - `specs/scoring-rules.yaml`
   - `specs/registry-schema.yaml`
3. Inspect the current authored placeholders:
   - `claims/canonical-claims.yaml`
   - `claims/contradictions.yaml`
   - `constraints/`
   - `scenarios/`
4. Inspect likely Phase 2 landing zones:
   - `sources/`
   - `claims/by-artifact/`
   - `data/raw/`
   - `data/normalized/`
   - `data/derived/`
5. Inspect the current Phase 2 implementation surface:
   - `src/mh370_investigation_engine/ingestion/manual_foundation.py`
   - `tools/ingest/`
   - `tools/normalize/normalize_evidence.py`
   - `tools/validate/validate_provenance.py`
6. Inspect the current validation surface:
   - `src/mh370_investigation_engine/schema_loader.py`
   - `src/mh370_investigation_engine/yaml_io.py`
   - `src/mh370_investigation_engine/validation/schema_validation.py`
   - `src/mh370_investigation_engine/validation/reference_validation.py`
   - `src/mh370_investigation_engine/validation/neutrality_validation.py`
   - `src/mh370_investigation_engine/validation/provenance_validation.py`
7. Inspect the current regression guardrails:
   - `tests/schemas/`
   - `tests/integrity/`
   - `tests/phase2/`
8. Summarize:
   - current repository phase
   - what is implemented vs not implemented
   - current contract boundaries
   - whether the next safe step is first-corpus ingestion, schema tightening, or validator hardening
   - likely next step without inventing extra scope

The goal of bootstrap is to recover the repo’s methodology and implementation context quickly without re-deriving the architecture from scratch.

## Verification

When changing behavior, verify with repo-grounded commands.

Prefer:
- `.venv/bin/pytest`
- `python3 -m venv .venv && .venv/bin/pip install -e '.[dev]' && .venv/bin/pytest` if the virtualenv does not exist yet

When changing schemas or validators, verify:
- schema tests
- integrity tests
- aggregate repository validation through the test suite

Determinism checks currently cover:
- stable YAML serialization for equivalent mappings
- stable ordering and byte output for a small normalized multi-object bundle

When changing Phase 2 ingestion behavior, verify:
- source and artifact records validate
- claim fixtures or authored claim files validate
- provenance validation still passes
- reference integrity still passes
- neutrality checks still pass
- deterministic tests still pass

Do not claim determinism or integrity without running the relevant tests.

## Git workflow

- Do not commit directly to `main`
- Use a feature branch
- Keep commits focused

Workflow shorthand:

- `yeet`: create an appropriate branch, stage the intended changes, commit, push, and open a PR
- `merged`: after a `yeet` PR is merged, sync local `main` with `origin/main`, delete the merged feature branch locally, delete it on `origin`, and prune stale remote-tracking refs
- `full yeet`: do `yeet`, then after the PR is merged perform the full `merged` cleanup flow: sync local `main` with remote and prune merged branches locally and remotely
