"""Structural neutrality validation for evidence and scenario boundaries."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ..yaml_io import iter_yaml_paths, load_yaml_file

REPOSITORY_YAML_ROOTS = ("claims", "constraints", "scenarios", "sources", "evaluations")
EVIDENCE_ENTITY_TYPES = {"source", "artifact", "claim", "claim_link", "geo_reference", "timeline_event"}
FORBIDDEN_EVIDENCE_KEYS = {
    "scenario_id",
    "scenario_ids",
    "assumptions",
    "required_conditions",
    "compatibility_band",
    "assumption_load",
    "explanation_ledger",
}


@dataclass(frozen=True)
class NeutralityIssue:
    """Structured neutrality issue."""

    path: str
    message: str


def validate_neutrality(document: dict[str, Any], path: str | Path) -> list[NeutralityIssue]:
    """Validate structural neutrality rules for a single document."""
    issues: list[NeutralityIssue] = []
    entity_type = document.get("entity_type")
    path_str = str(path)

    if entity_type in EVIDENCE_ENTITY_TYPES:
        for key in FORBIDDEN_EVIDENCE_KEYS:
            if key in document:
                issues.append(
                    NeutralityIssue(
                        path=path_str,
                        message=f"Evidence-layer object contains forbidden field {key!r}",
                    )
                )
        for key, value in document.items():
            if key.endswith("_id") and isinstance(value, str) and value.startswith("scn_"):
                issues.append(
                    NeutralityIssue(
                        path=path_str,
                        message="Evidence-layer object must not reference scenario IDs",
                    )
                )
            if key.endswith("_refs") and isinstance(value, list):
                if any(isinstance(item, str) and item.startswith("scn_") for item in value):
                    issues.append(
                        NeutralityIssue(
                            path=path_str,
                            message="Evidence-layer object must not reference scenario IDs",
                        )
                    )

    if entity_type == "scenario":
        if "claims" in document or "constraints" in document:
            issues.append(
                NeutralityIssue(
                    path=path_str,
                    message="Scenario objects must reference claims and constraints by ID rather than embed them",
                )
            )

    return issues


def validate_neutrality_for_file(path: str | Path) -> list[NeutralityIssue]:
    """Load and validate a YAML document for neutrality constraints."""
    path_obj = Path(path)
    document = load_yaml_file(path_obj)
    if not isinstance(document, dict):
        return [NeutralityIssue(path=str(path_obj), message="YAML document must be a mapping")]
    return validate_neutrality(document, path_obj)


def validate_neutrality_in_directory(root: str | Path) -> list[NeutralityIssue]:
    """Validate neutrality for all YAML documents under a root."""
    root_path = Path(root)
    issues: list[NeutralityIssue] = []
    for path in iter_yaml_paths(root_path):
        document = load_yaml_file(path)
        if isinstance(document, dict) and "entity_type" in document:
            issues.extend(validate_neutrality(document, path))
    return issues


def validate_repository_neutrality(root: str | Path) -> list[NeutralityIssue]:
    """Validate neutrality for repository-authored YAML documents."""
    root_path = Path(root)
    issues: list[NeutralityIssue] = []
    for directory in REPOSITORY_YAML_ROOTS:
        current_root = root_path / directory
        if not current_root.exists():
            continue
        for path in iter_yaml_paths(current_root):
            document = load_yaml_file(path)
            if isinstance(document, dict) and "entity_type" in document:
                issues.extend(validate_neutrality(document, path))
    return issues
