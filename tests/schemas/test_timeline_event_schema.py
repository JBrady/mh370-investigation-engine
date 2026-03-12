from pathlib import Path

from mh370_investigation_engine.validation.schema_validation import validate_yaml_file


FIXTURES = Path(__file__).resolve().parents[1] / "fixtures"


def test_valid_timeline_event_schema() -> None:
    assert validate_yaml_file(FIXTURES / "valid" / "timeline_event.yaml") == []


def test_invalid_timeline_event_schema() -> None:
    assert validate_yaml_file(FIXTURES / "invalid" / "timeline_event.yaml")
