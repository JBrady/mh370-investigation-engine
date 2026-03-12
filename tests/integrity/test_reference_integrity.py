from pathlib import Path

from mh370_investigation_engine.validation.reference_validation import (
    validate_references,
    validate_references_in_directory,
    validate_repository_references,
)
from mh370_investigation_engine.yaml_io import load_yaml_file


FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "refs"
REPO_ROOT = Path(__file__).resolve().parents[2]


def test_valid_reference_fixture_set() -> None:
    assert validate_references_in_directory(FIXTURES / "valid") == []


def test_invalid_reference_fixture_set() -> None:
    issues = validate_references_in_directory(FIXTURES / "invalid")
    assert issues
    assert any("Unresolved reference" in issue.message or "Duplicate ID" in issue.message for issue in issues)


def test_repository_reference_integrity() -> None:
    assert validate_repository_references(REPO_ROOT) == []


def test_field_aware_reference_target_validation() -> None:
    source_document = load_yaml_file(FIXTURES / "valid" / "source.yaml")
    scenario_document = load_yaml_file(FIXTURES / "valid" / "scenario.yaml")
    artifact_document = load_yaml_file(FIXTURES / "valid" / "artifact.yaml")
    artifact_document["source_id"] = "scn_refs_scenario"

    issues = validate_references(
        [
            (FIXTURES / "valid" / "source.yaml", source_document),
            (FIXTURES / "valid" / "scenario.yaml", scenario_document),
            (FIXTURES / "valid" / "artifact.yaml", artifact_document),
        ]
    )

    assert issues
    assert any("source_id" in issue.message for issue in issues)
