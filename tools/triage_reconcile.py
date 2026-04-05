#!/usr/bin/env python3
# Author: André Henrique (@mrhenrike) | União Geek — https://github.com/Uniao-Geek
"""Reconcile triage backlog with already integrated fixes."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Dict, List, Tuple


RESOLVED_PATTERNS: Tuple[str, ...] = (
    "paramiko dsskey removed",
    "nameerror: name 'snmpengine' is not defined",
    "not supported between instances of 'tuple' and 'int'",
    "ctrl+c",
    "telnetlib",
    "pkg_resources",
    "bump requests",
    "fix netgear rax30 exploit check",
    "update autopwn.py",
    "new exploit for - zte zxv10 w812n",
    "huawei hg824* file traversal",
    "huawei hg824* auth rce",
    "exception in thread thread-5",
    "threads are terminated",
    "error using scanner/autopwn",
    "issue with autopwn",
    "can't start scanners/autopwn",
    "problem installing routersploit",
    "issue with routersploit in parrotsec",
    "need help im using termux",
    "error on termux",
    "termux",
    "add a password reset module for tp-link archer routers",
    "add new exploit for d-link from cve-2019-16920",
    "py3",
    "use is_alive in favour of isalive",
    "updated exploit.py for compatibility with python 3.9",
    "fix exploit check for routers/linksys/test_eseries_themoon_rce",
    "[hootoo] multiple unauth exploits for tripmate series",
)

INSUFFICIENT_CONTEXT_PATTERNS: Tuple[str, ...] = (
    "help",
    "not working",
    "error after run",
    "error while using the tool",
    "issue with routersploit",
    "routersploit run command error",
    "can't start scanners/autopwn",
    "terminal transcript",
    "problem installing routersploit",
    "functionality question",
)

DEFER_PHASE6_PATTERNS: Tuple[str, ...] = (
    "module request",
    "new exploit",
    "cve-",
    "auth bypass",
    "rce",
    "path traversal",
    "password disclosure",
    "hardcoded ssh credentials",
    "have port",
    "vulnerability",
    "exploit-db.com/exploits/",
    "masscan integration",
    "cable haunt",
    "gpon",
    "technicolor",
    "asus",
    "tenda",
    "d-link",
    "tp-link",
    "huawei",
    "zte",
    "watchguard",
    "cisco",
)

NON_CORE_PATTERNS: Tuple[str, ...] = (
    "update readme",
    "python source code formatting",
    "adding tests",
    "docs/",
    "create ",
    "terminal transcript",
)


def _reconcile_row(row: Dict[str, str]) -> Dict[str, str]:
    title = (row.get("title") or "").lower()
    classification = row.get("classification") or ""
    item_type = (row.get("type") or "").lower()

    if classification == "adapt_candidate" and any(pattern in title for pattern in RESOLVED_PATTERNS):
        row["classification"] = "applied_or_already_covered"
        row["reconcile_reason"] = "matched_resolved_pattern"
    elif classification == "adapt_candidate" and ("camera" in title or "dvr" in title or "printer" in title):
        row["classification"] = "rejected_out_of_scope"
        row["reconcile_reason"] = "out_of_scope_domain"
    elif classification in {"adapt_candidate", "backlog"} and any(pattern in title for pattern in INSUFFICIENT_CONTEXT_PATTERNS):
        row["classification"] = "needs_repro_context"
        row["reconcile_reason"] = "insufficient_repro_context"
    elif classification in {"adapt_candidate", "backlog"} and any(pattern in title for pattern in DEFER_PHASE6_PATTERNS):
        row["classification"] = "deferred_phase6_deep_intel"
        row["reconcile_reason"] = "deferred_to_phase6"
    elif classification in {"adapt_candidate", "backlog"} and item_type == "pr" and any(pattern in title for pattern in NON_CORE_PATTERNS):
        row["classification"] = "non_core_reference"
        row["reconcile_reason"] = "non_core_pr"
    elif classification in {"adapt_candidate", "backlog"}:
        row["classification"] = "deferred_phase6_deep_intel"
        row["reconcile_reason"] = "deferred_to_phase6_default"
    else:
        row["reconcile_reason"] = "no_change"

    return row


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    triage_csv = repo_root / ".log" / "triage_2018plus.csv"
    if not triage_csv.exists():
        raise FileNotFoundError("Missing source triage CSV: {}".format(triage_csv))

    with triage_csv.open("r", encoding="utf-8", newline="") as source_handle:
        reader = csv.DictReader(source_handle)
        rows = [_reconcile_row(dict(item)) for item in reader]

    reconciled_csv = repo_root / ".log" / "triage_2018plus_reconciled.csv"
    fields = ["type", "number", "state", "title", "classification", "url", "updated_at", "reconcile_reason"]
    with reconciled_csv.open("w", encoding="utf-8", newline="") as out_handle:
        writer = csv.DictWriter(out_handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    pending = [r for r in rows if r["classification"] in {"adapt_candidate", "backlog"}]
    pending.sort(key=lambda item: item.get("updated_at", ""), reverse=True)
    pending_top = repo_root / ".log" / "triage_pending_top.csv"
    with pending_top.open("w", encoding="utf-8", newline="") as pending_handle:
        writer = csv.DictWriter(pending_handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(pending[:150])

    summary: Dict[str, int] = {}
    for row in rows:
        key = row["classification"]
        summary[key] = summary.get(key, 0) + 1

    print("reconciled_rows={} summary={} pending={}".format(len(rows), summary, len(pending)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
