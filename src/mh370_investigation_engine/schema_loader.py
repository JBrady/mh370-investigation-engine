"""Schema loading helpers."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .yaml_io import load_yaml_file

SCHEMA_FILE_BY_ENTITY_TYPE = {
    "artifact": "artifact-schema.yaml",
    "claim": "claim-schema.yaml",
    "claim_link": "claim-link-schema.yaml",
    "constraint": "constraint-schema.yaml",
    "geo_reference": "geo-reference-schema.yaml",
    "reasoning_report": "reasoning-report-schema.yaml",
    "registry": "registry-schema.yaml",
    "scenario": "scenario-schema.yaml",
    "source": "source-schema.yaml",
    "timeline_event": "timeline-event-schema.yaml",
}


def repository_root() -> Path:
    """Return the repository root from the package path."""
    return Path(__file__).resolve().parents[2]


def specs_root() -> Path:
    """Return the root directory containing repository schemas."""
    return repository_root() / "specs"


def schema_path_for_entity_type(entity_type: str) -> Path:
    """Return the schema path for a supported entity type."""
    try:
        filename = SCHEMA_FILE_BY_ENTITY_TYPE[entity_type]
    except KeyError as exc:
        raise KeyError(f"Unsupported entity_type for schema lookup: {entity_type}") from exc
    return specs_root() / filename


def load_schema(entity_type: str) -> Any:
    """Load a repository schema by entity type."""
    return load_yaml_file(schema_path_for_entity_type(entity_type))
