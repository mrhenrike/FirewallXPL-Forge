#!/usr/bin/env python3
# Author: André Henrique (@mrhenrike) | União Geek — https://github.com/Uniao-Geek
"""Generate external intelligence integration status for test matrix."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Dict, List


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    source_file = repo_root / "firewallxpl" / "resources" / "catalogs" / "external_tool_intel_sources.json"
    payload = json.loads(source_file.read_text(encoding="utf-8"))
    sources: List[Dict[str, str]] = payload.get("sources", [])

    out_file = repo_root / ".log" / "external_intel_matrix.csv"
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with out_file.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "id",
                "name",
                "type",
                "domain",
                "scope_alignment",
                "integration_status",
                "test_matrix_status",
                "url",
            ],
        )
        writer.writeheader()
        for source in sources:
            writer.writerow(
                {
                    "id": source.get("id", ""),
                    "name": source.get("name", ""),
                    "type": source.get("type", ""),
                    "domain": source.get("domain", ""),
                    "scope_alignment": source.get("scope_alignment", ""),
                    "integration_status": source.get("integration_status", ""),
                    "test_matrix_status": source.get("test_matrix_status", ""),
                    "url": source.get("url", ""),
                }
            )

    print("external_sources={} output={}".format(len(sources), out_file.name))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
