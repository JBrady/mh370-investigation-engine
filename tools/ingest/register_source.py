#!/usr/bin/env python3
"""Register an authored source record and rebuild normalized bundles."""

from __future__ import annotations

import argparse

from mh370_investigation_engine.ingestion import register_source
from mh370_investigation_engine.yaml_io import load_yaml_file


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--input", required=True)
    args = parser.parse_args()

    result = register_source(args.repo_root, load_yaml_file(args.input))
    print(result.authored_path)


if __name__ == "__main__":
    main()
