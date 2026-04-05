#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Extract Git repository URLs from tg12/PoC_CVEs link dumps (cve_links.txt / .csv).

Parses **CVE-anchored blocks** from ``cve_links.txt`` so each URL can be scored against
RouterXPL ``cve_extended_catalog.json`` (vendor/product/description) and optionally against
live GitHub metadata (**description**, **topics**, **name**) via ``gh api`` — not only the URL path.

Author: André Henrique (@mrhenrike) | União Geek

"""

from __future__ import annotations

import argparse
import csv
import json
import logging
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

LOGGER = logging.getLogger(__name__)

RXFORGE_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SUPER = RXFORGE_ROOT.parents[2]
DEFAULT_TG12 = DEFAULT_SUPER / "submodules" / "IoT" / "third-party-router-poc" / "tg12__PoC_CVEs"
DEFAULT_CVE_CATALOG = RXFORGE_ROOT / "firewallxpl" / "resources" / "catalogs" / "cve_extended_catalog.json"

_GH_REPO = re.compile(
    r"https?://github\.com/([\w.-]+)/([\w.,-]+)(?:\.git)?/?(?:[#?].*)?$", re.IGNORECASE
)
_GL_REPO = re.compile(
    r"https?://gitlab\.com/([\w./-]+)/([\w.-]+)(?:\.git)?/?(?:[#?].*)?$", re.IGNORECASE
)
_CVE_LINE = re.compile(r"CVE-\d{4}-\d+")

# Edge / RouterXPL scope tokens (URL path, README metadata, or CVE catalog blob).
_EDGE_TERMS: tuple[str, ...] = (
    "router",
    "switch",
    "firewall",
    "fortigate",
    "fortios",
    "cisco",
    "mikrot",
    "routeros",
    "tplink",
    "tp-link",
    "netgear",
    "asuswrt",
    "asus",
    "zyxel",
    "d-link",
    "dlink",
    "openwrt",
    "lede",
    "edge",
    "vpn",
    "ssl-vpn",
    "sslvpn",
    "ipsec",
    "wlan",
    "wifi",
    "wi-fi",
    "wireless",
    "access-point",
    "802.11",
    "modem",
    "gateway",
    "cpe",
    "broadband",
    "dsl",
    "gpon",
    "xgs-pon",
    "xgspon",
    "onu",
    "ont",
    "arris",
    "pace",
    "uverse",
    "u-verse",
    "bgw210",
    "nvg589",
    "nvg599",
    "embedded",
    "iot",
    "snmp",
    "upnp",
    "nat-traversal",
    "palo",
    "pan-os",
    "checkpoint",
    "gaia",
    "sophos",
    "sonicwall",
    "juniper",
    "junos",
    "srx",
    "ex2300",
    "arista",
    "nexus",
    "huawei",
    "hilink",
    "zte",
    "fiber",
    "broadcom",
    "vlan",
    "pppoe",
    "credential",
    "misfortune",
    "cgi-bin",
    "httpd",
    "lighttpd",
    "mini_httpd",
    "goahead",
    "boa",
    "alphapd",
    "tdpServer",
    "technicolor",
    "speedport",
    "vodafone",
    "sagem",
    "sercomm",
)


def _normalize_github(url: str) -> str | None:
    m = _GH_REPO.match(url.strip())
    if not m:
        return None
    owner, repo = m.group(1), m.group(2).rstrip("/")
    return f"https://github.com/{owner}/{repo}.git"


def _normalize_gitlab(url: str) -> str | None:
    m = _GL_REPO.match(url.strip())
    if not m:
        return None
    owner_path, repo = m.group(1).strip("/"), m.group(2).rstrip("/")
    return f"https://gitlab.com/{owner_path}/{repo}.git"


def _strip_cell(line: str) -> str:
    """Strip ASCII table padding and surrounding ``|`` cells."""

    return line.strip().strip("|").strip()


def _parse_tg12_txt_cve_urls(path: Path) -> list[dict[str, Any]]:
    """Return list of {cve_id, urls: [raw http...]}."""

    text = path.read_text(encoding="utf-8", errors="replace")
    entries: list[dict[str, Any]] = []
    current: str | None = None
    buf_urls: list[str] = []

    def flush() -> None:
        nonlocal current, buf_urls
        if current and buf_urls:
            entries.append({"cve_id": current, "urls": list(buf_urls)})
        buf_urls = []

    for raw in text.splitlines():
        line = raw.rstrip()
        if not line.startswith("|"):
            continue
        cell = _strip_cell(line)
        if not cell or cell.startswith("+") or set(cell) <= {"-", "+"}:
            continue
        if cell.startswith("CVE-"):
            flush()
            m = _CVE_LINE.search(cell)
            current = m.group(0) if m else None
            continue
        if cell.startswith("http") and current:
            first = cell.split()[0]
            buf_urls.append(first)
            continue

    flush()
    return entries


def _urls_from_csv(path: Path) -> set[str]:
    out: set[str] = set()
    with path.open(encoding="utf-8", errors="replace", newline="") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames or "URL" not in reader.fieldnames:
            LOGGER.warning("CSV missing URL column: %s", path)
            return out
        for row in reader:
            u = (row.get("URL") or "").strip()
            if not u:
                continue
            for norm in (_normalize_github(u), _normalize_gitlab(u)):
                if norm:
                    out.add(norm)
    return out


def _load_cve_blob_index(catalog_path: Path) -> dict[str, str]:
    if not catalog_path.is_file():
        return {}
    data = json.loads(catalog_path.read_text(encoding="utf-8"))
    entries = data.get("entries") or []
    out: dict[str, str] = {}
    for e in entries:
        cid = e.get("cve_id")
        if not cid:
            continue
        parts = [
            str(e.get("vendor", "")),
            str(e.get("product", "")),
            str(e.get("affected_versions", "")),
            str(e.get("description", "")),
        ]
        out[str(cid).upper()] = " ".join(parts).lower()
    return out


def _text_hits_edge(text: str) -> bool:
    blob = text.lower()
    return any(t in blob for t in _EDGE_TERMS)


def _url_path_hits_edge(url: str) -> bool:
    p = urlparse(url)
    blob = f"{p.path} {p.netloc}".lower()
    return _text_hits_edge(blob)


def _gh_repo_meta(owner: str, repo: str) -> dict[str, Any] | None:
    try:
        proc = subprocess.run(
            ["gh", "api", f"repos/{owner}/{repo}"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
    except (subprocess.CalledProcessError, FileNotFoundError) as exc:
        LOGGER.debug("gh api repos/%s/%s failed: %s", owner, repo, exc)
        return None
    if not proc.stdout.strip():
        return None
    return json.loads(proc.stdout)


def _meta_blob(meta: dict[str, Any]) -> str:
    topics = meta.get("topics") or []
    if not isinstance(topics, list):
        topics = []
    parts = [
        str(meta.get("name", "")),
        str(meta.get("description", "")),
        str(meta.get("homepage", "")),
        " ".join(str(t) for t in topics),
    ]
    return " ".join(parts).lower()


def _split_gh_clone(clone_url: str) -> tuple[str, str] | None:
    u = clone_url.replace("https://github.com/", "").removesuffix(".git")
    if "/" not in u:
        return None
    o, r = u.split("/", 1)
    return o, r


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Parse tg12 PoC_CVEs into clone URLs with CVE-aware / metadata filtering."
    )
    parser.add_argument("--links-dir", type=Path, default=None, help="tg12 checkout directory")
    parser.add_argument(
        "--cve-catalog",
        type=Path,
        default=DEFAULT_CVE_CATALOG,
        help="cve_extended_catalog.json for vendor/product/description tokens",
    )
    parser.add_argument(
        "--filter-edge-relevant",
        action="store_true",
        help="Keep URLs when URL path, CVE catalog text, or (--enrich-github) repo metadata hits edge terms.",
    )
    parser.add_argument(
        "--filter-router-keywords",
        action="store_true",
        help=argparse.SUPPRESS,
    )
    parser.add_argument(
        "--enrich-github",
        action="store_true",
        help="Call gh api repos/{o}/{r} for unknown matches (respect --max-enrich).",
    )
    parser.add_argument(
        "--max-enrich",
        type=int,
        default=400,
        help="Max GitHub repos to enrich when --enrich-github is set.",
    )
    parser.add_argument("--out-json", type=Path, default=None, help="Write catalog-style JSON fragment.")
    parser.add_argument("--limit", type=int, default=0, help="Cap records written to --out-json.")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

    want_filter = args.filter_edge_relevant or args.filter_router_keywords
    base = args.links_dir or DEFAULT_TG12
    if not base.is_dir():
        LOGGER.error("Links directory not found: %s", base)
        return 2

    cve_blobs = _load_cve_blob_index(args.cve_catalog) if want_filter or args.out_json else {}

    flat_pairs: list[tuple[str | None, str]] = []
    clone_urls: set[str] = set()
    txt_path = base / "cve_links.txt"
    if txt_path.is_file():
        for block in _parse_tg12_txt_cve_urls(txt_path):
            cid = block["cve_id"]
            for raw_u in block["urls"]:
                for norm in (_normalize_github(raw_u), _normalize_gitlab(raw_u)):
                    if norm:
                        clone_urls.add(norm)
                        flat_pairs.append((cid, norm))
    csv_path = base / "cve_links.csv"
    if csv_path.is_file():
        for norm in _urls_from_csv(csv_path):
            clone_urls.add(norm)
            flat_pairs.append((None, norm))

    clone_urls.discard("https://github.com/tg12/PoC_CVEs.git")

    enrich_cache: dict[str, dict[str, Any]] = {}
    enriched = 0

    def ensure_enrich(clone_u: str) -> dict[str, Any] | None:
        nonlocal enriched
        if not args.enrich_github:
            return None
        if clone_u in enrich_cache:
            return enrich_cache[clone_u]
        if enriched >= args.max_enrich:
            return None
        pr = _split_gh_clone(clone_u)
        if not pr:
            enrich_cache[clone_u] = {}
            return None
        meta = _gh_repo_meta(pr[0], pr[1])
        enriched += 1
        enrich_cache[clone_u] = meta or {}
        return enrich_cache[clone_u] or None

    if want_filter:
        by_url: dict[str, set[str]] = defaultdict(set)
        for cid, cu in flat_pairs:
            by_url[cu].add(cid or "")

        keep: set[str] = set()
        for cu in clone_urls:
            ok = _url_path_hits_edge(cu)
            if not ok:
                for cid in by_url.get(cu, ()):
                    if cid and _text_hits_edge(cve_blobs.get(cid.upper(), "")):
                        ok = True
                        break
            if not ok and args.enrich_github:
                meta = ensure_enrich(cu)
                if meta and _text_hits_edge(_meta_blob(meta)):
                    ok = True
            if ok:
                keep.add(cu)
        clone_urls = keep

    sorted_urls = sorted(clone_urls)
    LOGGER.info(
        "unique_repo_urls=%s filter=%s enrich_github=%s (dir=%s)",
        len(sorted_urls),
        want_filter,
        args.enrich_github,
        base,
    )

    if args.out_json:
        records = []
        for cu in sorted_urls:
            if "github.com/" in cu:
                tail = cu.replace("https://github.com/", "").removesuffix(".git")
                full_name: str | None = tail
                host = "github"
            elif "gitlab.com/" in cu:
                tail = cu.replace("https://gitlab.com/", "").removesuffix(".git")
                full_name = None
                host = "gitlab"
            else:
                continue
            cves_for_u = sorted({c for c, u in flat_pairs if u == cu and c})
            rec = {
                "full_name": full_name,
                "clone_url": cu,
                "host": host,
                "sources": [
                    "derived:tg12/PoC_CVEs/cve_links"
                    + ("+cve_blocks" if txt_path.is_file() else "")
                ],
                "rxforge_integration": "suggested_upstream",
                "notes": "Auto-extracted; triage license and scope. Cross-check cve_lookup / ExploitDB.",
                "related_cves_hint": cves_for_u,
            }
            em = enrich_cache.get(cu)
            if em:
                rec["github_description_preview"] = str(em.get("description") or "")[:240]
                rec["github_topics"] = em.get("topics") or []
            records.append(rec)
        if args.limit and len(records) > args.limit:
            records = records[: args.limit]
        args.out_json.parent.mkdir(parents=True, exist_ok=True)
        args.out_json.write_text(
            json.dumps({"generated_from": str(base.resolve()), "repositories": records}, indent=2),
            encoding="utf-8",
        )
        LOGGER.info("Wrote %s records to %s", len(records), args.out_json)

    for u in sorted_urls[:20]:
        print(u)
    if len(sorted_urls) > 20:
        print(f"... and {len(sorted_urls) - 20} more")

    return 0


if __name__ == "__main__":
    sys.exit(main())
