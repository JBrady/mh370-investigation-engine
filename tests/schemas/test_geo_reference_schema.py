from pathlib import Path

from mh370_investigation_engine.validation.schema_validation import validate_yaml_file


FIXTURES = Path(__file__).resolve().parents[1] / "fixtures"


def test_valid_geo_reference_schema() -> None:
    assert validate_yaml_file(FIXTURES / "valid" / "geo_reference.yaml") == []


def test_invalid_geo_reference_schema() -> None:
    assert validate_yaml_file(FIXTURES / "invalid" / "geo_reference.yaml")
