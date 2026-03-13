from __future__ import annotations

from pathlib import Path

import pytest

from mh370_investigation_engine.ingestion import (
    generate_claim_template,
    ingest_claim_drafts,
    register_artifact,
    register_source,
)
from mh370_investigation_engine.ingestion.manual_foundation import IngestionError
from mh370_investigation_engine.validation import validate_repository_provenance
from mh370_investigation_engine.yaml_io import load_yaml_file


def _make_repo_root(tmp_path: Path) -> Path:
    for relative_path in (
        "sources/official",
        "sources/technical",
        "sources/media",
        "claims/by-artifact",
        "data/normalized",
        "data/raw",
        "data/derived",
    ):
        (tmp_path / relative_path).mkdir(parents=True, exist_ok=True)
    return tmp_path


def _source_document() -> dict[str, object]:
    return {
        "id": "src_phase2_source",
        "entity_type": "source",
        "schema_version": "1.0.0",
        "title": "Fixture official source",
        "source_type": "report",
        "repository_classification": "official",
        "publisher": "Fixture publisher",
    }


def _artifact_document() -> dict[str, object]:
    return {
        "id": "art_phase2_artifact",
        "entity_type": "artifact",
        "schema_version": "1.0.0",
        "source_id": "src_phase2_source",
        "artifact_type": "annex",
        "title": "Fixture artifact",
        "media_type": "application/pdf",
        "locator": "pages 1-2",
        "raw_relpath": "data/raw/official/src_phase2_source/fixture.pdf",
        "file_hash": "sha256:phase2-fixture",
        "extraction_ready": True,
    }


def _claim_document() -> dict[str, object]:
    return {
        "id": "clm_phase2_claim",
        "entity_type": "claim",
        "schema_version": "1.0.0",
        "source_id": "src_phase2_source",
        "artifact_id": "art_phase2_artifact",
        "text": "Fixture observation extracted manually from an artifact.",
        "classification": "observation",
        "status": "confirmed",
        "provenance": {
            "extraction_method": "manual",
            "locator": "page 1",
        },
    }


def test_register_source_writes_authored_and_normalized_outputs(tmp_path: Path) -> None:
    repo_root = _make_repo_root(tmp_path)

    result = register_source(repo_root, _source_document())

    assert result.authored_path == repo_root / "sources" / "official" / "src_phase2_source" / "source.yaml"
    assert result.authored_path.exists()

    source_bundle = load_yaml_file(result.normalized_bundle_paths["sources"])
    assert [item["id"] for item in source_bundle["items"]] == ["src_phase2_source"]


def test_register_artifact_writes_authored_and_normalized_outputs(tmp_path: Path) -> None:
    repo_root = _make_repo_root(tmp_path)
    register_source(repo_root, _source_document())

    result = register_artifact(repo_root, _artifact_document())

    assert result.authored_path == (
        repo_root / "sources" / "official" / "src_phase2_source" / "artifacts" / "art_phase2_artifact.yaml"
    )
    assert result.authored_path.exists()

    artifact_bundle = load_yaml_file(result.normalized_bundle_paths["artifacts"])
    assert [item["id"] for item in artifact_bundle["items"]] == ["art_phase2_artifact"]
    assert artifact_bundle["items"][0]["raw_relpath"] == "data/raw/official/src_phase2_source/fixture.pdf"


def test_duplicate_artifact_file_hash_is_rejected(tmp_path: Path) -> None:
    repo_root = _make_repo_root(tmp_path)
    register_source(repo_root, _source_document())
    register_artifact(repo_root, _artifact_document())

    duplicate = {
        **_artifact_document(),
        "id": "art_phase2_duplicate",
    }

    with pytest.raises(IngestionError):
        register_artifact(repo_root, duplicate)


def test_duplicate_artifact_id_is_rejected(tmp_path: Path) -> None:
    repo_root = _make_repo_root(tmp_path)
    register_source(repo_root, _source_document())
    register_artifact(repo_root, _artifact_document())

    duplicate = {
        **_artifact_document(),
        "file_hash": "sha256:phase2-other-fixture",
    }

    with pytest.raises(IngestionError):
        register_artifact(repo_root, duplicate)


def test_generate_claim_template_is_intentionally_non_ingestable() -> None:
    template = generate_claim_template("src_phase2_source", "art_phase2_artifact")

    assert template["source_id"] == "src_phase2_source"
    assert template["artifact_id"] == "art_phase2_artifact"
    assert template["classification"] == "REPLACE_CLASSIFICATION"
    assert template["status"] == "REPLACE_STATUS"


def test_claim_ingestion_writes_claim_and_normalized_bundle(tmp_path: Path) -> None:
    repo_root = _make_repo_root(tmp_path)
    register_source(repo_root, _source_document())
    register_artifact(repo_root, _artifact_document())

    result = ingest_claim_drafts(
        repo_root,
        {
            "id": "reg_phase2_claim_batch",
            "entity_type": "registry",
            "schema_version": "1.0.0",
            "registry_type": "claim_draft_batch",
            "items": [_claim_document()],
        },
    )

    authored_claim_path = repo_root / "claims" / "by-artifact" / "art_phase2_artifact" / "clm_phase2_claim.yaml"
    assert result.written_ids == ["clm_phase2_claim"]
    assert result.quarantined_ids == []
    assert result.quarantine_path is None
    assert authored_claim_path.exists()

    claim_bundle = load_yaml_file(result.normalized_bundle_paths["claims"])
    assert [item["id"] for item in claim_bundle["items"]] == ["clm_phase2_claim"]


