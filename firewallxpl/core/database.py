"""FirewallXPL Operational Database.

Extends EmbedXPL XplDatabase base for FirewallXPL-specific usage.
Stored at ~/.firewallxpl/fxf.db

Usage::

    from firewallxpl.core.database import FxfDatabase

    db = FxfDatabase()
    db.workspace("pentest-x")
    db.add_host("192.168.1.1")
    db.add_vuln("192.168.1.1", module_path="firewallxpl...", cve_ids=["CVE-..."])
    db.add_cred("192.168.1.1", "admin", "admin")
    db.stats()

Author: Andre Henrique (@mrhenrike) | Uniao Geek
# authorized use only
"""
from __future__ import annotations

from pathlib import Path

# XplDatabase base from EmbedXPL (shared infrastructure)
try:
    from embedxpl.core.database import XplDatabase
except ImportError:
    # Fallback: re-implement minimal base if EmbedXPL not installed
    import sys
    _SUITE = Path(__file__).resolve().parents[5]
    if str(_SUITE / "EmbedXPL-Forge") not in sys.path:
        sys.path.insert(0, str(_SUITE / "EmbedXPL-Forge"))
    from embedxpl.core.database import XplDatabase


class FxfDatabase(XplDatabase):
    """FirewallXPL operational database stored at ~/.firewallxpl/fxf.db.

    Domain: NGFW, UTM, IDS, IPS, NAC, VPN, WAF, LB
    """

    _DB_DIR  = Path.home() / ".firewallxpl"
    _DB_FILE = "fxf.db"
    _TOOL    = "FirewallXPL"
