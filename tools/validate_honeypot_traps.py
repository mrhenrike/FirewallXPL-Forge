#!/usr/bin/env python3
"""Prepare and execute final honeypot validation campaign (defensive/intrusive)."""

from __future__ import annotations

# Author: André Henrique (@mrhenrike) | União Geek — https://github.com/Uniao-Geek

import csv
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List


PLATFORMS: List[Dict[str, object]] = [
    {
        "name": "shodan",
        "required_env": ["SHODAN_API_KEY"],
        "query_templates": [
            "product:GoAhead honeypot",
            "product:MikroTik honeypot",
            "port:23 honeypot router",
            "port:161 honeypot snmp",
        ],
    },
    {
        "name": "censys",
        "required_env": ["CENSYS_API_ID", "CENSYS_API_SECRET"],
        "query_templates": [
            "services.software.product: honeypot AND services.port: 22",
            "services.banner: cowrie OR dionaea",
            "services.port: 161 AND services.banner: snmp",
        ],
    },
    {
        "name": "netlas",
        "required_env": ["NETLAS_API_KEY"],
        "query_templates": [
            "honeypot AND (router OR switch)",
            "snmp AND honeypot",
            "telnet AND honeypot",
        ],
    },
    {
        "name": "zoomeye",
        "required_env": ["ZOOMEYE_API_KEY"],
        "query_templates": [
            "app:\"honeypot\" +port:23",
            "app:\"router\" +honeypot",
            "service:\"snmp\" +honeypot",
        ],
    },
    {
        "name": "fofa",
        "required_env": ["FOFA_EMAIL", "FOFA_KEY"],
        "query_templates": [
            "body=\"honeypot\" && (title=\"router\" || title=\"switch\")",
            "protocol=\"telnet\" && body=\"cowrie\"",
            "protocol=\"snmp\" && body=\"honeypot\"",
        ],
    },
]


def _env_ready(required_env: List[str]) -> bool:
    """Return True when all required environment variables are available."""
    return all(bool(os.getenv(item)) for item in required_env)


def main() -> int:
    """Generate final honeypot campaign artifacts with live-readiness status."""
    repo_root = Path(__file__).resolve().parents[1]
    intel_dir = repo_root / "firewallxpl" / "resources" / "arsenal" / "intel"
    log_dir = repo_root / ".log"
    intel_dir.mkdir(parents=True, exist_ok=True)
    log_dir.mkdir(parents=True, exist_ok=True)

    rows: List[Dict[str, object]] = []
    now = datetime.now(timezone.utc).isoformat()
    for platform in PLATFORMS:
        required_env = [str(item) for item in platform["required_env"]]
        ready = _env_ready(required_env)
        for query in platform["query_templates"]:
            rows.append(
                {
                    "platform": platform["name"],
                    "required_env": ",".join(required_env),
                    "live_ready": ready,
                    "mode_defensive": "enabled",
                    "mode_intrusive": "enabled_controlled",
                    "query_template": query,
                    "status": "ready_for_live_run" if ready else "blocked_missing_credentials",
                    "checked_at": now,
                }
            )

    payload = {
        "checked_at": now,
        "campaign": "honeypot_validation",
        "modes": {
            "defensive": {
                "description": "non-intrusive checks only",
                "actions": ["fingerprint", "banner_collection", "check_only"],
            },
            "intrusive": {
                "description": "controlled active validation",
                "limits": {
                    "thread_min": 1,
                    "thread_max": 20,
                    "timeout_s": 20,
                    "retries": 1,
                },
                "actions": ["controlled_module_run", "post_validation_evidence"],
            },
        },
        "entries": rows,
    }

    json_path = intel_dir / "honeypot_validation_campaign.json"
    json_path.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")

    csv_path = log_dir / "honeypot_validation_campaign.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "platform",
                "required_env",
                "live_ready",
                "mode_defensive",
                "mode_intrusive",
                "query_template",
                "status",
                "checked_at",
            ],
        )
        writer.writeheader()
        for row in rows:
            writer.writerow(row)

    ready_count = sum(1 for row in rows if row["live_ready"])
    print(
        "honeypot_validation entries={} live_ready_entries={} json={} csv={}".format(
            len(rows),
            ready_count,
            json_path.name,
            csv_path.name,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
