# FirewallXPL-Forge wiki (en-US)

**Language:** English (United States) — **default** for this repository. **Português (pt-BR):** [../pt-BR/README.md](../pt-BR/README.md)

**Maintainer:** André Henrique ([@mrhenrike](https://github.com/mrhenrike)) \| [União Geek](https://github.com/Uniao-Geek)

Official usage documentation. Read on GitHub or copy into the **GitHub Wiki** (separate Git repository).

## Architecture diagrams (device classes)

PNG gallery (MikrotikAPI-BF–style). Mermaid sources: [../../diagrams/architecture/README.md](../../diagrams/architecture/README.md).

| SOHO router | Managed switch |
|:---:|:---:|
| ![SOHO](../../img/architecture/fxf_arch_router_soho.png) | ![Switch](../../img/architecture/fxf_arch_switch_l2l3.png) |

| NGFW / UTM | ISP CPE |
|:---:|:---:|
| ![NGFW](../../img/architecture/fxf_arch_ngfw_utm.png) | ![ISP CPE](../../img/architecture/fxf_arch_isp_cpe.png) |

| Mixed edge |
|:---:|
| ![Mixed edge](../../img/architecture/fxf_arch_edge_mixed.png) |

## Table of contents

| Doc | Topics |
|-----|--------|
| [01-introduction-and-installation.md](01-introduction-and-installation.md) | Goals, legal scope, Python, `pip`, `env_doctor`, logs, architecture figure |
| [02-interactive-shell-commands.md](02-interactive-shell-commands.md) | `use`, `set`, `setg`, `show`, `run`, `check`, `back`, `exit`, `help` |
| [03-search-and-listing.md](03-search-and-listing.md) | `search`, filters, `show all/scanners/...` |
| [04-non-interactive-mode.md](04-non-interactive-mode.md) | `fxf.py -m` / `-s`, automation |
| [05-creds-modules.md](05-creds-modules.md) | Default creds and brute force |
| [06-exploits-modules.md](06-exploits-modules.md) | Exploits, `check()`, common options |
| [07-scanners-and-autopwn.md](07-scanners-and-autopwn.md) | `router_scan`, `autopwn`, FortiGate SSL-VPN scanner |
| [08-generic-modules.md](08-generic-modules.md) | PCAP, CVE lookup, wordlists, SNMP, UPnP, BTLE |
| [09-payloads-and-encoders.md](09-payloads-and-encoders.md) | Payloads and encoders |
| [10-catalogs-and-tools.md](10-catalogs-and-tools.md) | JSON catalogs, `tools/` |
| [11-troubleshooting.md](11-troubleshooting.md) | Common failures |
| [Module path index (all locales)](../ANEXO-INDICE-MODULOS.md) | Full path list |

## Regenerate the annex

```bash
python tools/gen_wiki_module_index.py
```

## See also

- [README.md](../../../README.md)
- [CONTRIBUTING.md](../../../CONTRIBUTING.md)
- [docs/COVERAGE_MATRIX.md](../../COVERAGE_MATRIX.md)

---

> **Author:** André Henrique ([@mrhenrike](https://github.com/mrhenrique)) \| **União Geek** — [https://github.com/Uniao-Geek](https://github.com/Uniao-Geek)
