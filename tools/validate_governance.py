#!/usr/bin/env python3
"""Validate governance baseline files and GitHub templates."""

from __future__ import annotations

# Author: André Henrique (@mrhenrike) | União Geek — https://github.com/Uniao-Geek

import logging
from pathlib import Path
from typing import List


LOGGER = logging.getLogger("validate_governance")


def _configure_logging() -> None:
    """Configure logger for governance checks."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )


def _must_contain(path: Path, required_tokens: List[str], errors: List[str]) -> None:
    """Validate a file exists and contains required tokens."""
    if not path.exists():
        errors.append("missing required governance file: {}".format(path.as_posix()))
        return
    content = path.read_text(encoding="utf-8", errors="ignore")
    if not content.strip():
        errors.append("governance file is empty: {}".format(path.as_posix()))
        return
    lower = content.lower()
    for token in required_tokens:
        if token.lower() not in lower:
            errors.append("missing token '{}' in {}".format(token, path.as_posix()))


def main() -> int:
    """Run governance baseline validation."""
    _configure_logging()
    repo_root = Path(__file__).resolve().parents[1]
    errors: List[str] = []

    _must_contain(
        repo_root / "LICENSE",
        ["redistribution and use", "as is"],
        errors,
    )
    _must_contain(
        repo_root / "CODE_OF_CONDUCT.md",
        ["expected behavior", "unacceptable behavior", "reporting"],
        errors,
    )
    _must_contain(
        repo_root / "SECURITY.md",
        ["reporting a vulnerability", "safe testing rules", "coordinated disclosure"],
        errors,
    )
    _must_contain(
        repo_root / "CONTRIBUTING.md",
        ["scope", "validation expectations", "security and conduct"],
        errors,
    )
    _must_contain(
        repo_root / ".github" / "ISSUE_TEMPLATE.md",
        ["issue type", "scope check", "steps to reproduce"],
        errors,
    )
    _must_contain(
        repo_root / ".github" / "PULL_REQUEST_TEMPLATE.md",
        ["status", "scope", "required local checks", "risk notes"],
        errors,
    )
    _must_contain(
        repo_root / ".github" / "ISSUE_TEMPLATE" / "config.yml",
        ["blank_issues_enabled", "contact_links"],
        errors,
    )

    if errors:
        for error in errors:
            LOGGER.error(error)
        return 1

    LOGGER.info("Governance validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
