"""NSE script installer for FirewallXPL-Forge.

Detects nmap installation on the host OS, locates the NSE scripts directory, and
deploys the bundled firewall-specific .nse scripts. Falls back gracefully when nmap
is not installed, printing the destination path so the user can copy files manually.

Supported platforms: Linux, macOS, Windows.

Author: André Henrique (@mrhenrike) | União Geek — https://github.com/Uniao-Geek
"""

from __future__ import annotations

import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path
from typing import List, Optional, Tuple

# ---------------------------------------------------------------------------
# Bundled NSE scripts location (inside the installed package)
# ---------------------------------------------------------------------------

_PACKAGE_NSE_DIR: Path = Path(__file__).resolve().parent.parent / "resources" / "arsenal" / "nse"

# ---------------------------------------------------------------------------
# Known nmap script directory defaults per platform
# ---------------------------------------------------------------------------

_LINUX_MACOS_PATHS: List[str] = [
    "/usr/share/nmap/scripts",
    "/usr/local/share/nmap/scripts",
    "/opt/homebrew/share/nmap/scripts",
    "/opt/local/share/nmap/scripts",
]

_WINDOWS_PATHS: List[str] = [
    r"C:\Program Files (x86)\Nmap\scripts",
    r"C:\Program Files\Nmap\scripts",
    r"C:\Nmap\scripts",
]


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _find_nmap_binary() -> Optional[str]:
    """Return the absolute path to the nmap binary, or None if not found."""
    return shutil.which("nmap")


def _nmap_version(nmap_bin: str) -> str:
    """Return nmap version string, e.g. '7.95'."""
    try:
        result = subprocess.run(
            [nmap_bin, "--version"],
            capture_output=True, text=True, timeout=10,
        )
        first_line = result.stdout.splitlines()[0] if result.stdout else ""
        parts = first_line.split()
        if len(parts) >= 3:
            return parts[2]
        return first_line
    except Exception:
        return "unknown"


def _nmap_scripts_dir(nmap_bin: str) -> Optional[Path]:
    """Locate the nmap scripts directory.

    First tries `nmap --datadir`, then falls back to known platform defaults.
    """
    # Try --datadir
    try:
        result = subprocess.run(
            [nmap_bin, "--datadir"],
            capture_output=True, text=True, timeout=10,
        )
        output = result.stdout.strip() or result.stderr.strip()
        for line in output.splitlines():
            candidate = Path(line.strip()) / "scripts"
            if candidate.is_dir():
                return candidate
    except Exception:
        pass

    # Platform defaults
    system = platform.system().lower()
    candidates = _WINDOWS_PATHS if system == "windows" else _LINUX_MACOS_PATHS

    for path_str in candidates:
        candidate = Path(path_str)
        if candidate.is_dir():
            return candidate

    # Last resort: locate any .nse on the filesystem (Linux/macOS only)
    if system != "windows":
        try:
            result = subprocess.run(
                ["locate", "-l", "1", "*.nse"],
                capture_output=True, text=True, timeout=15,
            )
            if result.stdout.strip():
                return Path(result.stdout.strip()).parent
        except Exception:
            pass

    return None


def _find_nse_dir_without_nmap() -> Optional[Path]:
    """Best-effort attempt to find the nmap scripts folder even without nmap in PATH.

    Searches known locations. Returns the first existing one or None.
    """
    system = platform.system().lower()
    candidates = _WINDOWS_PATHS if system == "windows" else _LINUX_MACOS_PATHS
    for path_str in candidates:
        p = Path(path_str)
        if p.is_dir():
            return p
    return None


def _bundled_nse_scripts() -> List[Path]:
    """Return sorted list of .nse files bundled with FirewallXPL-Forge."""
    if not _PACKAGE_NSE_DIR.is_dir():
        return []
    return sorted(_PACKAGE_NSE_DIR.glob("*.nse"))


def _run_script_updatedb(nmap_bin: str) -> bool:
    """Run `nmap --script-updatedb` and return True if it succeeded."""
    try:
        result = subprocess.run(
            [nmap_bin, "--script-updatedb"],
            capture_output=True, text=True, timeout=60,
        )
        return result.returncode == 0
    except Exception:
        return False


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

class NseInstallResult:
    """Holds the outcome of an install_nse_scripts() call."""

    def __init__(self) -> None:
        self.nmap_found: bool = False
        self.nmap_binary: Optional[str] = None
        self.nmap_version: str = ""
        self.scripts_dir: Optional[Path] = None
        self.installed: List[str] = []
        self.skipped: List[str] = []
        self.errors: List[Tuple[str, str]] = []
        self.updatedb_ok: Optional[bool] = None
        self.bundled_scripts: List[Path] = []
        self.destination_hint: str = ""

    @property
    def success(self) -> bool:
        return self.nmap_found and bool(self.installed) and not self.errors

    @property
    def partial(self) -> bool:
        return bool(self.installed) and bool(self.errors)


