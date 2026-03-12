from pathlib import Path

from mh370_investigation_engine.validation.schema_validation import validate_yaml_file


FIXTURES = Path(__file__).resolve().parents[1] / "fixtures"


def test_valid_source_schema() -> None:
    assert validate_yaml_file(FIXTURES / "valid" / "source.yaml") == []


def test_invalid_source_schema() -> None:
    assert validate_yaml_file(FIXTURES / "invalid" / "source.yaml")
