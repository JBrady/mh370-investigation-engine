from pathlib import Path

from mh370_investigation_engine.validation.schema_validation import validate_document, validate_yaml_file


FIXTURES = Path(__file__).resolve().parents[1] / "fixtures"


def test_valid_registry_schema() -> None:
    assert validate_yaml_file(FIXTURES / "valid" / "registry.yaml") == []


def test_invalid_registry_schema() -> None:
    assert validate_yaml_file(FIXTURES / "invalid" / "registry.yaml")


def test_valid_claim_quarantine_registry_schema() -> None:
    document = {
        "id": "reg_fixture_claim_quarantine",
        "entity_type": "registry",
        "schema_version": "1.0.0",
        "registry_type": "claim_quarantine",
        "description": "Fixture quarantine registry.",
        "items": [
            {
                "draft_id": "clm_fixture_claim",
                "artifact_id": "art_fixture_artifact",
                "source_id": "src_fixture_source",
                "reasons": ["Fixture quarantine reason"],
                "draft": {
                    "id": "clm_fixture_claim",
                    "entity_type": "claim",
                },
            }
        ],
    }

    assert validate_document(document, "inline-claim-quarantine") == []


def test_valid_normalized_artifact_bundle_item_with_raw_relpath() -> None:
    document = {
        "id": "reg_fixture_artifacts",
        "entity_type": "registry",
        "schema_version": "1.0.0",
        "registry_type": "normalized_artifact_bundle",
        "description": "Fixture normalized artifact bundle.",
        "items": [
            {
                "id": "art_fixture_artifact",
                "entity_type": "artifact",
                "schema_version": "1.0.0",
                "source_id": "src_fixture_source",
                "artifact_type": "report",
                "title": "Fixture artifact",
                "raw_relpath": "data/raw/official/src_fixture_source/fixture.pdf",
            }
        ],
    }

    assert validate_document(document, "inline-artifact-bundle") == []
