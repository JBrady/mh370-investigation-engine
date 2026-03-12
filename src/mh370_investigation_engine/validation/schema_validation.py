"""JSON Schema validation helpers for repository YAML documents."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from ..schema_loader import load_schema
from ..yaml_io import iter_yaml_paths, load_yaml_file

REPOSITORY_YAML_ROOTS = ("claims", "constraints", "scenarios", "sources", "evaluations")


@dataclass(frozen=True)
class ValidationIssue:
    """Structured validation issue."""

    path: str
    message: str


def _entity_type_for_document(document: Any, path: Path) -> str:
    if not isinstance(document, dict):
        raise ValueError(f"{path} must contain a mapping document")
    entity_type = document.get("entity_type")
    if not entity_type:
        raise ValueError(f"{path} is missing entity_type")
    return str(entity_type)


def validate_document(document: Any, path: str | Path) -> list[ValidationIssue]:
    """Validate an in-memory document against its entity schema."""
    path_obj = Path(path)
    entity_type = _entity_type_for_document(document, path_obj)
    schema = load_schema(entity_type)
    validator = Draft202012Validator(schema)
    return [
        ValidationIssue(path=str(path_obj), message=error.message)
        for error in sorted(validator.iter_errors(document), key=lambda item: list(item.path))
    ]


def validate_yaml_file(path: str | Path) -> list[ValidationIssue]:
    """Load and validate a YAML file."""
    path_obj = Path(path)
    try:
        document = load_yaml_file(path_obj)
    except Exception as exc:  # pragma: no cover - exercised indirectly in tests
        return [ValidationIssue(path=str(path_obj), message=f"YAML load failed: {exc}")]
    try:
        return validate_document(document, path_obj)
    except Exception as exc:
        return [ValidationIssue(path=str(path_obj), message=str(exc))]


def validate_repository_documents(root: str | Path) -> list[ValidationIssue]:
    """Validate all repository-authored YAML documents under known roots."""
    root_path = Path(root)
    issues: list[ValidationIssue] = []
    for directory in REPOSITORY_YAML_ROOTS:
        current_root = root_path / directory
        if not current_root.exists():
            continue
        for path in iter_yaml_paths(current_root):
            issues.extend(validate_yaml_file(path))
    return issues
