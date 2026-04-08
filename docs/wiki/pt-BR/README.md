# Wiki FirewallXPL-Forge (pt-BR)

**Idioma:** Português (Brazil). **English (en-US, default):** [../en-US/README.md](../en-US/README.md)

**Mantenedor:** André Henrique ([@mrhenrike](https://github.com/mrhenrike)) \| [União Geek](https://github.com/Uniao-Geek)

Documentação de uso do framework. Pode ser lida no GitHub ou copiada para o repositório **GitHub Wiki** (clone Git separado).

## Diagramas de arquitetura (por classe de dispositivo)

Galeria PNG (estilo FirewallXPL-Forge). Fontes Mermaid: [../../diagrams/architecture/README.md](../../diagrams/architecture/README.md).

| Router SOHO | Switch gerido |
|:---:|:---:|
| ![SOHO](../../img/architecture/fxf_arch_router_soho.png) | ![Switch](../../img/architecture/fxf_arch_switch_l2l3.png) |

| NGFW / UTM | CPE ISP |
|:---:|:---:|
| ![NGFW](../../img/architecture/fxf_arch_ngfw_utm.png) | ![CPE](../../img/architecture/fxf_arch_isp_cpe.png) |

| Edge misto |
|:---:|
| ![Edge misto](../../img/architecture/fxf_arch_edge_mixed.png) |

## Índice

| Documento | Conteúdo |
|-----------|----------|
| [01-introducao-e-instalacao.md](01-introducao-e-instalacao.md) | Objetivos, escopo legal, Python, `pip`, `env_doctor`, logs, figura de arquitetura |
| [02-shell-interativo-comandos.md](02-shell-interativo-comandos.md) | `use`, `set`, `setg`, `show`, `run`, `check`, `back`, `exit`, `help` |
| [03-busca-e-listagem.md](03-busca-e-listagem.md) | `search`, filtros, `show all/scanners/...` |
| [04-modo-nao-interativo.md](04-modo-nao-interativo.md) | `fxf.py -m` / `-s`, automação |
| [05-modulos-creds.md](05-modulos-creds.md) | Credenciais e brute force |
| [06-modulos-exploits.md](06-modulos-exploits.md) | Exploits, `check()`, opções comuns |
| [07-scanners-e-autopwn.md](07-scanners-e-autopwn.md) | `router_scan`, `autopwn`, FortiGate SSL-VPN |
| [08-modulos-generic.md](08-modulos-generic.md) | PCAP, CVE lookup, wordlists, SNMP, UPnP, BTLE |
| [09-payloads-e-encoders.md](09-payloads-e-encoders.md) | Payloads e encoders |
| [10-catalogos-e-ferramentas.md](10-catalogos-e-ferramentas.md) | Catálogos JSON, `tools/` |
| [11-troubleshooting.md](11-troubleshooting.md) | Erros frequentes |
| [Anexo: índice de módulos](../ANEXO-INDICE-MODULOS.md) | Lista completa de caminhos |

## Regenerar o anexo

```bash
python tools/gen_wiki_module_index.py
```

## Ver também

- [README.pt-BR.md](../../README.pt-BR.md)
- [CONTRIBUTING.pt-BR.md](../../CONTRIBUTING.pt-BR.md)
- [docs/COVERAGE_MATRIX.md](../COVERAGE_MATRIX.md)

---

> **Author:** André Henrique ([@mrhenrike](https://github.com/mrhenrike)) \| **União Geek** — [https://github.com/Uniao-Geek](https://github.com/Uniao-Geek)
