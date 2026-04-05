#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Collect GitHub repository URLs from search queries and merge with a static seed list.

The GitHub Search API returns at most 1000 results per query. This script paginates until
exhausted or the cap is reached, then deduplicates by full name.

Author: André Henrique (@mrhenrike) | União Geek

"""

from __future__ import annotations

import json
import logging
import re
import subprocess
import sys
import urllib.parse
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any

LOGGER = logging.getLogger(__name__)

RXFORGE_ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = RXFORGE_ROOT / "firewallxpl" / "resources" / "catalogs"

SEARCH_QUERIES = (
    "exploit router",
    "exploit tap",
    "exploit firewall",
    "exploit utm",
)

# User-provided seed URLs (deduped). GitLab and GitHub normalized to clone HTTPS.
SEED_CLONE_URLS = [
    "https://github.com/openwrt-xiaomi/xmir-patcher.git",
    "https://github.com/EntySec/RomBuster.git",
    "https://github.com/EntySec/HatSploit.git",
    "https://github.com/EntySec/Pwny.git",
    "https://github.com/EntySec/libload.git",
    "https://github.com/EntySec/HatAsm.git",
    "https://gitlab.com/exploit-database/exploitdb.git",
    "https://github.com/samyk/poisontap.git",
    "https://github.com/samyk/evercookie.git",
    "https://github.com/samyk/pwnat.git",
    "https://github.com/arthastang/IoT-Implant-Toolkit.git",
    "https://github.com/arthastang/IoT-Home-Guard.git",
    "https://github.com/samyk/magspoof.git",
    "https://github.com/samyk/slipstream.git",
    "https://github.com/samyk/skyjack.git",
    "https://github.com/coincoin7/Wireless-Router-Vulnerability.git",
    "https://github.com/arthastang/Router-Exploit-Shovel.git",
    "https://github.com/seclab-ucr/tcp_exploit.git",
    "https://github.com/seclab-ucr/SymTCP.git",
    "https://github.com/seclab-ucr/KOOBE.git",
    "https://github.com/seclab-ucr/CCS24Mesh.git",
    "https://github.com/acecilia/OpenWRTInvasion.git",
    "https://github.com/hkm/routerpwn.com.git",
    "https://github.com/j91321/rext.git",
    "https://github.com/foreni-packages/cisco-global-exploiter.git",
    "https://gitlab.com/exploit-database/exploitdb-bin-sploits.git",
    "https://github.com/johnoseni1/Router-hacker-Exploit-and-extract-user-and-password-.git",
    "https://github.com/649/Pingpon-Exploit.git",
    "https://github.com/MaherAzzouzi/ZTE-F660-Exploit.git",
    "https://github.com/stasinopoulos/ZTExploit.git",
    "https://github.com/oscommonjs/EXP_IOT.git",
    "https://github.com/ElberTavares/routers-exploit.git",
    "https://github.com/knqyf263/CVE-2020-10749.git",
    "https://github.com/G-bdennour/Huawei.git",
    "https://github.com/kthemis/RouterExploitScan.git",
    "https://github.com/ThomasRinsma/vmg8825scripts.git",
    "https://github.com/0vercl0k/zenith.git",
    "https://github.com/hook-s3c/CVE-2018-18852.git",
    "https://github.com/Zeyad-Azima/Huawei_Thief.git",
    "https://github.com/iridium/tapohax.git",
    "https://github.com/0xedh/mistrastar-mips-exploit.git",
    "https://github.com/tacnetsol/TRENDNetExploits.git",
    "https://github.com/0xyassine/poc-seeker.git",
    "https://github.com/JackDoan/TP-Link-ArcherC5-RCE.git",
    "https://github.com/afang5472/TP-Link-WDR-Router-Command-injection_POC.git",
    "https://github.com/dylvie/CVE-2020-35575-TP-LINK-TL-WR841ND-password-disclosure.git",
    "https://github.com/CyberVinner/TP-Link-TL-WR820N-CVE-2025-14175.git",
    "https://github.com/teteco/CVE-2025-67070-Intelbras-CFTV-MFA-Bypass.git",
    "https://github.com/tg12/PoC_CVEs.git",
]

CVE_POC_SOURCE = "https://labs.jamessawyer.co.uk/cves/"


def _gh_api_json(path: str) -> dict[str, Any]:
    """Call `gh api` and parse JSON."""

    proc = subprocess.run(
        ["gh", "api", path],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return json.loads(proc.stdout)


def _collect_github_search(query: str, max_total: int = 1000) -> list[dict[str, Any]]:
    """Paginate /search/repositories for a query (GitHub hard cap 1000)."""

    collected: list[dict[str, Any]] = []
    page = 1
    per_page = 100
    while len(collected) < max_total:
        q = urllib.parse.quote(query)
        path = f"/search/repositories?q={q}&per_page={per_page}&page={page}"
        data = _gh_api_json(path)
        items = data.get("items") or []
        if not items:
            break
        collected.extend(items)
        if len(items) < per_page:
            break
        page += 1
        if page > 10:
            break
    return collected[:max_total]


def _normalize_clone_url(url: str) -> str | None:
    """Return https clone URL or None."""

    u = url.strip().rstrip("/")
    if u.endswith(".git"):
        return u
    m = re.match(r"^https://github\.com/([^/]+)/([^/]+)/?$", u)
    if m:
        return f"https://github.com/{m.group(1)}/{m.group(2)}.git"
    m = re.match(r"^https://gitlab\.com/(.+)/([^/]+)/?$", u)
    if m:
        return f"https://gitlab.com/{m.group(1)}/{m.group(2)}.git"
    return None


def _repo_meta_from_item(item: dict[str, Any]) -> dict[str, Any]:
    return {
        "full_name": item.get("full_name"),
        "clone_url": item.get("clone_url") or item.get("html_url"),
        "html_url": item.get("html_url"),
        "fork": item.get("fork"),
        "archived": item.get("archived"),
        "default_branch": item.get("default_branch"),
        "pushed_at": item.get("pushed_at"),
        "stargazers_count": item.get("stargazers_count"),
        "language": item.get("language"),
        "license_spdx": (item.get("license") or {}).get("spdx_id"),
        "source": "github_search",
    }


@dataclass
class CatalogRecord:
    full_name: str | None
    clone_url: str
    host: str
    sources: list[str]
    fork: bool | None = None
    archived: bool | None = None
    rxforge_integration: str = "catalog_upstream_clone"
    notes: str = ""


def _dedupe_records(records: list[CatalogRecord]) -> list[CatalogRecord]:
    seen: dict[str, CatalogRecord] = {}
    for r in records:
        key = r.clone_url.rstrip("/").lower()
        if key not in seen:
            seen[key] = r
        else:
            seen[key].sources = sorted(set(seen[key].sources + r.sources))
    return list(seen.values())


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    by_url: dict[str, CatalogRecord] = {}

    for cu in SEED_CLONE_URLS:
        n = _normalize_clone_url(cu) or cu
        key = n.rstrip("/").lower()
        host = "gitlab" if "gitlab.com" in n else "github"
        fn = None
        if "github.com" in n:
            fn = n.replace("https://github.com/", "").replace(".git", "")
        by_url[key] = CatalogRecord(
            full_name=fn,
            clone_url=n,
            host=host,
            sources=["user_seed"],
            notes=f"CVE PoC index reference: {CVE_POC_SOURCE}",
        )

    for q in SEARCH_QUERIES:
        LOGGER.info("GitHub search query=%r", q)
        try:
            items = _collect_github_search(q)
        except subprocess.CalledProcessError as exc:
            LOGGER.error("gh api failed for query=%r: %s", q, exc)
            continue
        for it in items:
            meta = _repo_meta_from_item(it)
            cu = meta.get("clone_url")
            if not isinstance(cu, str):
                continue
            key = cu.rstrip("/").lower()
            rec = CatalogRecord(
                full_name=meta.get("full_name"),
                clone_url=cu,
                host="github",
                sources=[f"github_search:{q}"],
                fork=meta.get("fork"),
                archived=meta.get("archived"),
                notes="Auto-collected via GitHub Search API (subject to 1000 result cap per query).",
            )
            if key in by_url:
                by_url[key].sources = sorted(set(by_url[key].sources + rec.sources))
            else:
                by_url[key] = rec

    records = _dedupe_records(list(by_url.values()))
    records.sort(key=lambda r: (r.host, r.clone_url))

    payload = {
        "title": "Third-party router / edge / PoC upstream repositories (curated + search)",
        "generated_by": "tools/collect_third_party_router_repos.py",
        "cve_poc_index_urls": [CVE_POC_SOURCE],
        "disclaimer_pt": (
            "Uso apenas em escopo autorizado. Respeite licenças upstream. "
            "Repositórios grande (ex.: exploitdb) podem aumentar muito o clone do superprojeto."
        ),
        "disclaimer_en": (
            "Authorized use only. Respect upstream licenses. Large repos (e.g. exploitdb) "
            "significantly increase superproject clone size."
        ),
        "repositories": [asdict(r) for r in records],
        "counts": {"total": len(records)},
    }

    out_path = OUT_DIR / "third_party_router_exploit_repos.json"
    out_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    LOGGER.info("Wrote %s (%s repos)", out_path, len(records))
    return 0


if __name__ == "__main__":
    sys.exit(main())
