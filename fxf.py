#!/usr/bin/env python3
# Author: André Henrique (@mrhenrike) | União Geek — https://github.com/Uniao-Geek

import logging.handlers
import platform
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

if sys.version_info < (3, 8):
    print("FirewallXPL requires Python 3.8+ (detected: {}).".format(platform.python_version()))
    exit(1)

_MIGRATION_BANNER = """
\033[33m╔══════════════════════════════════════════════════════════════════════╗
║  FirewallXPL-Forge merged into EmbedXPL-Forge (exf)                  ║
║  Migrate: pip install embedxpl                                       ║
╚══════════════════════════════════════════════════════════════════════╝\033[0m
"""
print(_MIGRATION_BANNER, file=sys.stderr)

log_handler = logging.handlers.RotatingFileHandler(filename="firewallxpl.log", maxBytes=500000)
log_formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s       %(message)s")
log_handler.setFormatter(log_formatter)
LOGGER = logging.getLogger()
LOGGER.setLevel(logging.DEBUG)
LOGGER.addHandler(log_handler)


def _launcher(argv):
    try:
        from firewallxpl.interpreter import FirewallXPLInterpreter
    except ModuleNotFoundError as err:
        print("FirewallXPL bootstrap error: missing Python dependency: {}".format(err))
        print("Run: pip install -r requirements.txt")
        print("Check: fxf --doctor")
        raise SystemExit(1)

    fxf = FirewallXPLInterpreter()
    if len(argv[1:]):
        fxf.nonInteractive(argv)
    else:
        fxf.start()


def firewallxpl(argv):
    from tools.xpl_cli import ProductInfo, bootstrap

    try:
        import tomllib
        _ver = tomllib.loads((_ROOT / "pyproject.toml").read_text())["project"]["version"]
    except Exception:
        _ver = "2.2.1"

    product = ProductInfo(
        name="FirewallXPL-Forge",
        slug="firewallxpl-forge",
        version=_ver,
        cli_name="fxf",
        min_python=(3, 8),
        pip_package="firewallxpl-forge",
        setup_hint="pip install -r requirements.txt",
    )
    bootstrap(argv, product, _launcher)


if __name__ == "__main__":
    try:
        firewallxpl(sys.argv)
    except (KeyboardInterrupt, SystemExit):
        pass
