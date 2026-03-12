#!/usr/bin/env python3
"""Ingest manual claim drafts and rebuild normalized claim outputs."""

from __future__ import annotations

import argparse

from mh370_investigation_engine.ingestion import ingest_claim_drafts
from mh370_investigation_engine.yaml_io import load_yaml_file


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--input", required=True)
    args = parser.parse_args()

    result = ingest_claim_drafts(args.repo_root, load_yaml_file(args.input))
    for claim_id in result.written_ids:
        print(f"written:{claim_id}")
    for claim_id in result.quarantined_ids:
        print(f"quarantined:{claim_id}")


if __name__ == "__main__":
    main()
