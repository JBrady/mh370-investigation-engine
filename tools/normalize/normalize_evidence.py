#!/usr/bin/env python3
"""Build deterministic normalized evidence bundles from authored records."""

from __future__ import annotations

import argparse

from mh370_investigation_engine.ingestion import build_normalized_evidence


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    args = parser.parse_args()

    for path in build_normalized_evidence(args.repo_root).values():
        print(path)


if __name__ == "__main__":
    main()
