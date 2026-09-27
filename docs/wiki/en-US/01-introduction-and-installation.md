# Introduction, scope, and installation

**Language:** English (en-US). **pt-BR:** [../pt-BR/01-introducao-e-instalacao.md](../pt-BR/01-introducao-e-instalacao.md)

## What FirewallXPL-Forge is

A **modular Python framework** for **authorized** security testing of network perimeter
devices: NGFW, UTM, WAF, VPN concentrators, NAC, load balancers, and OT-adjacent
firewalls. It follows the Metasploit module model: select a module, set options,
run `check` then `run`.

> **Migration notice (v2.1.0):** All 81 modules are available in
> [EmbedXPL-Forge](https://github.com/mrhenrike/EmbedXPL-Forge) (`pip install embedxpl`).
> FirewallXPL-Forge v2.1.0 is the final standalone release and will not receive new modules.

**Architecture overview:**

```
fxf > use exploits/perimeter/fortinet/fortios_auth_bypass_cve_2022_40684
fxf (FortiOS Auth Bypass CVE-2022-40684) > set target 10.0.0.1
fxf (FortiOS Auth Bypass CVE-2022-40684) > check
[+] Target is vulnerable
fxf (FortiOS Auth Bypass CVE-2022-40684) > run
```

---

## Legal and ethical use

**Use only on networks and devices you own or have explicit written permission to test.**
Maintainers are not responsible for misuse. Follow your contract and rules of engagement.

---

## Requirements

| Item | Minimum | Notes |
|------|---------|-------|
| Python | 3.8 | 3.13+ requires `telnetlib3` extra |
| OS | Linux, macOS, Windows | Primary dev target is Linux |
| nmap | any | Optional; needed for `discovery` extra and NSE scripts |
| cryptography lib | any | Needed for CVE-2026-0257 cookie forge (`pip install cryptography`) |

---

## Install

### From PyPI (recommended)

```bash
pip install firewallxpl
# With TUI and nmap discovery support:
pip install "firewallxpl[tui,discovery]"
```

### From source (development / editable)

```bash
git clone https://github.com/mrhenrike/FirewallXPL-Forge.git
cd FirewallXPL-Forge
python3 -m venv .venv
source .venv/bin/activate      # Linux / macOS
# .venv\Scripts\Activate.ps1  # Windows PowerShell
pip install -e ".[tui,discovery]"
```

### Optional extras

| Extra | Installs | Purpose |
|-------|----------|---------|
| `tui` | `rich` | Colored TUI output |
| `tui-full` | `rich`, `textual` | Full TUI with interactive tables |
| `discovery` | `python-nmap` | Nmap-powered host/service discovery |
| `ml` | `scikit-learn`, `joblib` | ML advisor for AutoPwn |
| `ml-gpu` | `torch` | GPU timing logits (CUDA) |
| `async` | `aiohttp`, `asyncssh` | Async HTTP + SSH client |
| `full` | all above | Everything |

---

## Install NSE scripts

After installing firewallxpl, deploy the bundled firewall-specific NSE scripts to nmap:

```bash
# Interactive
python fxf.py
fxf > install-nse

# Non-interactive (requires nmap in PATH)
python fxf.py -c "install-nse"

# With elevated privileges (Linux)
sudo python fxf.py -c "install-nse"

# Custom destination
python fxf.py -c "install-nse --path /usr/local/share/nmap/scripts"
```

If nmap is not installed, the command displays the bundled script path so you can
copy files manually later. See [12-nse-scripts.md](12-nse-scripts.md) for the full NSE reference.

---

## Diagnostics

```bash
python tools/env_doctor.py
```

Checks core imports. Scapy is not checked; fix Scapy manually if `generic/pcap/*`
modules fail.

```bash
python tools/check_env_readiness.py
```

Validates environment readiness (module indexing, resource files).

---

## Start the application

### Interactive mode

```bash
python fxf.py
```

Requires a **TTY**. The prompt is `fxf >`.

**Environment customization:**

| Variable | Default | Effect |
|----------|---------|--------|
| `FXF_RAW_PROMPT` | `fxf >` (underlined) | Prompt when no module is loaded |
| `FXF_MODULE_PROMPT` | `fxf (module) >` | Prompt with a module loaded |

### Non-interactive / batch mode

```bash
python fxf.py -m <module/path> [-s "option value"] ...
python fxf.py -h
```

See [04-non-interactive-mode.md](04-non-interactive-mode.md).

---

## Log file

`firewallxpl.log` in the current working directory. Rotating handler, max 500 KB.

## Command history

`~/.fxf_history` (readline history, 100 entries).

---

[Wiki hub](../README.md)
