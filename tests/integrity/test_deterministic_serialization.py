from pathlib import Path

from mh370_investigation_engine.validation import validate_repository
from mh370_investigation_engine.validation.schema_validation import validate_repository_documents
from mh370_investigation_engine.yaml_io import dump_yaml, load_yaml_file, normalize_records


FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "determinism"
REPO_ROOT = Path(__file__).resolve().parents[2]


def test_yaml_dump_is_stable_for_equivalent_mappings() -> None:
    a = load_yaml_file(FIXTURES / "ordered_a.yaml")
    b = load_yaml_file(FIXTURES / "ordered_b.yaml")
    assert dump_yaml(a) == dump_yaml(b)


def test_multi_object_bundle_normalization_is_stable() -> None:
    source = load_yaml_file(REPO_ROOT / "tests" / "fixtures" / "valid" / "source.yaml")
    artifact = load_yaml_file(REPO_ROOT / "tests" / "fixtures" / "valid" / "artifact.yaml")
    claim = load_yaml_file(REPO_ROOT / "tests" / "fixtures" / "valid" / "claim.yaml")

    bundle_a = [claim, source, artifact]
    bundle_b = [artifact, claim, source]

    assert dump_yaml(normalize_records(bundle_a)) == dump_yaml(normalize_records(bundle_b))


def test_repository_documents_are_schema_valid() -> None:
    assert validate_repository_documents(REPO_ROOT) == []


def test_aggregate_repository_validation_is_clean() -> None:
    results = validate_repository(str(REPO_ROOT))
    assert all(not issues for issues in results.values())
