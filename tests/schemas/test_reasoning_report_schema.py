from pathlib import Path

from mh370_investigation_engine.validation.schema_validation import validate_yaml_file


FIXTURES = Path(__file__).resolve().parents[1] / "fixtures"


def test_valid_reasoning_report_schema() -> None:
    assert validate_yaml_file(FIXTURES / "valid" / "reasoning_report.yaml") == []


def test_invalid_reasoning_report_schema() -> None:
    assert validate_yaml_file(FIXTURES / "invalid" / "reasoning_report.yaml")
