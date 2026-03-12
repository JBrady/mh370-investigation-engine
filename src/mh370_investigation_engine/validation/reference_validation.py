"""Reference integrity validation."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ..ids import detect_entity_type_from_id, has_expected_prefix
from ..yaml_io import iter_yaml_paths, load_yaml_file

REPOSITORY_YAML_ROOTS = ("claims", "constraints", "scenarios", "sources", "evaluations")
FIELD_TARGET_TYPES = {
    "artifact_id": {"artifact"},
    "claim_refs": {"claim"},
    "constraint_refs": {"constraint"},
    "geo_reference_ids": {"geo_reference"},
    "scenario_refs": {"scenario"},
    "source_claim_id": {"claim"},
    "source_id": {"source"},
    "target_claim_id": {"claim"},
}


@dataclass(frozen=True)
class ReferenceIssue:
    """Structured reference issue."""

    path: str
    message: str


def _collect_ref_values(node: Any) -> list[tuple[str, str]]:
    refs: list[tuple[str, str]] = []
    if isinstance(node, dict):
        for key, value in node.items():
            if key.endswith("_id") and isinstance(value, str):
                refs.append((key, value))
            elif (key.endswith("_refs") or key.endswith("_ids")) and isinstance(value, list):
                refs.extend((key, item) for item in value if isinstance(item, str))
            else:
                refs.extend(_collect_ref_values(value))
    elif isinstance(node, list):
        for item in node:
            refs.extend(_collect_ref_values(item))
    return refs


def validate_references(documents: list[tuple[Path, dict[str, Any]]]) -> list[ReferenceIssue]:
    """Validate duplicate IDs and unresolved typed references."""
    issues: list[ReferenceIssue] = []
    ids_to_paths: dict[str, list[str]] = defaultdict(list)

    for path, document in documents:
        entity_type = document.get("entity_type")
        identifier = document.get("id")
        if isinstance(entity_type, str) and isinstance(identifier, str):
            if not has_expected_prefix(entity_type, identifier):
                issues.append(
                    ReferenceIssue(
                        path=str(path),
                        message=f"ID {identifier!r} does not match expected prefix for {entity_type}",
                    )
                )
            ids_to_paths[identifier].append(str(path))

    for identifier, paths in sorted(ids_to_paths.items()):
        if len(paths) > 1:
            issues.append(
                ReferenceIssue(
                    path=", ".join(paths),
                    message=f"Duplicate ID detected: {identifier}",
                )
            )

    known_ids = set(ids_to_paths)
    for path, document in documents:
        for field_name, reference in _collect_ref_values(document):
            if reference == document.get("id"):
                continue
            ref_entity_type = detect_entity_type_from_id(reference)
            expected_types = FIELD_TARGET_TYPES.get(field_name)
            if expected_types is not None and ref_entity_type not in expected_types:
                expected_label = ", ".join(sorted(expected_types))
                issues.append(
                    ReferenceIssue(
                        path=str(path),
                        message=(
                            f"Field {field_name!r} must reference {expected_label} IDs; "
                            f"got {reference!r}"
                        ),
                    )
                )
            if ref_entity_type is None:
                continue
            if reference not in known_ids:
                issues.append(
                    ReferenceIssue(path=str(path), message=f"Unresolved reference: {reference}")
                )
    return issues


def validate_references_in_directory(root: str | Path) -> list[ReferenceIssue]:
    """Load YAML documents below a root and validate their references."""
    root_path = Path(root)
    documents: list[tuple[Path, dict[str, Any]]] = []
    for path in iter_yaml_paths(root_path):
        document = load_yaml_file(path)
        if isinstance(document, dict) and "entity_type" in document and "id" in document:
            documents.append((path, document))
    return validate_references(documents)


def validate_repository_references(root: str | Path) -> list[ReferenceIssue]:
    """Validate references for repository-authored YAML documents."""
    root_path = Path(root)
    documents: list[tuple[Path, dict[str, Any]]] = []
    for directory in REPOSITORY_YAML_ROOTS:
        current_root = root_path / directory
        if not current_root.exists():
            continue
        for path in iter_yaml_paths(current_root):
            document = load_yaml_file(path)
            if isinstance(document, dict) and "entity_type" in document and "id" in document:
                documents.append((path, document))
    return validate_references(documents)
