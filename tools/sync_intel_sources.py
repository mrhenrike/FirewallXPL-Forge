#!/usr/bin/env python3
"""Sync phase-6 external intelligence and integrate modular catalogs."""

from __future__ import annotations

# Author: André Henrique (@mrhenrike) | União Geek — https://github.com/Uniao-Geek

import csv
import json
import subprocess
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple


def _run_gh_api(endpoint: str, paginate: bool = False) -> List[dict]:
    """Run gh api command and return parsed JSON list."""
    cmd = ["gh", "api", endpoint, "-X", "GET"]
    if paginate:
        cmd.extend(["--paginate", "--slurp"])
    completed = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError("gh api failed for {}: {}".format(endpoint, completed.stderr.strip()))
    stdout = completed.stdout or ""
    if not stdout.strip():
        raise RuntimeError("gh api returned empty payload for {}".format(endpoint))
    payload = json.loads(stdout)
    if paginate:
        # --slurp returns list of pages; flatten if each page is a list.
        rows: List[dict] = []
        if isinstance(payload, list):
            for page in payload:
                if isinstance(page, list):
                    rows.extend(page)
                elif isinstance(page, dict):
                    rows.append(page)
        return rows
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        return [payload]
    return []


def _extract_github_ref(url: str) -> Tuple[str, str]:
    """Extract github owner/repo from URL. Return (owner, repo_or_empty)."""
    parsed = urllib.parse.urlparse(url)
    if "github.com" not in parsed.netloc.lower():
        return "", ""
    parts = [item for item in parsed.path.split("/") if item]
    if len(parts) >= 2:
        return parts[0], parts[1]
    if len(parts) == 1:
        return parts[0], ""
    return "", ""


def _http_probe(url: str, timeout: float = 8.0) -> Tuple[bool, int]:
    """Probe URL reachability and return (reachable, status_code)."""
    req = urllib.request.Request(url, headers={"User-Agent": "FirewallXPL-Forge-IntelSync/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            return True, int(getattr(response, "status", 200))
    except urllib.error.HTTPError as exc:
        return False, int(exc.code)
    except Exception:
        return False, 0


def _write_json(path: Path, payload: object) -> None:
    """Write UTF-8 JSON payload with stable formatting."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def _write_csv(path: Path, rows: List[Dict[str, object]], fieldnames: List[str]) -> None:
    """Write CSV rows."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def main() -> int:
    """Execute phase-6 sync and integration outputs."""
    repo_root = Path(__file__).resolve().parents[1]
    catalogs_root = repo_root / "firewallxpl" / "resources" / "catalogs"
    arsenal_root = repo_root / "firewallxpl" / "resources" / "arsenal"
    log_root = repo_root / ".log"
    log_root.mkdir(parents=True, exist_ok=True)

    # 1) Pull project data (2018+ window inputs) for triage pipeline.
    issues = _run_gh_api("repos/mrhenrike/FirewallXPL-Forge/issues?state=all&since=2018-01-01T00:00:00Z&per_page=100", paginate=True)
    pulls = _run_gh_api("repos/mrhenrike/FirewallXPL-Forge/pulls?state=all&per_page=100", paginate=True)
    forks = _run_gh_api("repos/mrhenrike/FirewallXPL-Forge/forks?sort=newest&per_page=100", paginate=True)
    _write_json(log_root / "issues_2018plus.json", issues)
    _write_json(log_root / "prs_all.json", pulls)
    _write_json(log_root / "forks_all.json", forks)

    # 2) Build live snapshot from external sources catalog.
    source_catalog = json.loads((catalogs_root / "external_tool_intel_sources.json").read_text(encoding="utf-8"))
    sources = source_catalog.get("sources", [])
    snapshot_rows: List[Dict[str, object]] = []
    now_utc = datetime.now(timezone.utc).isoformat()
    for source in sources:
        src_url = str(source.get("url", ""))
        owner, repo = _extract_github_ref(src_url)
        reachable, status_code = _http_probe(src_url)
        row: Dict[str, object] = {
            "id": str(source.get("id", "")),
            "name": str(source.get("name", "")),
            "type": str(source.get("type", "")),
            "domain": str(source.get("domain", "")),
            "url": src_url,
            "reachable": reachable,
            "http_status": status_code,
            "checked_at": now_utc,
            "github_owner": owner,
            "github_repo": repo,
            "github_stars": "",
            "github_forks": "",
            "github_open_issues": "",
            "github_updated_at": "",
        }
        if owner and repo:
            try:
                repo_meta = _run_gh_api("repos/{}/{}".format(owner, repo), paginate=False)[0]
                row["github_stars"] = repo_meta.get("stargazers_count", "")
                row["github_forks"] = repo_meta.get("forks_count", "")
                row["github_open_issues"] = repo_meta.get("open_issues_count", "")
                row["github_updated_at"] = repo_meta.get("updated_at", "")
            except Exception:
                pass
        snapshot_rows.append(row)

    snapshot_payload = {"checked_at": now_utc, "total_sources": len(snapshot_rows), "sources": snapshot_rows}
    _write_json(arsenal_root / "intel" / "external_intel_live_snapshot.json", snapshot_payload)
    _write_csv(
        log_root / "external_intel_live_snapshot.csv",
        snapshot_rows,
        [
            "id",
            "name",
            "type",
            "domain",
            "url",
            "reachable",
            "http_status",
            "checked_at",
            "github_owner",
            "github_repo",
            "github_stars",
            "github_forks",
            "github_open_issues",
            "github_updated_at",
        ],
    )

    # 3) Integrate artifacts into modular subcatalogs.
    pocs = [
        {
            "id": row["id"],
            "name": row["name"],
            "source_url": row["url"],
            "classification": "poc_pov_pof_candidate",
            "status": "catalog_only",
            "domain": row["domain"],
        }
        for row in snapshot_rows
        if any(token in str(row["type"]).lower() for token in ("algorithm", "fuzz"))
    ]
    firmware = [
        {
            "id": row["id"],
            "name": row["name"],
            "source_url": row["url"],
            "classification": "firmware_tooling_candidate",
            "status": "catalog_only",
            "domain": row["domain"],
        }
        for row in snapshot_rows
        if "firmware" in str(row["type"]).lower()
    ]
    binaries = [
        {
            "id": row["id"],
            "name": row["name"],
            "source_url": row["url"],
            "classification": "binary_tool_candidate",
            "status": "catalog_only",
            "domain": row["domain"],
        }
        for row in snapshot_rows
        if any(token in str(row["type"]).lower() for token in ("tool", "binary"))
    ]
    _write_json(arsenal_root / "pocs" / "external_poc_pov_pof_catalog.json", {"total": len(pocs), "items": pocs})
    _write_json(arsenal_root / "firmware" / "external_firmware_catalog.json", {"total": len(firmware), "items": firmware})
    _write_json(arsenal_root / "binaries" / "external_binary_catalog.json", {"total": len(binaries), "items": binaries})

    print(
        "intel_sync issues={} prs={} forks={} external_sources={} pocs={} firmware={} binaries={}".format(
            len(issues),
            len(pulls),
            len(forks),
            len(snapshot_rows),
            len(pocs),
            len(firmware),
            len(binaries),
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
