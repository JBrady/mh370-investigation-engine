"""YAML helpers with deterministic serialization."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


def load_yaml_file(path: str | Path) -> Any:
    """Load a single YAML document from disk."""
    with Path(path).open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def dump_yaml(data: Any) -> str:
    """Serialize YAML with stable key ordering."""
    return yaml.safe_dump(data, sort_keys=True, allow_unicode=False)


def normalize_records(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Return records in deterministic entity/id order."""
    return sorted(
        records,
        key=lambda item: (str(item.get("entity_type", "")), str(item.get("id", ""))),
    )


def iter_yaml_paths(root: str | Path) -> list[Path]:
    """Return YAML paths in deterministic sorted order."""
    root_path = Path(root)
    return sorted(
        path
        for path in root_path.rglob("*")
        if path.is_file() and path.suffix in {".yaml", ".yml"}
    )
