# Architecture diagrams — FirewallXPL-Forge

**Author:** André Henrique ([@mrhenrike](https://github.com/mrhenrike)) \| **União Geek** — [https://github.com/Uniao-Geek](https://github.com/Uniao-Geek)

**Languages:** Diagram labels are **English (en-US)** by default (aligned with tool output). **Português (pt-BR):** [README.pt-BR.md](README.pt-BR.md).

Diagrams follow the same visual language as **MikrotikAPI-BF** (`img/mikrotik_*`): central device core, **access vectors** as spokes, **✓ / ✗** for coverage in FirewallXPL-Forge (`creds`, `exploits`, `scanners`, `generic`), optional CVE callouts.

## Files

| File | Category |
|------|----------|
| [01-router-soho.mmd](01-router-soho.mmd) | SOHO / home gateway (Linux / RTOS firmware) |
| [02-switch-l2-l3.mmd](02-switch-l2-l3.mmd) | Managed L2/L3 switch |
| [03-ngfw-utm.mmd](03-ngfw-utm.mmd) | NGFW / UTM / enterprise firewall appliance |
| [04-isp-cpe.mmd](04-isp-cpe.mmd) | ISP CPE / residential gateway |
| [05-edge-mixed.mmd](05-edge-mixed.mmd) | Mixed small-office edge (router + UTM-lite) |
| [06-network-tap.mmd](06-network-tap.mmd) | Network TAP / passive broker (mgmt-only vectors) |

## Rendered PNGs

| PNG | Source |
|-----|--------|
| [../../img/architecture/fxf_arch_router_soho.png](../../img/architecture/fxf_arch_router_soho.png) | SOHO router |
| [../../img/architecture/fxf_arch_switch_l2l3.png](../../img/architecture/fxf_arch_switch_l2l3.png) | Switch |
| [../../img/architecture/fxf_arch_ngfw_utm.png](../../img/architecture/fxf_arch_ngfw_utm.png) | NGFW / UTM |
| [../../img/architecture/fxf_arch_isp_cpe.png](../../img/architecture/fxf_arch_isp_cpe.png) | ISP CPE |
| [../../img/architecture/fxf_arch_edge_mixed.png](../../img/architecture/fxf_arch_edge_mixed.png) | Mixed edge |

### Gallery (embedded)

| SOHO router | Switch |
|:---:|:---:|
| ![SOHO router](../../img/architecture/fxf_arch_router_soho.png) | ![Switch](../../img/architecture/fxf_arch_switch_l2l3.png) |

| NGFW / UTM | ISP CPE |
|:---:|:---:|
| ![NGFW / UTM](../../img/architecture/fxf_arch_ngfw_utm.png) | ![ISP CPE](../../img/architecture/fxf_arch_isp_cpe.png) |

| Mixed edge |
|:---:|
| ![Mixed edge](../../img/architecture/fxf_arch_edge_mixed.png) |

**TAP / passive devices:** see Mermaid source [06-network-tap.mmd](06-network-tap.mmd) — PNG optional (low remote attack surface).

## Render locally (optional)

With [Mermaid CLI](https://github.com/mermaid-js/mermaid-cli):

```bash
npx @mermaid-js/mermaid-cli -i docs/diagrams/architecture/01-router-soho.mmd -o docs/img/architecture/router_soho.png -b transparent
```

## Português (pt-BR)

- **✓ Coberto:** módulos existentes em `firewallxpl/modules/` para aquele vetor (ex.: `creds`, `exploits`, `generic` PCAP/CVE).
- **✗ Parcial / não focado:** depende de modelo; usar `generic/cve/cve_lookup`, `scanners/autopwn` e pesquisa por *vendor*.

---

> **Author:** André Henrique ([@mrhenrike](https://github.com/mrhenrique)) \| **União Geek** — [https://github.com/Uniao-Geek](https://github.com/Uniao-Geek)
