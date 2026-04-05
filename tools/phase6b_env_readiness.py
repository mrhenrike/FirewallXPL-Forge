#!/usr/bin/env python3
"""Check honeypot provider credential readiness for phase6b live run."""

from __future__ import annotations

# Author: André Henrique (@mrhenrike) | União Geek — https://github.com/Uniao-Geek

import csv
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List


PROVIDERS: List[Dict[str, object]] = [
    {"platform": "shodan", "required_env": ["SHODAN_API_KEY"]},
    {"platform": "censys", "required_env": ["CENSYS_API_ID", "CENSYS_API_SECRET"]},
    {"platform": "netlas", "required_env": ["NETLAS_API_KEY"]},
    {"platform": "zoomeye", "required_env": ["ZOOMEYE_API_KEY"]},
    {"platform": "fofa", "required_env": ["FOFA_EMAIL", "FOFA_KEY"]},
]


def _is_ready(keys: List[str]) -> bool:
    """Return True if all required env vars are set."""
    return all(bool(os.getenv(key)) for key in keys)


def main() -> int:
    """Generate readiness artifacts for final honeypot validation."""
    repo_root = Path(__file__).resolve().parents[1]
    log_dir = repo_root / ".log"
    log_dir.mkdir(parents=True, exist_ok=True)

    rows: List[Dict[str, object]] = []
    now = datetime.now(timezone.utc).isoformat()
    for provider in PROVIDERS:
        required = [str(item) for item in provider["required_env"]]
        ready = _is_ready(required)
        rows.append(
            {
                "platform": provider["platform"],
                "required_env": required,
                "ready": ready,
                "missing_env": [item for item in required if not os.getenv(item)],
                "checked_at": now,
            }
        )

    payload = {
        "checked_at": now,
        "providers_total": len(rows),
        "providers_ready": sum(1 for row in rows if row["ready"]),
        "providers_blocked": sum(1 for row in rows if not row["ready"]),
        "rows": rows,
    }

    json_path = log_dir / "honeypot_env_readiness.json"
    json_path.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")

    csv_path = log_dir / "honeypot_env_readiness.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["platform", "required_env", "ready", "missing_env", "checked_at"],
        )
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    "platform": row["platform"],
                    "required_env": ",".join(row["required_env"]),
                    "ready": row["ready"],
                    "missing_env": ",".join(row["missing_env"]),
                    "checked_at": row["checked_at"],
                }
            )

    print(
        "phase6b_env_readiness providers_total={} ready={} blocked={} json={} csv={}".format(
            payload["providers_total"],
            payload["providers_ready"],
            payload["providers_blocked"],
            json_path.name,
            csv_path.name,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
