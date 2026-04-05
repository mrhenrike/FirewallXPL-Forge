#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Group GitHub catalog entries by upstream (parent) repository and suggest canonical URLs.

Uses ``gh api repos/{owner}/{repo}`` to read ``fork`` and ``parent.full_name``. Repos that share
the same canonical root (parent if fork, else self) can be deduplicated for clones — typically
keep the upstream or the fork with ``user_seed`` / highest star count.

Does not rewrite third_party_router_exploit_repos.json by default; emits a JSON report.

Author: André Henrique (@mrhenrike) | União Geek

"""

from __future__ import annotations

import argparse
import json
import logging
import subprocess
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

LOGGER = logging.getLogger(__name__)

RXFORGE_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CATALOG = RXFORGE_ROOT / "firewallxpl" / "resources" / "catalogs" / "third_party_router_exploit_repos.json"


def _gh_repo(owner: str, repo: str) -> dict[str, Any] | None:
    try:
        proc = subprocess.run(
            ["gh", "api", f"repos/{owner}/{repo}"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
    except subprocess.CalledProcessError as exc:
        LOGGER.warning("gh api failed %s/%s: %s", owner, repo, exc.stderr[:200] if exc.stderr else exc)
        return None
    except FileNotFoundError:
        LOGGER.error("gh CLI not found")
        return None
    return json.loads(proc.stdout) if proc.stdout.strip() else None


def _split_from_clone(clone_url: str) -> tuple[str, str] | None:
    u = clone_url.strip().rstrip("/")
    for prefix in ("https://github.com/", "http://github.com/"):
        if u.startswith(prefix):
            tail = u[len(prefix) :].removesuffix(".git")
            if "/" in tail:
                o, r = tail.split("/", 1)
                return o, r
    return None


def _canonical_root(meta: dict[str, Any]) -> str:
    if meta.get("fork") and isinstance(meta.get("parent"), dict):
        p = meta["parent"].get("full_name")
        if isinstance(p, str) and p:
            return p
    fn = meta.get("full_name")
    return str(fn) if fn else ""


def main() -> int:
    parser = argparse.ArgumentParser(description="Report GitHub fork dedupe groups for PoC catalog.")
    parser.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG)
    parser.add_argument("--out", type=Path, default=None, help="JSON report path (default: stdout only)")
    parser.add_argument("--max-repos", type=int, default=0, help="Cap API calls (0 = all GitHub entries).")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

    data = json.loads(args.catalog.read_text(encoding="utf-8"))
    repos = data.get("repositories") or []

    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    errors: list[dict[str, str]] = []
    n = 0
    for entry in repos:
        if entry.get("host") != "github":
            continue
        cu = entry.get("clone_url")
        if not isinstance(cu, str):
            continue
        pr = _split_from_clone(cu)
        if not pr:
            continue
        if args.max_repos and n >= args.max_repos:
            errors.append({"clone_url": cu, "error": "max-repos cap"})
            continue
        n += 1
        owner, repo = pr
        meta = _gh_repo(owner, repo)
        if not meta:
            errors.append({"clone_url": cu, "error": "metadata_unavailable"})
            continue
        root = _canonical_root(meta)
        if not root:
            errors.append({"clone_url": cu, "error": "no_canonical"})
            continue
        groups[root].append(
            {
                "full_name": meta.get("full_name"),
                "clone_url": meta.get("clone_url") or cu,
                "fork": meta.get("fork"),
                "stargazers_count": meta.get("stargazers_count"),
                "catalog_sources": entry.get("sources"),
            }
        )

    # Suggested keeper: max stars, tie-break non-fork
    suggestions: list[dict[str, Any]] = []
    for root, members in sorted(groups.items(), key=lambda x: x[0]):
        if len(members) < 2:
            continue
        sorted_m = sorted(
            members,
            key=lambda m: (
                -(m.get("stargazers_count") or 0),
                1 if m.get("fork") else 0,
                str(m.get("clone_url")),
            ),
        )
        suggestions.append(
            {
                "canonical_root": root,
                "keeper": sorted_m[0],
                "alternate_clone_urls": [m["clone_url"] for m in sorted_m[1:]],
            }
        )

    report = {
        "generated_by": "tools/dedupe_github_fork_canonicals.py",
        "catalog": str(args.catalog.resolve()),
        "github_api_lookups": n,
        "fork_groups_multi_clone": len(suggestions),
        "groups": suggestions,
        "errors_sample": errors[:50],
        "error_count": len(errors),
    }

    text = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text, encoding="utf-8")
        LOGGER.info("Wrote %s", args.out)
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
