# Introduction, scope, and installation

**Language:** English (en-US). **pt-BR:** [../pt-BR/01-introducao-e-instalacao.md](../pt-BR/01-introducao-e-instalacao.md)

## What FirewallXPL-Forge is

A **modular Python framework** for **authorized** security testing of embedded network gear (routers, switches, TAPs, firewalls, NGFW): credential tests, public vulnerability checks, scanners, PCAP/CVE utilities, etc.

**Architecture overview (SOHO router example — full gallery in [wiki hub README](../README.md)):**

![SOHO router — attack surface & tool coverage](../../img/architecture/fxf_arch_router_soho.png)

## Legal and ethical use

**Use only on networks and devices you own or have explicit written permission to test.** Maintainers are not responsible for misuse. Follow your contract and rules of engagement.

## Requirements

- **Python 3.8–3.13**
- Dependencies in `requirements.txt`
- **Python 3.13+:** `telnetlib3` replaces removed stdlib `telnetlib`
- **PCAP modules** need **Scapy**; live capture on Windows may need Npcap — offline `.pcap` analysis often works with Python only

## Install

```bash
git clone https://github.com/mrhenrike/FirewallXPL-Forge.git
cd FirewallXPL-Forge
python3 -m venv .venv
source .venv/bin/activate   # Linux/macOS
# .venv\Scripts\activate    # Windows
python3 -m pip install -r requirements.txt
```

## Diagnostics

```bash
python tools/env_doctor.py
```

Checks core imports. Scapy is not in the doctor today; fix Scapy manually if `generic/pcap/*` imports fail.

## Start the app

```bash
python fxf.py
```

Interactive mode needs a **TTY**. For automation use `-m` / `-s` (see [04-non-interactive-mode.md](04-non-interactive-mode.md)).

## Log file

**`firewallxpl.log`** in the current working directory receives bootstrap logging.

## Command history

Readline history is typically `~/.rxf_history`.

---

[Wiki hub](../README.md)
