"""Provenance validation for authored claim records."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ..yaml_io import iter_yaml_paths, load_yaml_file


@dataclass(frozen=True)
class ProvenanceIssue:
    """Structured provenance issue."""

    path: str
    message: str


def _load_documents(root: Path, target_entity_type: str) -> dict[str, dict[str, Any]]:
    documents: dict[str, dict[str, Any]] = {}
    if not root.exists():
        return documents
    for path in iter_yaml_paths(root):
        document = load_yaml_file(path)
        if isinstance(document, dict) and document.get("entity_type") == target_entity_type:
            identifier = document.get("id")
            if isinstance(identifier, str):
                documents[identifier] = document
    return documents


def validate_claim_provenance(
    document: dict[str, Any],
    path: str | Path,
    sources_by_id: dict[str, dict[str, Any]],
    artifacts_by_id: dict[str, dict[str, Any]],
) -> list[ProvenanceIssue]:
    """Validate provenance completeness and source/artifact consistency for a claim."""
    path_str = str(path)
    issues: list[ProvenanceIssue] = []

    source_id = document.get("source_id")
    artifact_id = document.get("artifact_id")
    provenance = document.get("provenance")

    if not isinstance(source_id, str) or not source_id.strip():
        issues.append(ProvenanceIssue(path=path_str, message="Claim is missing source_id"))
    if not isinstance(artifact_id, str) or not artifact_id.strip():
        issues.append(ProvenanceIssue(path=path_str, message="Claim is missing artifact_id"))

    if not isinstance(provenance, dict):
        issues.append(ProvenanceIssue(path=path_str, message="Claim is missing provenance mapping"))
    else:
        extraction_method = provenance.get("extraction_method")
        locator = provenance.get("locator")
        if not isinstance(extraction_method, str) or not extraction_method.strip():
            issues.append(
                ProvenanceIssue(path=path_str, message="Claim provenance is missing extraction_method")
            )
        if not isinstance(locator, str) or not locator.strip():
            issues.append(ProvenanceIssue(path=path_str, message="Claim provenance is missing locator"))

    if isinstance(source_id, str) and source_id not in sources_by_id:
        issues.append(ProvenanceIssue(path=path_str, message=f"Claim source_id does not resolve: {source_id}"))
    if isinstance(artifact_id, str) and artifact_id not in artifacts_by_id:
        issues.append(
            ProvenanceIssue(path=path_str, message=f"Claim artifact_id does not resolve: {artifact_id}")
        )
    if isinstance(source_id, str) and isinstance(artifact_id, str) and artifact_id in artifacts_by_id:
        artifact_source_id = artifacts_by_id[artifact_id].get("source_id")
        if artifact_source_id != source_id:
            issues.append(
                ProvenanceIssue(
                    path=path_str,
                    message=(
                        "Claim source_id does not match the registered source_id for its artifact"
                    ),
                )
            )

    return issues


def validate_repository_provenance(root: str | Path) -> list[ProvenanceIssue]:
    """Validate provenance across all authored claim records in the repository."""
    root_path = Path(root)
    sources_by_id = _load_documents(root_path / "sources", "source")
    artifacts_by_id = _load_documents(root_path / "sources", "artifact")
    issues: list[ProvenanceIssue] = []

    claims_root = root_path / "claims"
    if not claims_root.exists():
        return issues

    for path in iter_yaml_paths(claims_root):
        document = load_yaml_file(path)
        if isinstance(document, dict) and document.get("entity_type") == "claim":
            issues.extend(validate_claim_provenance(document, path, sources_by_id, artifacts_by_id))
    return issues
