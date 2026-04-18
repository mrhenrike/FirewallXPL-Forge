#!/usr/bin/env python3
# Author: André Henrique (@mrhenrike) | União Geek — https://github.com/Uniao-Geek

import logging.handlers
import platform
import sys

# ──────────────────────────────────────────────────────────────────────────────
#  MIGRATION NOTICE (v2.1.0)
#  FirewallXPL-Forge has been merged into EmbedXPL-Forge.
#  All 81 modules (Fortinet, Cisco, Palo Alto, SonicWall, Sophos, Juniper,
#  F5, Citrix, Barracuda, A10/Imperva, NAC, pfSense, OT perimeter) are now
#  available under `embedxpl/modules/exploits/firewalls/` and related paths.
#
#  ➜  Migrate:  pip install embedxpl
#  ➜  New CLI:  exf  (or fxf — alias registered by embedxpl)
#  ➜  Docs:     https://github.com/mrhenrike/EmbedXPL-Forge
#
#  FirewallXPL-Forge v2.1.0 continues to work but will not receive new modules.
# ──────────────────────────────────────────────────────────────────────────────

_MIGRATION_BANNER = """
\033[33m╔══════════════════════════════════════════════════════════════════════╗
║  ⚠  FirewallXPL-Forge has been merged into EmbedXPL-Forge            ║
║                                                                      ║
║  All 81 modules are now available in EmbedXPL-Forge v2.0+            ║
║                                                                      ║
║  Migrate:  pip install embedxpl                                      ║
║  New CLI:  exf  (or  fxf  — alias registered by embedxpl)            ║
║  Repo:     https://github.com/mrhenrike/EmbedXPL-Forge               ║
║                                                                      ║
║  FirewallXPL v2.1.0 is the final standalone release.                ║
╚══════════════════════════════════════════════════════════════════════╝\033[0m
"""
print(_MIGRATION_BANNER, file=sys.stderr)

if sys.version_info.major < 3:
    print("FirewallXPL supports only Python3. Rerun application in Python3 environment.")
    exit(1)
if sys.version_info < (3, 8):
    print("FirewallXPL requires Python 3.8+ (detected: {}).".format(platform.python_version()))
    exit(1)

log_handler = logging.handlers.RotatingFileHandler(filename="firewallxpl.log", maxBytes=500000)
log_formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s       %(message)s")
log_handler.setFormatter(log_formatter)
LOGGER = logging.getLogger()
LOGGER.setLevel(logging.DEBUG)
LOGGER.addHandler(log_handler)


def firewallxpl(argv):
    try:
        from firewallxpl.interpreter import FirewallXPLInterpreter
    except ModuleNotFoundError as err:
        print("FirewallXPL bootstrap error: missing Python dependency: {}".format(err))
        print("Run: python -m pip install -r requirements.txt")
        print("Optional diagnostics: python tools/env_doctor.py")
        raise SystemExit(1)

    rxf = FirewallXPLInterpreter()
    if len(argv[1:]):
        rxf.nonInteractive(argv)
    else:
        rxf.start()

if __name__ == "__main__":
    try:
        firewallxpl(sys.argv)
    except (KeyboardInterrupt, SystemExit):
        pass