def test_claim_ingestion_quarantines_incomplete_claims(tmp_path: Path) -> None:
    repo_root = _make_repo_root(tmp_path)
    register_source(repo_root, _source_document())
    register_artifact(repo_root, _artifact_document())

    invalid_claim = _claim_document()
    invalid_claim["id"] = "clm_phase2_missing_locator"
    invalid_claim["provenance"] = {"extraction_method": "manual"}

    result = ingest_claim_drafts(
        repo_root,
        {
            "id": "reg_phase2_invalid_batch",
            "entity_type": "registry",
            "schema_version": "1.0.0",
            "registry_type": "claim_draft_batch",
            "items": [invalid_claim],
        },
    )

    assert result.written_ids == []
    assert result.quarantined_ids == ["clm_phase2_missing_locator"]
    assert result.quarantine_path is not None
    quarantine = load_yaml_file(result.quarantine_path)
    assert quarantine["items"][0]["draft_id"] == "clm_phase2_missing_locator"
    assert any("locator" in reason.lower() for reason in quarantine["items"][0]["reasons"])


def test_claim_ingestion_quarantines_template_placeholder_content(tmp_path: Path) -> None:
    repo_root = _make_repo_root(tmp_path)
    register_source(repo_root, _source_document())
    register_artifact(repo_root, _artifact_document())

    template_like_claim = generate_claim_template("src_phase2_source", "art_phase2_artifact")
    template_like_claim["classification"] = "observation"
    template_like_claim["status"] = "confirmed"

    result = ingest_claim_drafts(
        repo_root,
        {
            "id": "reg_phase2_template_batch",
            "entity_type": "registry",
            "schema_version": "1.0.0",
            "registry_type": "claim_draft_batch",
            "items": [template_like_claim],
        },
    )

    assert result.written_ids == []
    assert result.quarantined_ids == [template_like_claim["id"]]
    quarantine = load_yaml_file(result.quarantine_path)
    reasons = quarantine["items"][0]["reasons"]
    assert any("template placeholder content remains" in reason.lower() for reason in reasons)


def test_claim_ingestion_quarantines_non_mapping_batch_entries(tmp_path: Path) -> None:
    repo_root = _make_repo_root(tmp_path)
    register_source(repo_root, _source_document())
    register_artifact(repo_root, _artifact_document())

    result = ingest_claim_drafts(
        repo_root,
        {
            "id": "reg_phase2_malformed_batch",
            "entity_type": "registry",
            "schema_version": "1.0.0",
            "registry_type": "claim_draft_batch",
            "items": ["TODO_not_a_claim_mapping"],
        },
    )

    assert result.written_ids == []
    assert result.quarantined_ids == ["claim_draft_1"]
    quarantine = load_yaml_file(result.quarantine_path)
    assert quarantine["items"][0]["draft"] == "TODO_not_a_claim_mapping"
    assert quarantine["items"][0]["reasons"] == ["Claim draft entry is not a mapping"]


def test_repository_provenance_validation_detects_mismatched_source_artifact_pair(tmp_path: Path) -> None:
    repo_root = _make_repo_root(tmp_path)
    register_source(repo_root, _source_document())
    register_artifact(repo_root, _artifact_document())

    mismatched_claim = _claim_document()
    mismatched_claim["id"] = "clm_phase2_mismatched_source"
    mismatched_claim["source_id"] = "src_other_source"

    claim_path = repo_root / "claims" / "by-artifact" / "art_phase2_artifact" / "clm_phase2_mismatched_source.yaml"
    claim_path.parent.mkdir(parents=True, exist_ok=True)
    claim_path.write_text(
        "\n".join(
            [
                'id: clm_phase2_mismatched_source',
                "entity_type: claim",
                'schema_version: "1.0.0"',
                "source_id: src_other_source",
                "artifact_id: art_phase2_artifact",
                "text: Fixture mismatched claim.",
                "classification: observation",
                "status: confirmed",
                "provenance:",
                "  extraction_method: manual",
                "  locator: page 1",
                "",
            ]
        ),
        encoding="utf-8",
    )

    issues = validate_repository_provenance(repo_root)
    assert issues
    assert any("does not match" in issue.message for issue in issues)


def test_duplicate_claim_ids_are_quarantined(tmp_path: Path) -> None:
    repo_root = _make_repo_root(tmp_path)
    register_source(repo_root, _source_document())
    register_artifact(repo_root, _artifact_document())

    first_result = ingest_claim_drafts(
        repo_root,
        {
            "id": "reg_phase2_first_batch",
            "entity_type": "registry",
            "schema_version": "1.0.0",
            "registry_type": "claim_draft_batch",
            "items": [_claim_document()],
        },
    )
    assert first_result.written_ids == ["clm_phase2_claim"]

    duplicate_claim = _claim_document()
    duplicate_claim["text"] = "Fixture duplicate claim with the same ID."
    second_result = ingest_claim_drafts(
        repo_root,
        {
            "id": "reg_phase2_duplicate_batch",
            "entity_type": "registry",
            "schema_version": "1.0.0",
            "registry_type": "claim_draft_batch",
            "items": [duplicate_claim],
        },
    )

    assert second_result.written_ids == []
    assert second_result.quarantined_ids == ["clm_phase2_claim"]
    assert any("Duplicate claim ID already exists" in issue for issue in second_result.issues)
