#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Register Git submodules in the superproject from third_party_router_exploit_repos.json.

By default only entries whose `sources` include ``user_seed`` are added (explicit curator list).

Paths: ``submodules/IoT/third-party-router-poc/<owner>__<repo>`` (GitLab uses owner path segments).

Run from the *superproject root* (Projetos-SafeLabs), for example::

    python submodules/IoT/RouterXPL-Forge/tools/add_git_submodules_from_catalog.py --dry-run
    python submodules/IoT/RouterXPL-Forge/tools/add_git_submodules_from_catalog.py

Author: André Henrique (@mrhenrike) | União Geek

"""

from __future__ import annotations

import argparse
import json
import logging
import re
import subprocess
import sys
from pathlib import Path

LOGGER = logging.getLogger(__name__)

RXFORGE_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CATALOG = RXFORGE_ROOT / "firewallxpl" / "resources" / "catalogs" / "third_party_router_exploit_repos.json"


def _slug_from_clone_url(clone_url: str) -> str:
    u = clone_url.strip().rstrip("/").removesuffix(".git")
    if "github.com/" in u:
        tail = u.split("github.com/", 1)[1]
        return tail.replace("/", "__")
    if "gitlab.com/" in u:
        tail = u.split("gitlab.com/", 1)[1]
        return tail.replace("/", "__")
    h = re.sub(r"[^a-zA-Z0-9._-]+", "_", u)[:120]
    return h or "repo"


def _gitmodules_has_url(gitmodules_text: str, url: str) -> bool:
    """True only if a submodule ``url =`` line exactly matches (avoids exploitdb vs exploitdb-bin)."""

    want = {url, url.removesuffix(".git"), f"{url}/", f"{url.removesuffix('.git')}/"}
    for line in gitmodules_text.splitlines():
        s = line.strip()
        if not s.startswith("url = "):
            continue
        val = s.removeprefix("url = ").strip().strip('"').strip("'")
        if val in want:
            return True
    return False


def _run_git(args: list[str], cwd: Path, dry_run: bool) -> None:
    if dry_run:
        LOGGER.info("DRY-RUN: git %s (cwd=%s)", " ".join(args), cwd)
        return
    subprocess.run(["git", *args], cwd=cwd, check=True)


def main() -> int:
    parser = argparse.ArgumentParser(description="Add submodules from third_party catalog.")
    parser.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG)
    parser.add_argument(
        "--superproject-root",
        type=Path,
        default=None,
        help="Root of Projetos-SafeLabs (default: parent of submodules/)",
    )
    parser.add_argument(
        "--source",
        action="append",
        default=["user_seed"],
        help="Only add repos whose sources contains this tag (repeatable). Default: user_seed",
    )
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

    root = args.superproject_root
    if root is None:
        root = Path(__file__).resolve().parents[4]
        if (root / "submodules").is_dir():
            pass
        else:
            root = Path.cwd()

    gitmodules = root / ".gitmodules"
    existing = gitmodules.read_text(encoding="utf-8", errors="replace") if gitmodules.is_file() else ""

    data = json.loads(args.catalog.read_text(encoding="utf-8"))
    repos = data.get("repositories") or []
    required = set(args.source)
    added = 0
    skipped = 0
    for entry in repos:
        sources = set(entry.get("sources") or [])
        if not (sources & required):
            continue
        cu = entry.get("clone_url")
        if not isinstance(cu, str) or not cu.startswith("http"):
            LOGGER.warning("Skip entry without clone_url: %s", entry.get("full_name"))
            skipped += 1
            continue
        if _gitmodules_has_url(existing, cu):
            LOGGER.info("Already in .gitmodules: %s", cu)
            skipped += 1
            continue
        rel = Path("submodules") / "IoT" / "third-party-router-poc" / _slug_from_clone_url(cu)
        sm_name = rel.as_posix()
        target = root / rel
        if target.exists():
            LOGGER.warning("Path already exists on disk, skip: %s", target)
            skipped += 1
            continue
        LOGGER.info("Adding submodule %s -> %s", sm_name, cu)
        try:
            _run_git(
                ["submodule", "add", "-f", "--name", sm_name, cu, sm_name],
                cwd=root,
                dry_run=args.dry_run,
            )
        except subprocess.CalledProcessError as exc:
            LOGGER.error("git submodule add failed for %s: %s", cu, exc)
            skipped += 1
            continue
        if not args.dry_run:
            existing = (root / ".gitmodules").read_text(encoding="utf-8", errors="replace")
        added += 1

    LOGGER.info("Done. added=%s skipped=%s", added, skipped)
    return 0


if __name__ == "__main__":
    sys.exit(main())
