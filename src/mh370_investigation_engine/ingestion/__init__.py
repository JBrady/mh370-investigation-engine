"""Manual-first ingestion helpers for Phase 2."""

from .manual_foundation import (
    ClaimIngestionResult,
    RegistrationResult,
    build_normalized_evidence,
    generate_claim_template,
    ingest_claim_drafts,
    register_artifact,
    register_source,
)

__all__ = [
    "ClaimIngestionResult",
    "RegistrationResult",
    "build_normalized_evidence",
    "generate_claim_template",
    "ingest_claim_drafts",
    "register_artifact",
    "register_source",
]
