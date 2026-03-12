"""Validation helpers for repository contracts."""

from .neutrality_validation import (
    validate_neutrality,
    validate_neutrality_for_file,
    validate_repository_neutrality,
)
from .reference_validation import (
    validate_references,
    validate_references_in_directory,
    validate_repository_references,
)
from .schema_validation import validate_repository_documents, validate_yaml_file


def validate_repository(root: str) -> dict[str, list]:
    """Run repository validation across the core contract checks."""
    return {
        "schema": validate_repository_documents(root),
        "references": validate_repository_references(root),
        "neutrality": validate_repository_neutrality(root),
    }


__all__ = [
    "validate_neutrality",
    "validate_neutrality_for_file",
    "validate_repository_neutrality",
    "validate_repository",
    "validate_references",
    "validate_references_in_directory",
    "validate_repository_references",
    "validate_repository_documents",
    "validate_yaml_file",
]
