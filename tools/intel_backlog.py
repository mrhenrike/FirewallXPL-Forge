#!/usr/bin/env python3
"""Build prioritized deep-intel backlog from tracked external sources."""

from __future__ import annotations

# Author: André Henrique (@mrhenrike) | União Geek — https://github.com/Uniao-Geek

import csv
import json
import re
from pathlib import Path
from typing import Dict, List


# ---------------------------------------------------------------------------
# Keyword normalisation helpers (shared logic with generate_coverage_matrix)
# ---------------------------------------------------------------------------

def _normalize_keyword_token(value: str) -> str:
    """Strip non-alphanumeric chars for fuzzy keyword comparison."""
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
# Backlog helpers
# ---------------------------------------------------------------------------

def _priority(scope_alignment: str, integration_status: str) -> str:
    """Map source metadata to backlog priority."""
    scope = scope_alignment.lower()
    status = integration_status.lower()
    if "high" in scope and ("planned" in status or "queued" in status):
        return "p1"
    if "conditional" in scope and ("planned" in status or "queued" in status):
        return "p2"
    return "p3"


def _recommended_action(source_type: str) -> str:
    """Suggest next technical action by source type."""
    value = source_type.lower()
    if "fuzz" in value:
        return "adapter_or_wrapper_module"
    if "firmware" in value:
        return "catalog_and_parser_integration"
    if "algorithm" in value:
        return "research_and_repro_lab_validation"
    return "reference_triage"


def _collect_module_blobs(modules_root: Path) -> List[str]:
    """Build searchable blobs from every .py module file."""
    blobs: List[str] = []
    for py_file in modules_root.rglob("*.py"):
        if py_file.name.startswith("__"):
            continue
        relative = py_file.relative_to(modules_root).as_posix().lower()
        blobs.append(relative)
    return blobs


def _count_keyword_hits(blobs: List[str], keywords: List[str]) -> int:
    """Count how many module blobs match at least one keyword."""
    hits = 0
    for blob in blobs:
        if any(_keyword_matches(blob, kw) for kw in keywords):
            hits += 1
    return hits


def main() -> int:
    """Generate deep-intel backlog artifacts."""
    repo_root = Path(__file__).resolve().parents[1]
    catalogs = repo_root / "firewallxpl" / "resources" / "catalogs"
    modules_root = repo_root / "firewallxpl" / "modules"
    intel_snapshot_path = repo_root / "firewallxpl" / "resources" / "arsenal" / "intel" / "external_intel_live_snapshot.json"
    log_dir = repo_root / ".log"
    log_dir.mkdir(parents=True, exist_ok=True)

    external_sources = json.loads((catalogs / "external_tool_intel_sources.json").read_text(encoding="utf-8")).get("sources", [])
    discord_entries = json.loads((catalogs / "discord_requested_devices.json").read_text(encoding="utf-8")).get("entries", [])
    snapshot_map: Dict[str, Dict[str, object]] = {}
    if intel_snapshot_path.exists():
        snap = json.loads(intel_snapshot_path.read_text(encoding="utf-8"))
        snapshot_map = {str(item.get("id", "")): item for item in snap.get("sources", [])}

    module_blobs = _collect_module_blobs(modules_root)

    backlog: List[Dict[str, str]] = []
    for item in external_sources:
        source_id = str(item.get("id", ""))
        snap_row = snapshot_map.get(source_id, {})
        reachable = snap_row.get("reachable", "")
        status_note = "reachable={}".format(reachable) if reachable != "" else "reachable=unknown"

        # Keyword coverage check for the source name / domain
        name_keywords = [t.lower() for t in re.split(r"[\s/()]+", str(item.get("name", ""))) if len(t) >= 3]
        kw_hits = _count_keyword_hits(module_blobs, name_keywords)

        backlog.append(
            {
                "id": source_id,
                "origin": "external_source",
                "name": str(item.get("name", "")),
                "domain": str(item.get("domain", "")),
                "url": str(item.get("url", "")),
                "priority": _priority(str(item.get("scope_alignment", "")), str(item.get("integration_status", ""))),
                "recommended_action": _recommended_action(str(item.get("type", ""))),
                "keyword_hits": str(kw_hits),
                "status": "pending_analysis" if reachable != False else "source_unreachable",
                "notes": "source_type={} {}".format(item.get("type", ""), status_note),
            }
        )

    for index, entry in enumerate(discord_entries):
        keywords = [str(k).lower() for k in entry.get("match_keywords", [])]
        kw_hits = _count_keyword_hits(module_blobs, keywords)

        backlog.append(
            {
                "id": "discord-{:03d}".format(index + 1),
                "origin": "discord_feedback",
                "name": "{} {}".format(entry.get("vendor", ""), entry.get("model", "")).strip(),
                "domain": str(entry.get("segment", "")),
                "url": "",
                "priority": "p1",
                "recommended_action": "coverage_gap_validation_and_module_mapping",
                "keyword_hits": str(kw_hits),
                "status": "pending_analysis",
                "notes": str(entry.get("context", "")),
            }
        )

    backlog.sort(key=lambda row: (row["priority"], row["origin"], row["id"]))

    json_path = catalogs / "deep_intel_backlog.json"
    csv_path = log_dir / "deep_intel_backlog.csv"
    payload = {"total": len(backlog), "items": backlog}
    json_path.write_text(json.dumps(payload, indent=2, ensure_ascii=True), encoding="utf-8")

    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["id", "origin", "name", "domain", "url", "priority", "recommended_action", "keyword_hits", "status", "notes"],
        )
        writer.writeheader()
        for row in backlog:
            writer.writerow(row)

    print("deep_intel_backlog_items={} json={} csv={}".format(len(backlog), json_path.name, csv_path.name))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
