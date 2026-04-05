#!/usr/bin/env python3
# Author: André Henrique (@mrhenrike) | União Geek — https://github.com/Uniao-Geek
"""Build actionable triage backlog from upstream issues/PRs/forks."""

from __future__ import annotations

import csv
import json
from json import JSONDecoder
from pathlib import Path
from typing import Dict, Iterable, List


KEYWORDS = (
    "snmp",
    "trap",
    "http",
    "auth",
    "telnet",
    "ssh",
    "sftp",
    "mib",
    "encoding",
    "autopwn",
    "false positive",
    "pkg_resources",
    "readline",
    "telnetlib3",
)


def _load_json_stream(path: Path) -> List[dict]:
    """Load a file that may contain multiple concatenated JSON arrays."""
    text = path.read_text(encoding="utf-8", errors="ignore")
    decoder = JSONDecoder()
    cursor = 0
    payloads: List[dict] = []
    size = len(text)
    while cursor < size:
        while cursor < size and text[cursor].isspace():
            cursor += 1
        if cursor >= size:
            break
        obj, end = decoder.raw_decode(text, cursor)
        cursor = end
        if isinstance(obj, list):
            payloads.extend(obj)
        else:
            payloads.append(obj)
    return payloads


def _has_keyword(text: str) -> bool:
    lower = (text or "").lower()
    return any(keyword in lower for keyword in KEYWORDS)


def _classify(title: str, body: str, state: str) -> str:
    combined = "{} {}".format(title or "", body or "").lower()
    if any(token in combined for token in ("telnetlib", "pkg_resources", "readline", "requests", "pysnmp", "false positive")):
        return "applied_or_already_covered"
    if any(token in combined for token in ("new exploit", "cve-", "rce", "auth", "snmp", "trap", "mib", "autopwn")):
        return "adapt_candidate"
    if state.lower() == "closed":
        return "review_closed_reference"
    return "backlog"


def _normalize_issue_rows(items: Iterable[dict]) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for item in items:
        if "pull_request" in item:
            continue
        title = item.get("title") or ""
        body = item.get("body") or ""
        if not _has_keyword("{} {}".format(title, body)):
            continue
        rows.append(
            {
                "type": "issue",
                "number": str(item.get("number", "")),
                "state": str(item.get("state", "")),
                "title": title.strip(),
                "classification": _classify(title, body, str(item.get("state", ""))),
                "url": str(item.get("html_url", "")),
                "updated_at": str(item.get("updated_at", "")),
            }
        )
    return rows


def _normalize_pr_rows(items: Iterable[dict]) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for item in items:
        title = item.get("title") or ""
        body = item.get("body") or ""
        if not _has_keyword("{} {}".format(title, body)):
            continue
        rows.append(
            {
                "type": "pr",
                "number": str(item.get("number", "")),
                "state": str(item.get("state", "")),
                "title": title.strip(),
                "classification": _classify(title, body, str(item.get("state", ""))),
                "url": str(item.get("html_url", "")),
                "updated_at": str(item.get("updated_at", "")),
            }
        )
    return rows


def _normalize_fork_rows(items: Iterable[dict]) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for item in items:
        full_name = str(item.get("full_name", ""))
        description = str(item.get("description", ""))
        if not _has_keyword("{} {}".format(full_name, description)):
            continue
        rows.append(
            {
                "type": "fork",
                "number": "",
                "state": "n/a",
                "title": full_name,
                "classification": "adapt_candidate",
                "url": str(item.get("html_url", "")),
                "updated_at": str(item.get("updated_at", "")),
            }
        )
    return rows


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    log_dir = repo_root / ".log"
    issues_path = log_dir / "issues_2018plus.json"
    prs_path = log_dir / "prs_all.json"
    forks_path = log_dir / "forks_all.json"

    if not issues_path.exists() or not prs_path.exists() or not forks_path.exists():
        raise FileNotFoundError("Required source files not found in .log/: issues_2018plus.json, prs_all.json, forks_all.json")

    issues = _load_json_stream(issues_path)
    prs = _load_json_stream(prs_path)
    forks = _load_json_stream(forks_path)

    rows = []
    rows.extend(_normalize_issue_rows(issues))
    rows.extend(_normalize_pr_rows(prs))
    rows.extend(_normalize_fork_rows(forks))
    rows.sort(key=lambda item: item.get("updated_at", ""), reverse=True)

    out_csv = log_dir / "triage_2018plus.csv"
    with out_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["type", "number", "state", "title", "classification", "url", "updated_at"])
        writer.writeheader()
        writer.writerows(rows)

    summary: Dict[str, int] = {}
    for row in rows:
        summary[row["classification"]] = summary.get(row["classification"], 0) + 1

    print("triage_rows={} summary={}".format(len(rows), summary))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
