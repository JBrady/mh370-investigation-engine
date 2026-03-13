from pathlib import Path

from mh370_investigation_engine.validation.schema_validation import validate_document, validate_yaml_file


FIXTURES = Path(__file__).resolve().parents[1] / "fixtures"


def test_valid_artifact_schema() -> None:
    assert validate_yaml_file(FIXTURES / "valid" / "artifact.yaml") == []


def test_invalid_artifact_schema() -> None:
    assert validate_yaml_file(FIXTURES / "invalid" / "artifact.yaml")


def test_artifact_schema_accepts_raw_relpath() -> None:
    document = {
        "id": "art_fixture_with_raw_path",
        "entity_type": "artifact",
        "schema_version": "1.0.0",
        "source_id": "src_fixture_source",
        "artifact_type": "report",
        "title": "Fixture artifact with raw path",
        "raw_relpath": "data/raw/official/src_fixture_source/fixture.pdf",
    }

    assert validate_document(document, "inline-artifact") == []
