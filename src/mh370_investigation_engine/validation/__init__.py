"""Validation helpers for repository contracts."""

from .neutrality_validation import (
    validate_neutrality,
    validate_neutrality_for_file,
    validate_repository_neutrality,
)
from .provenance_validation import validate_claim_provenance, validate_repository_provenance
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
        "provenance": validate_repository_provenance(root),
    }


__all__ = [
    "validate_neutrality",
    "validate_neutrality_for_file",
    "validate_repository_neutrality",
    "validate_claim_provenance",
    "validate_repository_provenance",
    "validate_repository",
    "validate_references",
    "validate_references_in_directory",
    "validate_repository_references",
    "validate_repository_documents",
    "validate_yaml_file",
]
