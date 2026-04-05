#!/usr/bin/env python3
"""Run scoped test suite excluding out-of-scope domains."""

from __future__ import annotations

# Author: André Henrique (@mrhenrike) | União Geek — https://github.com/Uniao-Geek

import subprocess
import sys
from pathlib import Path
from typing import List


def main() -> int:
    """Execute a focused pytest suite for in-scope domains."""
    repo_root = Path(__file__).resolve().parents[1]
    tests_root = repo_root / "tests"

    if not tests_root.exists():
        print("tests directory not found; skipping scoped tests")
        return 0

    cmd: List[str] = [
        sys.executable,
        "-m",
        "pytest",
        "-q",
        "tests/core/test_option.py",
        "--maxfail=1",
        "--disable-warnings",
        "--confcutdir=tests/core",
    ]
    completed = subprocess.run(cmd, cwd=str(repo_root))
    return int(completed.returncode)


if __name__ == "__main__":
    raise SystemExit(main())
