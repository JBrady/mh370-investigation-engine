from pathlib import Path

from mh370_investigation_engine.validation.neutrality_validation import (
    validate_neutrality,
    validate_repository_neutrality,
)
from mh370_investigation_engine.yaml_io import load_yaml_file


REPO_ROOT = Path(__file__).resolve().parents[2]


def test_repository_neutrality() -> None:
    assert validate_repository_neutrality(REPO_ROOT) == []


def test_claim_with_scenario_reference_fails_neutrality() -> None:
    document = load_yaml_file(Path(__file__).resolve().parents[1] / "fixtures" / "valid" / "claim.yaml")
    document["scenario_id"] = "scn_fixture_scenario"
    issues = validate_neutrality(document, "inline-fixture")
    assert issues
    assert any("scenario" in issue.message.lower() for issue in issues)
