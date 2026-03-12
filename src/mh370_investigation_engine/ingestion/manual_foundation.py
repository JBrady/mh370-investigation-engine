"""Manual-first Phase 2 ingestion foundation."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ..validation.neutrality_validation import validate_neutrality
from ..validation.provenance_validation import validate_claim_provenance
from ..validation.schema_validation import validate_document
from ..yaml_io import dump_yaml, iter_yaml_paths, load_yaml_file, normalize_records


@dataclass(frozen=True)
class RegistrationResult:
    """Result for source/artifact registration."""

    record_id: str
    authored_path: Path
    normalized_bundle_paths: dict[str, Path]


@dataclass(frozen=True)
class ClaimIngestionResult:
    """Result for claim ingestion."""

    written_ids: list[str]
    quarantined_ids: list[str]
    quarantine_path: Path | None
    normalized_bundle_paths: dict[str, Path]
    issues: list[str]


class IngestionError(ValueError):
    """Raised when an authored Phase 2 registration flow cannot proceed."""


def _write_yaml(path: Path, document: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(dump_yaml(document), encoding="utf-8")


def _collect_entity_documents(search_root: Path, entity_type: str) -> dict[str, dict[str, Any]]:
    documents: dict[str, dict[str, Any]] = {}
    if not search_root.exists():
        return documents
    for path in iter_yaml_paths(search_root):
        document = load_yaml_file(path)
        if isinstance(document, dict) and document.get("entity_type") == entity_type:
            identifier = document.get("id")
            if isinstance(identifier, str):
                documents[identifier] = document
    return documents


def _collect_sources(repo_root: Path) -> dict[str, dict[str, Any]]:
    return _collect_entity_documents(repo_root / "sources", "source")


def _collect_artifacts(repo_root: Path) -> dict[str, dict[str, Any]]:
    return _collect_entity_documents(repo_root / "sources", "artifact")


def _collect_claims(repo_root: Path) -> dict[str, dict[str, Any]]:
    return _collect_entity_documents(repo_root / "claims", "claim")


def _bundle_document(registry_id: str, registry_type: str, description: str, items: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "id": registry_id,
        "entity_type": "registry",
        "schema_version": "1.0.0",
        "registry_type": registry_type,
        "description": description,
        "items": items,
    }


def _clear_yaml_files(directory: Path) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    for path in sorted(directory.rglob("*.yaml")):
        path.unlink()


def _source_authored_path(repo_root: Path, source: dict[str, Any]) -> Path:
    classification = source["repository_classification"]
    return repo_root / "sources" / classification / source["id"] / "source.yaml"


def _artifact_authored_path(repo_root: Path, source: dict[str, Any], artifact: dict[str, Any]) -> Path:
    classification = source["repository_classification"]
    return repo_root / "sources" / classification / source["id"] / "artifacts" / f"{artifact['id']}.yaml"


def _claim_authored_path(repo_root: Path, claim: dict[str, Any]) -> Path:
    return repo_root / "claims" / "by-artifact" / claim["artifact_id"] / f"{claim['id']}.yaml"


def _raise_if_invalid(document: dict[str, Any], path_hint: str) -> None:
    issues = validate_document(document, path_hint)
    if issues:
        raise IngestionError("; ".join(issue.message for issue in issues))


def build_normalized_evidence(repo_root: str | Path) -> dict[str, Path]:
    """Build deterministic normalized outputs for authored sources, artifacts, and claims."""
    root = Path(repo_root)
    sources = normalize_records(list(_collect_sources(root).values()))
    artifacts = normalize_records(list(_collect_artifacts(root).values()))
    claims = normalize_records(list(_collect_claims(root).values()))

    sources_root = root / "data" / "normalized" / "sources"
    artifacts_root = root / "data" / "normalized" / "artifacts"
    claims_root = root / "data" / "normalized" / "claims"
    source_docs_root = sources_root / "documents"
    artifact_docs_root = artifacts_root / "documents"
    claim_docs_root = claims_root / "documents"

    _clear_yaml_files(source_docs_root)
    _clear_yaml_files(artifact_docs_root)
    _clear_yaml_files(claim_docs_root)

    for document in sources:
        _write_yaml(source_docs_root / f"{document['id']}.yaml", document)
    for document in artifacts:
        _write_yaml(artifact_docs_root / f"{document['id']}.yaml", document)
    for document in claims:
        _write_yaml(claim_docs_root / f"{document['id']}.yaml", document)

    source_bundle_path = sources_root / "sources-bundle.yaml"
    artifact_bundle_path = artifacts_root / "artifacts-bundle.yaml"
    claim_bundle_path = claims_root / "claims-bundle.yaml"

    _write_yaml(
        source_bundle_path,
        _bundle_document(
            "reg_normalized_sources",
            "normalized_source_bundle",
            "Deterministic normalized source bundle built from authored source records.",
            sources,
        ),
    )
    _write_yaml(
        artifact_bundle_path,
        _bundle_document(
            "reg_normalized_artifacts",
            "normalized_artifact_bundle",
            "Deterministic normalized artifact bundle built from authored artifact records.",
            artifacts,
        ),
    )
    _write_yaml(
        claim_bundle_path,
        _bundle_document(
            "reg_normalized_claims",
            "normalized_claim_bundle",
            "Deterministic normalized claim bundle built from authored claim records.",
            claims,
        ),
    )

    return {
        "sources": source_bundle_path,
        "artifacts": artifact_bundle_path,
        "claims": claim_bundle_path,
    }


def register_source(repo_root: str | Path, source: dict[str, Any]) -> RegistrationResult:
    """Register a new authored source record and rebuild normalized outputs."""
    root = Path(repo_root)
    _raise_if_invalid(source, "register_source")

    existing_sources = _collect_sources(root)
    identifier = source["id"]
    if identifier in existing_sources:
        raise IngestionError(f"Source already exists: {identifier}")

    authored_path = _source_authored_path(root, source)
    if authored_path.exists():
        raise IngestionError(f"Authored source path already exists: {authored_path}")

    _write_yaml(authored_path, source)
    return RegistrationResult(
        record_id=identifier,
        authored_path=authored_path,
        normalized_bundle_paths=build_normalized_evidence(root),
    )


def register_artifact(repo_root: str | Path, artifact: dict[str, Any]) -> RegistrationResult:
    """Register a new authored artifact record and rebuild normalized outputs."""
    root = Path(repo_root)
    _raise_if_invalid(artifact, "register_artifact")

    sources_by_id = _collect_sources(root)
    source_id = artifact["source_id"]
    if source_id not in sources_by_id:
        raise IngestionError(f"Artifact source_id does not resolve: {source_id}")

    existing_artifacts = _collect_artifacts(root)
    identifier = artifact["id"]
    if identifier in existing_artifacts:
        raise IngestionError(f"Artifact already exists: {identifier}")
    file_hash = artifact.get("file_hash")
    if isinstance(file_hash, str) and file_hash:
        for existing in existing_artifacts.values():
            if existing.get("file_hash") == file_hash:
                raise IngestionError(f"Artifact file_hash already exists: {file_hash}")

    authored_path = _artifact_authored_path(root, sources_by_id[source_id], artifact)
    if authored_path.exists():
        raise IngestionError(f"Authored artifact path already exists: {authored_path}")

    _write_yaml(authored_path, artifact)
    return RegistrationResult(
        record_id=identifier,
        authored_path=authored_path,
        normalized_bundle_paths=build_normalized_evidence(root),
    )


def generate_claim_template(source_id: str, artifact_id: str) -> dict[str, Any]:
    """Generate an intentionally non-ingestable manual claim template."""
    artifact_token = artifact_id.removeprefix("art_")
    return {
        "id": f"clm_{artifact_token}_replace_me",
        "entity_type": "claim",
        "schema_version": "1.0.0",
        "source_id": source_id,
        "artifact_id": artifact_id,
        "text": "REPLACE_WITH_ATOMIC_NEUTRAL_CLAIM",
        "classification": "REPLACE_CLASSIFICATION",
        "status": "REPLACE_STATUS",
        "provenance": {
            "extraction_method": "manual",
            "locator": "REPLACE_WITH_ARTIFACT_LOCATOR",
            "notes": "Template only. Replace placeholders before ingestion.",
        },
    }


def _parse_claim_drafts(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]
    if isinstance(payload, dict) and payload.get("entity_type") == "claim":
        return [payload]
    if isinstance(payload, dict) and payload.get("entity_type") == "registry":
        items = payload.get("items", [])
        if isinstance(items, list):
            return [item for item in items if isinstance(item, dict)]
    raise IngestionError("Claim draft input must be a claim mapping, a list of claims, or a registry of claim items")


def _quarantine_path(repo_root: Path) -> Path:
    return repo_root / "data" / "normalized" / "claims" / "quarantine" / "claims-quarantine.yaml"


def ingest_claim_drafts(repo_root: str | Path, payload: Any) -> ClaimIngestionResult:
    """Ingest authored claim drafts, quarantine invalid drafts, and rebuild normalized outputs."""
    root = Path(repo_root)
    drafts = _parse_claim_drafts(payload)
    sources_by_id = _collect_sources(root)
    artifacts_by_id = _collect_artifacts(root)
    existing_claims = _collect_claims(root)
    batch_ids: set[str] = set()

    written_ids: list[str] = []
    quarantined_ids: list[str] = []
    quarantine_entries: list[dict[str, Any]] = []
    issues: list[str] = []

    for index, draft in enumerate(drafts, start=1):
        draft_id = str(draft.get("id", f"claim_draft_{index}"))
        draft_issues: list[str] = []

        try:
            schema_issues = validate_document(draft, draft_id)
            draft_issues.extend(issue.message for issue in schema_issues)
        except Exception as exc:
            draft_issues.append(str(exc))

        neutrality_issues = validate_neutrality(draft, draft_id)
        draft_issues.extend(issue.message for issue in neutrality_issues)

        provenance_issues = validate_claim_provenance(draft, draft_id, sources_by_id, artifacts_by_id)
        draft_issues.extend(issue.message for issue in provenance_issues)

        if draft_id in existing_claims:
            draft_issues.append(f"Duplicate claim ID already exists: {draft_id}")
        if draft_id in batch_ids:
            draft_issues.append(f"Duplicate claim ID in ingest batch: {draft_id}")

        if draft_issues:
            quarantined_ids.append(draft_id)
            quarantine_entries.append(
                {
                    "draft_id": draft_id,
                    "artifact_id": draft.get("artifact_id"),
                    "source_id": draft.get("source_id"),
                    "reasons": sorted(set(draft_issues)),
                    "draft": draft,
                }
            )
            issues.extend(f"{draft_id}: {message}" for message in sorted(set(draft_issues)))
            continue

        batch_ids.add(draft_id)
        authored_path = _claim_authored_path(root, draft)
        if authored_path.exists():
            message = f"Authored claim path already exists: {authored_path}"
            quarantined_ids.append(draft_id)
            quarantine_entries.append(
                {
                    "draft_id": draft_id,
                    "artifact_id": draft.get("artifact_id"),
                    "source_id": draft.get("source_id"),
                    "reasons": [message],
                    "draft": draft,
                }
            )
            issues.append(f"{draft_id}: {message}")
            continue

        _write_yaml(authored_path, draft)
        written_ids.append(draft_id)

    quarantine_path: Path | None = None
    if quarantine_entries:
        quarantine_entries = sorted(
            quarantine_entries,
            key=lambda entry: (
                str(entry.get("artifact_id", "")),
                str(entry.get("draft_id", "")),
            ),
        )
        quarantine_path = _quarantine_path(root)
        _write_yaml(
            quarantine_path,
            _bundle_document(
                "reg_claim_quarantine",
                "claim_quarantine",
                "Unsupported or incomplete claim drafts produced during manual-first claim ingestion.",
                quarantine_entries,
            ),
        )
    else:
        existing_quarantine = _quarantine_path(root)
        if existing_quarantine.exists():
            existing_quarantine.unlink()

    normalized_bundle_paths = build_normalized_evidence(root)
    return ClaimIngestionResult(
        written_ids=written_ids,
        quarantined_ids=quarantined_ids,
        quarantine_path=quarantine_path,
        normalized_bundle_paths=normalized_bundle_paths,
        issues=issues,
    )
