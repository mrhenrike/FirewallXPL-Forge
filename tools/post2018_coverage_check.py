#!/usr/bin/env python3
# Author: André Henrique (@mrhenrike) | União Geek — https://github.com/Uniao-Geek
"""Check scan/discovery coverage against post-2018 network device catalog."""

from __future__ import annotations

import csv
import json
import re
from pathlib import Path
from typing import Dict, List, Set


# ---------------------------------------------------------------------------
# Keyword normalisation helpers (same logic as generate_coverage_matrix.py)
# ---------------------------------------------------------------------------

def _normalize_keyword_token(value: str) -> str:
    """Strip all non-alphanumeric chars so variants like tl-wr740n / tlwr740n match."""
    return re.sub(r"[^a-z0-9]+", "", (value or "").lower())


def _keyword_matches(blob: str, keyword: str) -> bool:
    """Return True when *keyword* matches *blob* in raw or compacted form."""
    raw_blob = (blob or "").lower()
    raw_kw = (keyword or "").lower().strip()
    if not raw_kw:
        return False
    if raw_kw in raw_blob:
        return True
    compact_blob = _normalize_keyword_token(raw_blob)
    compact_kw = _normalize_keyword_token(raw_kw)
    if not compact_kw:
        return False
    return compact_kw in compact_blob


# ---------------------------------------------------------------------------
# Module discovery
# ---------------------------------------------------------------------------

def _discover_supported_vendors(modules_root: Path) -> Set[str]:
    """Return set of vendor folder names found under exploits/creds/scanners."""
    vendors: Set[str] = set()
    for branch in ("exploits", "creds", "scanners"):
        routers_root = modules_root / branch / "routers"
        if not routers_root.exists():
            continue
        for item in routers_root.iterdir():
            if item.is_dir():
                vendors.add(item.name.lower())
    vendors.update({"generic", "multi"})
    return vendors


def _collect_module_blobs(modules_root: Path) -> List[str]:
    """Build a list of searchable blobs from every .py module file."""
    blobs: List[str] = []
    for py_file in modules_root.rglob("*.py"):
        if py_file.name.startswith("__"):
            continue
        relative = py_file.relative_to(modules_root).as_posix().lower()
        blobs.append(relative)
    return blobs


def _normalize_vendor(vendor: str) -> str:
    """Normalise vendor labels for matching."""
    v = (vendor or "").strip().lower()
    aliases = {
        "tp-link": "tplink",
        "d-link": "dlink",
        "mikro tik": "mikrotik",
        "rogers/shaw": "rogers",
        "isp multi-vendor": "multi",
    }
    return aliases.get(v, v)


def _product_keywords(product: str) -> List[str]:
    """Derive searchable keywords from a product name."""
    raw = (product or "").strip()
    if not raw:
        return []
    tokens: List[str] = [raw.lower()]
    # Add individual significant words (len >= 3)
    for word in re.split(r"[\s/()]+", raw):
        word_clean = word.strip().lower()
        if len(word_clean) >= 3 and word_clean not in tokens:
            tokens.append(word_clean)
    return tokens


def main() -> int:
    """Generate post-2018 device coverage CSV with keyword-level matching."""
    repo_root = Path(__file__).resolve().parents[1]
    modules_root = repo_root / "firewallxpl" / "modules"
    catalog_path = repo_root / "firewallxpl" / "resources" / "catalogs" / "post2018_network_devices.json"

    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    entries: List[Dict[str, str]] = catalog.get("entries", [])
    supported_vendors = _discover_supported_vendors(modules_root)
    module_blobs = _collect_module_blobs(modules_root)

    out_rows = []
    for entry in entries:
        vendor_raw = str(entry.get("vendor", ""))
        product_raw = str(entry.get("product", ""))
        vendor_norm = _normalize_vendor(vendor_raw)
        covered = (
            vendor_norm in supported_vendors
            or vendor_norm in {"rogers", "comcast", "isp", "multi", "isp multi-vendor"}
            or "multi" in supported_vendors
        )

        # Keyword-level coverage check against module paths
        keywords = _product_keywords(product_raw)
        keyword_hits = 0
        for blob in module_blobs:
            if any(_keyword_matches(blob, kw) for kw in keywords):
                keyword_hits += 1

        out_rows.append(
            {
                "year": entry.get("year"),
                "vendor": vendor_raw,
                "product": product_raw,
                "segment": entry.get("segment"),
                "vendor_normalized": vendor_norm,
                "covered_by_vendor_modules": "yes" if covered else "no",
                "keyword_hits": keyword_hits,
            }
        )

    out_rows.sort(key=lambda item: (int(item["year"]), str(item["vendor"])))
    output_csv = repo_root / ".log" / "post2018_device_coverage.csv"
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    with output_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "year",
                "vendor",
                "product",
                "segment",
                "vendor_normalized",
                "covered_by_vendor_modules",
                "keyword_hits",
            ],
        )
        writer.writeheader()
        writer.writerows(out_rows)

    totals = len(out_rows)
    covered = sum(1 for row in out_rows if row["covered_by_vendor_modules"] == "yes")
    kw_total = sum(int(row["keyword_hits"]) for row in out_rows)
    print("catalog_entries={} covered={} uncovered={} keyword_hits_total={} output={}".format(
        totals, covered, totals - covered, kw_total, output_csv.name))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
