# FirewallXPL-Forge

**Framework de exploração de segurança perimetral** — 164 módulos cobrindo **FW, NGFW, UTM, WAF, VPN, NAC, LB** e firewalls industriais **OT/ICS** em **23 vendors** e **51+ CVEs**.

**Autor:** André Henrique ([@mrhenrike](https://github.com/mrhenrike)) \| [União Geek](https://github.com/Uniao-Geek)

**Idioma:** **Português (pt-BR)** — esta página. **English (en-US, default):** [README.md](README.md)

[![Python 3.9–3.13](https://img.shields.io/badge/Python-3.9--3.13-blue.svg)](https://www.python.org/downloads/)
[![CI](https://github.com/mrhenrike/FirewallXPL-Forge/actions/workflows/compat-matrix.yml/badge.svg)](https://github.com/mrhenrike/FirewallXPL-Forge/actions)
[![PyPI](https://img.shields.io/pypi/v/firewallxpl.svg)](https://pypi.org/project/firewallxpl/)

---

## Arquitetura e Mapa de Superfície de Ataque

![FirewallXPL-Forge v2.0.0 — Mapa de Superfície de Ataque](docs/diagrams/architecture/attack-surface-map-v2.0.0.png)

---

## Instalação

```bash
# Via PyPI (recomendado)
pip install firewallxpl

# Com TUI Rich + descoberta Nmap
pip install firewallxpl[tui,discovery]

# Com engine ML + aceleração GPU
pip install firewallxpl[ml,gpu-nvidia]

# Tudo incluído
pip install firewallxpl[full]

# A partir do código-fonte
git clone https://github.com/mrhenrike/FirewallXPL-Forge.git
cd FirewallXPL-Forge
pip install -e ".[tui,discovery]"
python fxf.py
```

---

## O que o projeto faz

FirewallXPL-Forge fornece **módulos** para testes de segurança **autorizados** contra dispositivos de perímetro (pentest, laboratório, red team controlado). Classes alvo: `perimeter`, `waf`, `vpn`, `nac`, `lb`.

| Tipo | Função |
|------|--------|
| **exploits** | Exploração de vulnerabilidades conhecidas — `check()` + `run()` por módulo |
| **creds** | Credenciais default e brute force via SSH, FTP, Telnet, HTTP, SNMP |
| **scanners** | Identificação de fraquezas; **AutoPwn** orquestra todos os módulos com timing Nmap (T0–T5) |
| **payloads** | Geração de payloads por arquitetura (ARM/MIPS/x86/x64, reverse/bind shells) |
| **encoders** | Codificação de payloads (Python, PHP, Perl) |

---

## Uso

### Shell interativo

```bash
python fxf.py
```

```text
fxf > use exploits/perimeter/fortinet/fortios_sslvpn_path_traversal_cve_2018_13379
fxf (...) > set target 192.168.1.1
fxf (...) > check
[+] Alvo é vulnerável
fxf (...) > run
```

### AutoPwn com ML

```text
fxf > use scanners/autopwn
fxf (scanners/autopwn) > set target 192.168.1.1
fxf (scanners/autopwn) > set timing_template aggressive
fxf (scanners/autopwn) > set ml_advisor true
fxf (scanners/autopwn) > run
```

### Modo não-interativo

```bash
python fxf.py -m exploits/perimeter/fortinet/fortios_auth_bypass_cve_2022_40684 -s "target 10.0.0.1"
python fxf.py -m exploits/perimeter/paloalto/globalprotect_auth_bypass_cve_2026_0257 -s "target vpn.alvo.com" -s "forge_user admin"
```

### Instalador de scripts NSE

Instale os scripts Nmap especializados em firewalls embutidos no pacote:

```bash
# Modo interativo
fxf > install-nse

# Modo não-interativo (requer nmap no PATH)
python fxf.py -c "install-nse"

# Caminho personalizado ou simulação
python fxf.py -c "install-nse --path /usr/local/share/nmap/scripts"
python fxf.py -c "install-nse --check"
```

**Scripts embutidos:**

| Script | Finalidade |
|--------|-----------|
| `fxf-firewall-fingerprint.nse` | Fingerprinting genérico de firewall (11 vendors) |
| `fxf-globalprotect-detect.nse` | Detecção de portal/gateway Palo Alto GlobalProtect |
| `fxf-globalprotect-auth-bypass-cve-2026-0257.nse` | Verificacao passiva de CVE-2026-0257 |
| `fxf-fortios-detect.nse` | Detecção de Fortinet FortiOS |
| `fxf-cisco-asa-detect.nse` | Detecção de Cisco ASA/FTD |

```bash
# Apos instalar: use o nmap diretamente
nmap -p 443 --script fxf-globalprotect-auth-bypass-cve-2026-0257 <alvo>
nmap -p 443,80,8443 --script fxf-firewall-fingerprint 192.168.0.0/24
```

Consulte [docs/wiki/pt-BR/12-scripts-nse.md](docs/wiki/pt-BR/12-scripts-nse.md) para a referencia completa de NSE.

---

## Engines

| Engine | Descrição |
|--------|-----------|
| **Concorrência Async** | asyncio + ThreadPool (até 300 threads) + ProcessPool + ConnectionPool + Pipeline |
| **Aceleração GPU** | NVIDIA CUDA, AMD ROCm, Intel oneAPI, Apple Metal, OpenCL, CPU fallback |
| **Engine ML** | Fingerprinter, AttackOptimizer (Thompson Sampling), AnomalyDetector, AutoTuner |
| **Network Discovery** | Integração Nmap/Masscan + fallback TCP + identificação de dispositivos (23 vendors) |
| **TUI Rich** | Banner estilizado, painéis, tabelas, progress bars, dashboard |

---

## Documentação

- **Wiki (en-US + pt-BR):** [github.com/mrhenrike/FirewallXPL-Forge/wiki](https://github.com/mrhenrike/FirewallXPL-Forge/wiki)

---

## Licença

BSD — ver [LICENSE](LICENSE).

---

> **Autor:** André Henrique ([@mrhenrike](https://github.com/mrhenrike)) \| **União Geek** — [https://github.com/Uniao-Geek](https://github.com/Uniao-Geek)
