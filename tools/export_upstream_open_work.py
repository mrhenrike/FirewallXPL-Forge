#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Export open issues and open pull requests for GitHub repos listed in a JSON catalog.

Issue comments are fetched for open issues only, capped per repository to stay within
reasonable API volume (override with --max-issue-comments-per-repo).

With ``--fetch-pr-review-details``, also pulls PR reviews, inline review comments, and
PR conversation comments (caps with ``--max-open-prs-for-review-details``).

GitLab projects are skipped unless GL_TOKEN + project id mapping is added later.

Author: André Henrique (@mrhenrike) | União Geek

"""

from __future__ import annotations

import argparse
import json
import logging
import subprocess
import sys
from pathlib import Path
from typing import Any

LOGGER = logging.getLogger(__name__)

RXFORGE_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CATALOG = RXFORGE_ROOT / "firewallxpl" / "resources" / "catalogs" / "third_party_router_exploit_repos.json"
OUT_PATH = RXFORGE_ROOT / "firewallxpl" / "resources" / "catalogs" / "third_party_upstream_open_work.json"


def _gh_api(path: str) -> Any:
    proc = subprocess.run(
        ["gh", "api", path],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return json.loads(proc.stdout) if proc.stdout.strip() else None


def _list_open_issues(owner: str, repo: str, per_page: int = 100) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    page = 1
    while True:
        path = (
            f"/repos/{owner}/{repo}/issues?state=open&per_page={per_page}&page={page}"
        )
        batch = _gh_api(path)
        if not isinstance(batch, list) or not batch:
            break
        # Exclude pull requests (they appear in issues API)
        for it in batch:
            if "pull_request" in it:
                continue
            out.append(it)
        if len(batch) < per_page:
            break
        page += 1
        if page > 20:
            break
    return out


def _list_open_pulls(owner: str, repo: str, per_page: int = 100) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    page = 1
    while True:
        path = f"/repos/{owner}/{repo}/pulls?state=open&per_page={per_page}&page={page}"
        batch = _gh_api(path)
        if not isinstance(batch, list) or not batch:
            break
        out.extend(batch)
        if len(batch) < per_page:
            break
        page += 1
        if page > 20:
            break
    return out


def _pull_reviews(owner: str, repo: str, pull_number: int) -> list[dict[str, Any]]:
    """Submitted PR reviews (APPROVED / CHANGES_REQUESTED / COMMENTED)."""

    out: list[dict[str, Any]] = []
    page = 1
    while True:
        path = f"/repos/{owner}/{repo}/pulls/{pull_number}/reviews?per_page=100&page={page}"
        data = _gh_api(path)
        if not isinstance(data, list) or not data:
            break
        out.extend(data)
        if len(data) < 100:
            break
        page += 1
        if page > 20:
            break
    return out


def _pull_review_comments(owner: str, repo: str, pull_number: int) -> list[dict[str, Any]]:
    """Inline review comments on PR diffs."""

    out: list[dict[str, Any]] = []
    page = 1
    while True:
        path = f"/repos/{owner}/{repo}/pulls/{pull_number}/comments?per_page=100&page={page}"
        data = _gh_api(path)
        if not isinstance(data, list) or not data:
            break
        out.extend(data)
        if len(data) < 100:
            break
        page += 1
        if page > 20:
            break
    return out


def _pull_issue_thread_comments(owner: str, repo: str, pull_number: int) -> list[dict[str, Any]]:
    """Conversation comments on the PR (issue comments API)."""

    return _issue_comments(owner, repo, pull_number)


def _issue_comments(owner: str, repo: str, issue_number: int) -> list[dict[str, Any]]:
    """All comments for an issue (paginated)."""

    out: list[dict[str, Any]] = []
    page = 1
    while True:
        path = (
            f"/repos/{owner}/{repo}/issues/{issue_number}/comments"
            f"?per_page=100&page={page}"
        )
        data = _gh_api(path)
        if not isinstance(data, list) or not data:
            break
        out.extend(data)
        if len(data) < 100:
            break
        page += 1
        if page > 50:
            break
    return out


def _split_github_repo(full_name: str) -> tuple[str, str] | None:
    if "/" not in full_name:
        return None
    owner, repo = full_name.split("/", 1)
    if not owner or not repo:
        return None
    return owner, repo


def main() -> int:
    parser = argparse.ArgumentParser(description="Export open GitHub issues/PRs for catalog repos.")
    parser.add_argument(
        "--catalog",
        type=Path,
        default=DEFAULT_CATALOG,
        help="Path to third_party_router_exploit_repos.json",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=OUT_PATH,
        help="Output JSON path",
    )
    parser.add_argument(
        "--source",
        action="append",
        default=None,
        help="Only repos whose sources contains this tag (e.g. user_seed). Default: all GitHub entries.",
    )
    parser.add_argument(
        "--max-github-repos",
        type=int,
        default=0,
        help="Limit number of GitHub repos processed (0 = all).",
    )
    parser.add_argument(
        "--max-open-issues-for-comments",
        type=int,
        default=0,
        help="Max open issues to fetch full comments for (0 = all open issues).",
    )
    parser.add_argument(
        "--fetch-pr-review-details",
        action="store_true",
        help="Fetch PR reviews, inline review comments, and PR conversation comments (extra API calls).",
    )
    parser.add_argument(
        "--max-open-prs-for-review-details",
        type=int,
        default=25,
        help="Cap PRs per repo when --fetch-pr-review-details is set.",
    )
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

    raw = json.loads(args.catalog.read_text(encoding="utf-8"))
    repos = raw.get("repositories") or []
    source_filter = set(args.source) if args.source else None
    results: list[dict[str, Any]] = []
    gh_count = 0
    for entry in repos:
        if source_filter is not None:
            if not (set(entry.get("sources") or []) & source_filter):
                continue
        host = entry.get("host")
        if host != "github":
            results.append(
                {
                    "clone_url": entry.get("clone_url"),
                    "host": host,
                    "skipped": "non-github (use GitLab API separately)",
                }
            )
            continue
        fn = entry.get("full_name")
        if not fn:
            cu = entry.get("clone_url") or ""
            fn = cu.replace("https://github.com/", "").replace(".git", "").strip("/")
        parsed = _split_github_repo(str(fn))
        if not parsed:
            results.append({"clone_url": entry.get("clone_url"), "error": "unparseable full_name"})
            continue
        owner, repo = parsed
        if args.max_github_repos and gh_count >= args.max_github_repos:
            results.append(
                {
                    "full_name": f"{owner}/{repo}",
                    "skipped": "max-github-repos limit",
                }
            )
            continue
        gh_count += 1
        LOGGER.info("Fetching %s/%s", owner, repo)
        try:
            issues = _list_open_issues(owner, repo)
            pulls = _list_open_pulls(owner, repo)
        except subprocess.CalledProcessError as exc:
            results.append({"full_name": f"{owner}/{repo}", "error": str(exc)})
            continue
        issue_cap = args.max_open_issues_for_comments
        issues_for_comments = issues if issue_cap <= 0 else issues[:issue_cap]
        issue_payloads: list[dict[str, Any]] = []
        for it in issues_for_comments:
            num = it.get("number")
            comments: list[dict[str, Any]] = []
            if isinstance(num, int):
                try:
                    comments = _issue_comments(owner, repo, num)
                except subprocess.CalledProcessError:
                    comments = []
            issue_payloads.append(
                {
                    "number": num,
                    "title": it.get("title"),
                    "html_url": it.get("html_url"),
                    "user": (it.get("user") or {}).get("login"),
                    "comments_total": it.get("comments"),
                    "body_preview": (it.get("body") or "")[:400],
                    "comments": [
                        {
                            "user": (c.get("user") or {}).get("login"),
                            "html_url": c.get("html_url"),
                            "body_preview": (c.get("body") or "")[:400],
                        }
                        for c in comments
                    ],
                }
            )
        pull_cap = args.max_open_prs_for_review_details if args.fetch_pr_review_details else 0
        pull_payloads: list[dict[str, Any]] = []
        for idx, pr in enumerate(pulls):
            num = pr.get("number")
            base_pr = {
                "number": num,
                "title": pr.get("title"),
                "html_url": pr.get("html_url"),
                "user": (pr.get("user") or {}).get("login"),
                "draft": pr.get("draft"),
                "body_preview": (pr.get("body") or "")[:400],
            }
            if (
                args.fetch_pr_review_details
                and isinstance(num, int)
                and (pull_cap <= 0 or idx < pull_cap)
            ):
                try:
                    reviews = _pull_reviews(owner, repo, num)
                    rev_comments = _pull_review_comments(owner, repo, num)
                    pr_comments = _pull_issue_thread_comments(owner, repo, num)
                except subprocess.CalledProcessError:
                    reviews, rev_comments, pr_comments = [], [], []
                base_pr["reviews"] = [
                    {
                        "id": rv.get("id"),
                        "state": rv.get("state"),
                        "user": (rv.get("user") or {}).get("login"),
                        "body_preview": (rv.get("body") or "")[:400],
                        "html_url": rv.get("html_url"),
                    }
                    for rv in reviews
                ]
                base_pr["review_inline_comments"] = [
                    {
                        "id": c.get("id"),
                        "user": (c.get("user") or {}).get("login"),
                        "path": c.get("path"),
                        "body_preview": (c.get("body") or "")[:400],
                        "html_url": c.get("html_url"),
                    }
                    for c in rev_comments
                ]
                base_pr["pr_conversation_comments"] = [
                    {
                        "user": (c.get("user") or {}).get("login"),
                        "body_preview": (c.get("body") or "")[:400],
                        "html_url": c.get("html_url"),
                    }
                    for c in pr_comments
                ]
            pull_payloads.append(base_pr)
        results.append(
            {
                "full_name": f"{owner}/{repo}",
                "open_issues_count": len(issues),
                "open_pulls_count": len(pulls),
                "open_issues_sample_with_comments": issue_payloads,
                "open_pull_requests": pull_payloads,
                "github_ui": f"https://github.com/{owner}/{repo}/issues",
            }
        )

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        json.dumps({"repositories": results}, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    LOGGER.info("Wrote %s", args.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
