from pathlib import Path

from mh370_investigation_engine.validation.schema_validation import validate_yaml_file


FIXTURES = Path(__file__).resolve().parents[1] / "fixtures"


def test_valid_claim_link_schema() -> None:
    assert validate_yaml_file(FIXTURES / "valid" / "claim_link.yaml") == []


def test_invalid_claim_link_schema() -> None:
    assert validate_yaml_file(FIXTURES / "invalid" / "claim_link.yaml")
