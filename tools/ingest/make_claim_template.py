#!/usr/bin/env python3
"""Generate a manual claim authoring template."""

from __future__ import annotations

import argparse
from pathlib import Path

from mh370_investigation_engine.ingestion import generate_claim_template
from mh370_investigation_engine.yaml_io import dump_yaml


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-id", required=True)
    parser.add_argument("--artifact-id", required=True)
    parser.add_argument("--output")
    args = parser.parse_args()

    template = generate_claim_template(args.source_id, args.artifact_id)
    rendered = dump_yaml(template)
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(rendered, encoding="utf-8")
        print(output_path)
        return
    print(rendered, end="")


if __name__ == "__main__":
    main()
