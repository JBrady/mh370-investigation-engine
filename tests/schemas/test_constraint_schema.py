from pathlib import Path

from mh370_investigation_engine.validation.schema_validation import validate_yaml_file


FIXTURES = Path(__file__).resolve().parents[1] / "fixtures"


def test_valid_constraint_schema() -> None:
    assert validate_yaml_file(FIXTURES / "valid" / "constraint.yaml") == []


def test_valid_placeholder_constraint_schema() -> None:
    assert validate_yaml_file(FIXTURES / "valid" / "constraint_placeholder.yaml") == []


def test_invalid_constraint_schema() -> None:
    assert validate_yaml_file(FIXTURES / "invalid" / "constraint.yaml")


def test_non_placeholder_constraint_requires_basis_refs() -> None:
    assert validate_yaml_file(FIXTURES / "invalid" / "constraint_empty_basis.yaml")
