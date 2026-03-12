# Methodology

## Epistemic rules

- Evidence objects remain neutral.
- Claims may describe observations or source-grounded inferences.
- Hypotheses belong only in scenario files.
- Unsupported claims are quarantined rather than merged into canonical bundles.
- Uncertainty must be explicit when a statement depends on time, location, range, measurement, or drift ambiguity.

## Observation, inference, and scenario assumption

- Observation: a claim that directly reports what a public source or artifact records.
- Inference: a claim that stays anchored to source material but interprets it in a bounded and reviewable way.
- Scenario assumption: a condition adopted by a scenario to explain evidence or fill a gap. Scenario assumptions do not belong in the evidence layer.

Inference is not a loophole for scenario language. If a statement is only meaningful inside a scenario, it does not belong in a claim.

## Provenance rules

Every evidence-bearing claim must preserve:

- `source_id`
- `artifact_id`
- extraction method
- locator within the artifact

Git history is the primary edit history. Timestamp fields are not required by default.

For constraints, evidentiary basis is required unless the record is explicitly marked as a structural placeholder during the pre-ingestion foundation phase.

## Authored versus derived

Authored objects:

- sources
- artifacts
- claims
- constraints
- scenarios

Derived objects:

- canonical claim bundles
- timeline views
- contradiction summaries
- evaluation reports

Derived outputs are inspectable products, not hand-authored truth.

During the current Phase 2 foundation:

- sources, artifacts, and claims are authored manually
- normalized bundles are generated deterministically
- unsupported or incomplete claim drafts are quarantined into derived outputs rather than merged into authored claims

## Neutrality enforcement

Neutrality is enforced structurally and methodologically.

Structural constraints include:

- evidence objects cannot reference scenario IDs
- evidence objects cannot contain assumption bundles
- evidence objects cannot contain evaluator outputs
- scenarios cannot overwrite claim status or embed rewritten evidence as facts

Keyword checks may be used as lightweight linting, but lexical filtering is not the primary safeguard.

Reference integrity is also enforced structurally. Core fields such as `source_id`, `artifact_id`, `claim_refs`, and `constraint_refs` are validated against both existence and expected target type.

Provenance is also validated structurally for claim ingestion. A claim must not only contain provenance fields, it must also preserve a consistent `source_id` / `artifact_id` relationship against the registered artifact record.
