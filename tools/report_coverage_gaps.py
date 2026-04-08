#!/usr/bin/env python3
"""Report device_pool coverage vs firewallxpl module paths (vendor + keyword heuristics)."""

from __future__ import annotations

# Author: André Henrique (@mrhenrike) | União Geek — https://github.com/Uniao-Geek

import csv
import json
import logging
import re
from pathlib import Path
from typing import Dict, List, Sequence

LOGGER = logging.getLogger("report_market_priority_gaps")

_VENDOR_ALIASES: Dict[str, str] = {
    "tp link": "tplink",
    "tp-link": "tplink",
    "d link": "dlink",
    "d-link": "dlink",
    "palo alto": "paloalto",
    "paloalto networks": "paloalto",
    "ubiquiti networks": "ubiquiti",
}


def _configure_logging() -> None:
    """Configure stdout logging."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )


def _normalize_vendor_key(vendor: str) -> str:
    """Map vendor display name to a token comparable with module path segments."""
    s = re.sub(r"[^a-z0-9]+", " ", (vendor or "").lower()).strip()
    for needle, mapped in _VENDOR_ALIASES.items():
        if needle in s:
            return mapped
    if not s:
        return ""
    first = s.split()[0]
    if first in ("tp", "d") and len(s.split()) > 1:
        return s.replace(" ", "")[:20]
    return first


def _vendor_token_in_path(vendor_key: str, relative_path: str) -> bool:
    """Return True if vendor token appears in a module relative path."""
    if not vendor_key:
        return False
    compact = relative_path.replace("-", "").replace("_", "")
    return vendor_key in compact


def _keyword_in_path(keywords: Sequence[str], relative_paths_lower: List[str]) -> bool:
    """Return True if any keyword is a substring of any module path."""
    for raw in keywords:
        k = str(raw).lower().strip()
        if not k:
            continue
        for rel in relative_paths_lower:
            if k in rel:
                return True
    return False


def _load_module_paths(modules_root: Path) -> List[str]:
    """Collect lowercase relative paths of non-private Python modules."""
    paths: List[str] = []
    for path in modules_root.rglob("*.py"):
        if path.name.startswith("_"):
            continue
        paths.append(path.relative_to(modules_root).as_posix().lower())
    return paths


def main() -> int:
    """Write CSV gap report and print summary counts."""
    _configure_logging()
    repo_root = Path(__file__).resolve().parent.parent
    catalog_path = repo_root / "firewallxpl" / "resources" / "catalogs" / "market_priority_devices_2010_2026.json"
    modules_root = repo_root / "firewallxpl" / "modules"
    payload = json.loads(catalog_path.read_text(encoding="utf-8"))
    pool: List[Dict[str, object]] = payload.get("device_pool", [])
    paths = _load_module_paths(modules_root)

    out_csv = repo_root / ".log" / "market_priority_gaps.csv"
    out_csv.parent.mkdir(parents=True, exist_ok=True)

    vendor_hits = 0
    keyword_hits = 0
    union = 0
    rows: List[Dict[str, str]] = []

    for dev in pool:
        vid = str(dev.get("id", ""))
        vendor = str(dev.get("vendor", ""))
        product = str(dev.get("product", ""))
        segment = str(dev.get("segment", ""))
        vkey = _normalize_vendor_key(vendor)
        kws = list(dev.get("match_keywords") or [])
        has_v = any(_vendor_token_in_path(vkey, rel) for rel in paths)
        has_k = _keyword_in_path(kws, paths) or _keyword_in_path([product], paths)
        covered = has_v or has_k
        if has_v:
            vendor_hits += 1
        if has_k:
            keyword_hits += 1
        if covered:
            union += 1
        gap = "uncovered" if not covered else "partial_or_keyword"
        rows.append(
            {
                "id": vid,
                "vendor": vendor,
                "product": product,
                "segment": segment,
                "vendor_key": vkey,
                "vendor_path_hit": "yes" if has_v else "no",
                "keyword_path_hit": "yes" if has_k else "no",
                "gap_status": gap,
            },
        )

    fieldnames = [
        "id",
        "vendor",
        "product",
        "segment",
        "vendor_key",
        "vendor_path_hit",
        "keyword_path_hit",
        "gap_status",
    ]
    with out_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    n = len(pool)
    uncovered = n - union
    LOGGER.info(
        "device_pool=%s vendor_path_hits=%s keyword_path_hits=%s union=%s uncovered=%s csv=%s",
        n,
        vendor_hits,
        keyword_hits,
        union,
        uncovered,
        out_csv.as_posix(),
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
