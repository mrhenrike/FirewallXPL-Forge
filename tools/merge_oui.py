#!/usr/bin/env python3
# Author: André Henrique (@mrhenrike) | União Geek — https://github.com/Uniao-Geek
"""Merge OUI from multi-sources with precedence and confidence score."""

from __future__ import annotations

import csv
import re
import urllib.request
from pathlib import Path
from typing import Dict, List, Tuple


IEEE_OUI = "https://standards-oui.ieee.org/oui/oui.txt"
WIRESHARK_MANUF = "https://www.wireshark.org/download/automated/data/manuf"
NMAP_MAC_PREFIXES = "https://raw.githubusercontent.com/nmap/nmap/master/nmap-mac-prefixes"

PRECEDENCE = ("ieee", "wireshark", "nmap")
CONFIDENCE = {"ieee": 1.00, "wireshark": 0.90, "nmap": 0.85}


def _http_text(url: str, timeout: int = 60) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": "FirewallXPL-Forge-OUI/1.0"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read().decode("utf-8", errors="ignore")


def _parse_ieee(data: str) -> Dict[str, str]:
    result: Dict[str, str] = {}
    pattern = re.compile(r"^([0-9A-Fa-f]{6})\s+\(base 16\)\s+(.+)$")
    for line in data.splitlines():
        match = pattern.match(line.strip())
        if not match:
            continue
        prefix = match.group(1).upper()
        vendor = match.group(2).strip()
        result[prefix] = vendor
    return result


def _parse_wireshark(data: str) -> Dict[str, str]:
    result: Dict[str, str] = {}
    for line in data.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split("\t")
        if len(parts) < 2:
            continue
        prefix = parts[0].replace(":", "").replace("-", "").upper()
        if len(prefix) < 6:
            continue
        prefix = prefix[:6]
        vendor = parts[1].strip()
        if vendor:
            result[prefix] = vendor
    return result


def _parse_nmap(data: str) -> Dict[str, str]:
    result: Dict[str, str] = {}
    for line in data.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if " " not in line:
            continue
        prefix, vendor = line.split(None, 1)
        prefix = prefix.replace(":", "").replace("-", "").upper()
        if len(prefix) < 6:
            continue
        prefix = prefix[:6]
        result[prefix] = vendor.strip()
    return result


def _pick_best(source_values: Dict[str, Dict[str, str]], prefix: str) -> Tuple[str, str]:
    for source in PRECEDENCE:
        vendor = source_values.get(source, {}).get(prefix)
        if vendor:
            return source, vendor
    return "unknown", "Unknown Vendor"


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    vendors_dir = repo_root / "firewallxpl" / "resources" / "vendors"
    vendors_dir.mkdir(parents=True, exist_ok=True)

    ieee = _parse_ieee(_http_text(IEEE_OUI))
    wireshark = _parse_wireshark(_http_text(WIRESHARK_MANUF))
    nmap = _parse_nmap(_http_text(NMAP_MAC_PREFIXES))

    source_values = {"ieee": ieee, "wireshark": wireshark, "nmap": nmap}
    all_prefixes = sorted(set().union(*[set(values.keys()) for values in source_values.values()]))

    oui_lines: List[str] = []
    enriched_rows: List[Tuple[str, str, str, float, str, str]] = []

    for prefix in all_prefixes:
        source, vendor = _pick_best(source_values, prefix)
        confidence = CONFIDENCE.get(source, 0.5)

        alt_sources = []
        alt_vendors = []
        for alt_source, values in source_values.items():
            alt_vendor = values.get(prefix)
            if not alt_vendor or alt_source == source:
                continue
            alt_sources.append(alt_source)
            alt_vendors.append(alt_vendor)

        oui_lines.append("{} {}".format(prefix, vendor))
        enriched_rows.append(
            (
                prefix,
                vendor,
                source,
                confidence,
                ",".join(alt_sources),
                " | ".join(alt_vendors),
            )
        )

    (vendors_dir / "oui.dat").write_text("\n".join(oui_lines) + "\n", encoding="utf-8")

    with (vendors_dir / "oui_enriched.csv").open("w", encoding="utf-8", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["prefix", "vendor", "source", "confidence", "alt_sources", "alt_vendors"])
        writer.writerows(enriched_rows)

    print(
        "Merged OUI entries: ieee={} wireshark={} nmap={} total={}".format(
            len(ieee), len(wireshark), len(nmap), len(all_prefixes)
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
