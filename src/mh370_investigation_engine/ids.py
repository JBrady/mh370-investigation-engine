"""ID conventions for repository object types."""

from __future__ import annotations

PREFIX_BY_ENTITY_TYPE = {
    "artifact": "art_",
    "claim": "clm_",
    "claim_link": "lnk_",
    "constraint": "con_",
    "geo_reference": "geo_",
    "reasoning_report": "rpt_",
    "registry": "reg_",
    "scenario": "scn_",
    "source": "src_",
    "timeline_event": "evt_",
}

ENTITY_TYPE_BY_PREFIX = {prefix: entity for entity, prefix in PREFIX_BY_ENTITY_TYPE.items()}


def expected_prefix(entity_type: str) -> str | None:
    """Return the expected ID prefix for an entity type."""
    return PREFIX_BY_ENTITY_TYPE.get(entity_type)


def detect_entity_type_from_id(value: str) -> str | None:
    """Return the entity type implied by a typed ID."""
    for prefix, entity_type in ENTITY_TYPE_BY_PREFIX.items():
        if value.startswith(prefix):
            return entity_type
    return None


def has_expected_prefix(entity_type: str, value: str) -> bool:
    """Check whether an ID matches the configured prefix for its entity type."""
    prefix = expected_prefix(entity_type)
    return prefix is not None and value.startswith(prefix)
