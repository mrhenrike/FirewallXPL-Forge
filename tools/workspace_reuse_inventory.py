#!/usr/bin/env python3
"""Mine workspace assets and classify reuse status for RouterXPL-Forge."""

from __future__ import annotations

# Author: André Henrique (@mrhenrike) | União Geek — https://github.com/Uniao-Geek

import csv
import json
import logging
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


LOGGER = logging.getLogger("workspace_reuse_inventory")

ASSET_EXTENSIONS: Dict[str, Tuple[str, ...]] = {
    "wordlist": (".txt", ".lst"),
    "mib": (".mib", ".my"),
    "firmware": (".bin", ".img", ".trx"),
    "binary": (".exe", ".elf"),
    "archive": (".zip", ".7z", ".tar", ".gz"),
    "config": (".conf", ".cfg", ".ini"),
    "script": (".py", ".sh", ".ps1"),
    "database": (".csv", ".json"),
}

ASSET_KEYWORDS: Dict[str, Tuple[str, ...]] = {
    "wordlist": ("wordlist", "password", "usernames", "credential", "cred"),
    "mib": ("mib", "snmp"),
    "firmware": ("firmware", "rom", "image"),
    "binary": ("exploit", "payload", "tool"),
    "config": ("router", "switch", "firewall", "ngfw", "tap"),
    "script": ("scan", "exploit", "snmp", "ssh", "telnet", "router", "switch"),
    "database": ("catalog", "cve", "vendor", "oui"),
}

SCOPED_TOKENS: Tuple[str, ...] = (
    "router",
    "switch",
    "tap",
    "fw",
    "ngfw",
    "snmp",
    "ssh",
    "telnet",
    "http",
    "https",
    "sftp",
    "ftp",
    "mikrotik",
    "huawei",
    "zte",
    "tplink",
    "dlink",
    "netgear",
)

OUT_OF_SCOPE_TOKENS: Tuple[str, ...] = ("camera", "printer", "dvr", "webcam")

IGNORED_DIRS: Tuple[str, ...] = (
    ".git",
    ".cursor",
    ".vscode",
    "__pycache__",
    "node_modules",
    ".venv",
    "venv",
    ".log",
)


@dataclass
class AssetRecord:
    """Normalized workspace asset entry."""

    path: str
    type: str
    size_bytes: int
    classification: str
    reason: str


def _configure_logging() -> None:
    """Configure runtime logging."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )


def _detect_type(path: Path) -> str | None:
    """Detect candidate asset type by extension or filename keywords."""
    suffix = path.suffix.lower()
    filename = path.name.lower()
    for asset_type, exts in ASSET_EXTENSIONS.items():
        if suffix in exts:
            return asset_type
    for asset_type, keys in ASSET_KEYWORDS.items():
        if any(token in filename for token in keys):
            return asset_type
    return None


def _iter_workspace_files(workspace_root: Path) -> Iterable[Path]:
    """Yield workspace files while skipping non-relevant directories."""
    for file_path in workspace_root.rglob("*"):
        if not file_path.is_file():
            continue
        if any(part in IGNORED_DIRS for part in file_path.parts):
            continue
        yield file_path


def _classify(path: Path, asset_type: str) -> Tuple[str, str]:
    """Classify asset as integrate/catalog/reject with reason."""
    normalized = path.as_posix().lower()
    if any(token in normalized for token in OUT_OF_SCOPE_TOKENS):
        return "reject", "out_of_scope_camera_printer_dvr"

    if any(token in normalized for token in SCOPED_TOKENS):
        if asset_type in {"wordlist", "mib", "database", "script", "config"}:
            return "integrate_core", "in_scope_and_directly_actionable"
        return "catalog_only", "in_scope_but_needs_manual_validation"

    if asset_type in {"archive", "binary", "firmware"}:
        return "catalog_only", "potentially_useful_binary_or_firmware_needs_review"
    return "reject", "not_in_scope_or_low_signal"


def _collect(workspace_root: Path, project_root: Path) -> List[AssetRecord]:
    """Collect and classify relevant assets from workspace."""
    records: List[AssetRecord] = []
    for file_path in _iter_workspace_files(workspace_root):
        if project_root in file_path.parents:
            continue
        asset_type = _detect_type(file_path)
        if not asset_type:
            continue
        classification, reason = _classify(file_path, asset_type)
        records.append(
            AssetRecord(
                path=file_path.as_posix(),
                type=asset_type,
                size_bytes=file_path.stat().st_size,
                classification=classification,
                reason=reason,
            )
        )
    records.sort(key=lambda r: (r.classification, r.type, r.path))
    return records


def _write_outputs(records: List[AssetRecord], project_root: Path) -> None:
    """Persist JSON catalog and CSV report."""
    catalog_path = project_root / "firewallxpl" / "resources" / "catalogs" / "workspace_reuse_inventory.json"
    csv_path = project_root / ".log" / "workspace_reuse_inventory.csv"
    catalog_path.parent.mkdir(parents=True, exist_ok=True)
    csv_path.parent.mkdir(parents=True, exist_ok=True)

    summary: Dict[str, int] = {}
    for record in records:
        summary[record.classification] = summary.get(record.classification, 0) + 1

    payload = {
        "summary": summary,
        "total": len(records),
        "records": [asdict(record) for record in records],
    }
    catalog_path.write_text(json.dumps(payload, indent=2, ensure_ascii=True), encoding="utf-8")

    with csv_path.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["path", "type", "size_bytes", "classification", "reason"])
        if handle.tell() == 0:
            writer.writeheader()
        for record in records:
            writer.writerow(asdict(record))

    LOGGER.info("Wrote %s", catalog_path)
    LOGGER.info("Appended %s", csv_path)
    LOGGER.info("Summary: %s", summary)


def main() -> int:
    """Run workspace mining and export reusable inventory."""
    _configure_logging()
    project_root = Path(__file__).resolve().parent.parent
    workspace_root = project_root.parent.parent.parent
    records = _collect(workspace_root, project_root)
    _write_outputs(records, project_root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