def install_nse_scripts(
    custom_path: Optional[str] = None,
    force: bool = False,
    dry_run: bool = False,
) -> NseInstallResult:
    """Detect nmap, locate the NSE scripts directory, and install bundled .nse files.

    Args:
        custom_path: Override the auto-detected NSE scripts directory.
        force: Overwrite existing scripts even if they already exist.
        dry_run: Print what would happen without copying any file.

    Returns:
        NseInstallResult with detailed outcome fields.
    """
    result = NseInstallResult()
    result.bundled_scripts = _bundled_nse_scripts()

    # ------------------------------------------------------------------
    # Step 1: Locate nmap
    # ------------------------------------------------------------------
    nmap_bin = _find_nmap_binary()
    result.nmap_found = nmap_bin is not None
    result.nmap_binary = nmap_bin

    if nmap_bin:
        result.nmap_version = _nmap_version(nmap_bin)

    # ------------------------------------------------------------------
    # Step 2: Locate (or accept custom) scripts directory
    # ------------------------------------------------------------------
    if custom_path:
        scripts_dir = Path(custom_path)
    elif nmap_bin:
        scripts_dir = _nmap_scripts_dir(nmap_bin)
    else:
        scripts_dir = _find_nse_dir_without_nmap()

    result.scripts_dir = scripts_dir

    if scripts_dir is None:
        # Provide a sensible default hint for the user
        system = platform.system().lower()
        if system == "windows":
            result.destination_hint = r"C:\Program Files (x86)\Nmap\scripts"
        else:
            result.destination_hint = "/usr/share/nmap/scripts"
    else:
        result.destination_hint = str(scripts_dir)

    # ------------------------------------------------------------------
    # Step 3: Install files
    # ------------------------------------------------------------------
    if not result.bundled_scripts:
        return result

    if scripts_dir is None or not result.nmap_found:
        # Cannot install; surface info so user can install manually
        return result

    if dry_run:
        result.installed = [s.name for s in result.bundled_scripts]
        return result

    for nse_path in result.bundled_scripts:
        dest = scripts_dir / nse_path.name
        if dest.exists() and not force:
            result.skipped.append(nse_path.name)
            continue
        try:
            shutil.copy2(nse_path, dest)
            result.installed.append(nse_path.name)
        except PermissionError as exc:
            result.errors.append((nse_path.name, "Permission denied — try with sudo/RunAs: {}".format(exc)))
        except OSError as exc:
            result.errors.append((nse_path.name, str(exc)))

    # ------------------------------------------------------------------
    # Step 4: Update nmap script database
    # ------------------------------------------------------------------
    if result.installed and nmap_bin:
        result.updatedb_ok = _run_script_updatedb(nmap_bin)

    return result


def print_install_report(result: NseInstallResult, verbose: bool = False) -> None:
    """Print a human-readable install report to stdout.

    Designed to be called from both the interactive CLI and non-interactive mode.
    Uses plain print() so it works without the Printer thread.
    """
    GREEN = "\033[32m" if sys.stdout.isatty() else ""
    RED   = "\033[31m" if sys.stdout.isatty() else ""
    YELLOW = "\033[33m" if sys.stdout.isatty() else ""
    CYAN  = "\033[36m" if sys.stdout.isatty() else ""
    RESET = "\033[0m" if sys.stdout.isatty() else ""

    print()
    # Nmap detection
    if result.nmap_found:
        print("{}[+]{} nmap found: {} ({})".format(GREEN, RESET, result.nmap_binary, result.nmap_version))
    else:
        print("{}[-]{} nmap not found in PATH. Install nmap first:".format(RED, RESET))
        print("     Linux/Debian:  sudo apt-get install nmap")
        print("     Linux/RHEL:    sudo yum install nmap")
        print("     macOS:         brew install nmap")
        print("     Windows:       https://nmap.org/download.html")

    # Bundled scripts
    if result.bundled_scripts:
        print("{}[*]{} Bundled NSE scripts: {}".format(CYAN, RESET, len(result.bundled_scripts)))
        if verbose:
            for s in result.bundled_scripts:
                print("     {}".format(s.name))
    else:
        print("{}[!]{} No bundled NSE scripts found in package.".format(YELLOW, RESET))
        print("     Expected path: {}".format(_PACKAGE_NSE_DIR))
        return

    # Scripts directory
    if result.scripts_dir:
        print("{}[*]{} NSE scripts directory: {}".format(CYAN, RESET, result.scripts_dir))
    else:
        print("{}[!]{} NSE scripts directory not found automatically.".format(YELLOW, RESET))
        print("     Use: install-nse --path <directory>")
        print("     Or copy manually to: {}".format(result.destination_hint))

    # Not installed (no nmap or no scripts dir)
    if not result.nmap_found or result.scripts_dir is None:
        print()
        print("{}[*]{} Bundled scripts are available at:".format(CYAN, RESET))
        print("     {}".format(_PACKAGE_NSE_DIR))
        print("     Copy .nse files manually to your nmap scripts directory when ready.")
        return

    # Installation results
    for name in result.installed:
        print("{}[+]{} Installed: {}".format(GREEN, RESET, name))
    for name in result.skipped:
        print("{}[~]{} Skipped (already exists): {} — use --force to overwrite".format(YELLOW, RESET, name))
    for name, err in result.errors:
        print("{}[-]{} Error installing {}: {}".format(RED, RESET, name, err))

    # nmap --script-updatedb
    if result.updatedb_ok is True:
        print("{}[+]{} nmap --script-updatedb completed.".format(GREEN, RESET))
    elif result.updatedb_ok is False:
        print("{}[!]{} nmap --script-updatedb failed. Run manually: nmap --script-updatedb".format(YELLOW, RESET))

    # Summary
    if result.success:
        print()
        print("{}[+]{} All scripts installed. Use them with:".format(GREEN, RESET))
        print("     nmap --script fxf-globalprotect-detect <target>")
        print("     nmap --script fxf-firewall-fingerprint -p 443,80 <target>")
    elif result.partial:
        print()
        print("{}[!]{} Partial install — {} installed, {} errors.".format(YELLOW, RESET, len(result.installed), len(result.errors)))
    elif result.skipped and not result.installed:
        print()
        print("{}[~]{} All scripts already installed. Use --force to overwrite.".format(YELLOW, RESET))
    print()
