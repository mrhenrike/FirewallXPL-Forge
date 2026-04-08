#!/usr/bin/env python3
"""Validate yearly minimum coverage entries in market priority catalog."""

from __future__ import annotations

# Author: André Henrique (@mrhenrike) | União Geek — https://github.com/Uniao-Geek

import json
import logging
from pathlib import Path
from typing import Dict, List


LOGGER = logging.getLogger("validate_market_priority_minimums")


def _configure_logging() -> None:
    """Configure logging for command execution."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )


def _extract_ids(items: List[str], known_ids: Dict[str, Dict[str, object]]) -> List[str]:
    """Return only IDs present in device pool."""
    return [item for item in items if item in known_ids]


def main() -> int:
    """Validate minimum counts and unresolved IDs by year/segment."""
    _configure_logging()
    repo_root = Path(__file__).resolve().parent.parent
    catalog_path = repo_root / "firewallxpl" / "resources" / "catalogs" / "market_priority_devices_2010_2026.json"
    payload = json.loads(catalog_path.read_text(encoding="utf-8"))

    minimums = payload.get("minimum_targets_per_year", {})
    device_pool = payload.get("device_pool", [])
    yearly_brazil = payload.get("yearly_brazil", [])
    yearly_global = payload.get("yearly_global", [])

    known_ids = {str(item.get("id", "")): item for item in device_pool if item.get("id")}
    errors: List[str] = []

    required_domestic = int(minimums.get("brazil_domestic", 10))
    required_corporate = int(minimums.get("brazil_corporate", 10))
    required_global = int(minimums.get("global", 5))

    for entry in sorted(yearly_brazil, key=lambda x: int(x.get("year", 0))):
        year = int(entry.get("year", 0))
        domestic = [str(item) for item in entry.get("domestic", [])]
        corporate = [str(item) for item in entry.get("corporate", [])]
        domestic_resolved = _extract_ids(domestic, known_ids)
        corporate_resolved = _extract_ids(corporate, known_ids)
        domestic_missing = sorted(set(domestic) - set(domestic_resolved))
        corporate_missing = sorted(set(corporate) - set(corporate_resolved))

        if len(domestic_resolved) < required_domestic:
            errors.append(
                "year {} domestic has {} resolved entries (required {})".format(
                    year,
                    len(domestic_resolved),
                    required_domestic,
                )
            )
        if len(corporate_resolved) < required_corporate:
            errors.append(
                "year {} corporate has {} resolved entries (required {})".format(
                    year,
                    len(corporate_resolved),
                    required_corporate,
                )
            )
        if domestic_missing:
            errors.append("year {} domestic unresolved ids: {}".format(year, ", ".join(domestic_missing)))
        if corporate_missing:
            errors.append("year {} corporate unresolved ids: {}".format(year, ", ".join(corporate_missing)))

    for entry in sorted(yearly_global, key=lambda x: int(x.get("year", 0))):
        year = int(entry.get("year", 0))
        top = [str(item) for item in entry.get("top", [])]
        top_resolved = _extract_ids(top, known_ids)
        top_missing = sorted(set(top) - set(top_resolved))

        if len(top_resolved) < required_global:
            errors.append(
                "year {} global has {} resolved entries (required {})".format(
                    year,
                    len(top_resolved),
                    required_global,
                )
            )
        if top_missing:
            errors.append("year {} global unresolved ids: {}".format(year, ", ".join(top_missing)))

    if errors:
        for error in errors:
            LOGGER.error(error)
        return 1

    LOGGER.info("Market priority minimums validated successfully.")
    LOGGER.info(
        "Requirements satisfied: brazil_domestic=%s, brazil_corporate=%s, global=%s",
        required_domestic,
        required_corporate,
        required_global,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
