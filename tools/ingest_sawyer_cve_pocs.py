#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ingest PoC links from James Sawyer CVE Search API (JSON) into NDJSON or JSON.

OpenAPI: ``https://labs.jamessawyer.co.uk/cves/api/openapi.json``

Auth: header ``X-API-Key`` or ``Authorization: Bearer <token>`` (optional for some
client IPs; free tier may require key — see site notice).

Outputs one JSON object per line (NDJSON) by default for streaming merge into intel pipelines.

Author: André Henrique (@mrhenrike) | União Geek

"""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

LOGGER = logging.getLogger(__name__)

DEFAULT_API_BASE = "https://labs.jamessawyer.co.uk/cves/api"
DEFAULT_OUT = Path(__file__).resolve().parents[1] / ".log" / "sawyer_cve_pocs.ndjson"


def _request_cves(
    api_base: str,
    query: str,
    *,
    api_key: str | None,
    bearer: str | None,
    limit: int,
    match: str,
    timeout: float,
) -> dict[str, Any]:
    q = urllib.parse.urlencode({"q": query, "limit": str(limit), "match": match})
    url = f"{api_base.rstrip('/')}/cves?{q}"
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    if bearer:
        req.add_header("Authorization", f"Bearer {bearer}")
    elif api_key:
        req.add_header("X-API-Key", api_key)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        body = resp.read().decode("utf-8", errors="replace")
    return json.loads(body)


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch Sawyer CVE PoC API results into NDJSON/JSON.")
    parser.add_argument("--api-base", default=os.environ.get("JAMES_SAWYER_CVE_API_BASE", DEFAULT_API_BASE))
    parser.add_argument("--query", action="append", help="CVE id or substring (repeatable).")
    parser.add_argument("--cves-file", type=Path, help="File with one CVE or query per line.")
    parser.add_argument("--limit", type=int, default=100, help="Per-query limit (API max 100).")
    parser.add_argument("--match", default="auto", choices=["auto", "exact", "contains"])
    parser.add_argument("--format", choices=["ndjson", "json"], default="ndjson")
    parser.add_argument(
        "--out",
        type=Path,
        default=None,
        help="Output file (default: RouterXPL-Forge/.log/sawyer_cve_pocs.ndjson unless --stdout)",
    )
    parser.add_argument("--stdout", action="store_true", help="Print to stdout instead of --out.")
    parser.add_argument("--timeout", type=float, default=60.0)
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

    api_key = os.environ.get("JAMES_SAWYER_CVE_API_KEY") or os.environ.get("SAWYER_CVE_API_KEY")
    bearer = os.environ.get("JAMES_SAWYER_CVE_BEARER")

    queries: list[str] = list(args.query or [])
    if args.cves_file:
        text = args.cves_file.read_text(encoding="utf-8", errors="replace")
        queries.extend(line.strip() for line in text.splitlines() if line.strip() and not line.strip().startswith("#"))

    if not queries:
        LOGGER.error("Provide --query and/or --cves-file")
        return 2

    out_path = None if args.stdout else (args.out or DEFAULT_OUT)
    if out_path and not args.stdout:
        out_path.parent.mkdir(parents=True, exist_ok=True)

    all_results: list[dict[str, Any]] = []
    ndjson_fh = None
    if args.format == "ndjson" and out_path and not args.stdout:
        ndjson_fh = out_path.open("w", encoding="utf-8")

    try:
        for q in queries:
            try:
                payload = _request_cves(
                    args.api_base,
                    q,
                    api_key=api_key,
                    bearer=bearer,
                    limit=min(args.limit, 100),
                    match=args.match,
                    timeout=args.timeout,
                )
            except urllib.error.HTTPError as exc:
                LOGGER.error("HTTP %s for query=%r: %s", exc.code, q, exc.read()[:500] if exc.fp else "")
                continue
            except urllib.error.URLError as exc:
                LOGGER.error("Network error for query=%r: %s", q, exc)
                continue
            row = {
                "source": "labs.jamessawyer.co.uk/cve-api",
                "query": q,
                "api_response": payload,
            }
            all_results.append(row)
            if args.format == "ndjson":
                line = json.dumps(row, ensure_ascii=False) + "\n"
                if args.stdout:
                    sys.stdout.write(line)
                elif ndjson_fh:
                    ndjson_fh.write(line)
    finally:
        if ndjson_fh:
            ndjson_fh.close()

    if args.format == "json":
        blob = json.dumps({"records": all_results}, indent=2, ensure_ascii=False) + "\n"
        if args.stdout:
            sys.stdout.write(blob)
        elif out_path:
            out_path.write_text(blob, encoding="utf-8")

    LOGGER.info("records=%s format=%s", len(all_results), args.format)
    return 0


if __name__ == "__main__":
    sys.exit(main())
