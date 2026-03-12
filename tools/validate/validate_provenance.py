#!/usr/bin/env python3
"""Validate provenance across authored claim records."""

from __future__ import annotations

import argparse

from mh370_investigation_engine.validation import validate_repository_provenance


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    args = parser.parse_args()

    issues = validate_repository_provenance(args.repo_root)
    if issues:
        for issue in issues:
            print(f"{issue.path}: {issue.message}")
        raise SystemExit(1)
    print("provenance ok")


if __name__ == "__main__":
    main()
