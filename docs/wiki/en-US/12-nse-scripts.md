# NSE Scripts — FirewallXPL-Forge Nmap Integration

**Language:** English (en-US). **pt-BR:** [../pt-BR/12-scripts-nse.md](../pt-BR/12-scripts-nse.md)

FirewallXPL-Forge bundles a suite of Nmap Scripting Engine (NSE) scripts for firewall
detection, fingerprinting, and CVE pre-checks. Scripts ship inside the Python package
and are installed into the nmap scripts directory via the `install-nse` command.

---

## Requirements

| Requirement | Details |
|-------------|---------|
| **nmap** | Any version with NSE support (≥ 5.00 recommended; ≥ 7.90 for `sslcert` lib) |
| **firewallxpl** | Installed via `pip install firewallxpl` or editable clone |
| **Permissions** | Write access to nmap scripts dir (may need `sudo` / `RunAs`) |

---

## Installation

### Via interactive shell

```
fxf > install-nse
[+] nmap found: /usr/bin/nmap (7.95)
[*] NSE scripts directory: /usr/share/nmap/scripts
[+] Installed: fxf-globalprotect-detect.nse
[+] Installed: fxf-globalprotect-auth-bypass-cve-2026-0257.nse
[+] Installed: fxf-fortios-detect.nse
[+] Installed: fxf-cisco-asa-detect.nse
[+] Installed: fxf-firewall-fingerprint.nse
[+] nmap --script-updatedb completed.
[+] All scripts installed. Use them with:
     nmap --script fxf-globalprotect-detect <target>
     nmap --script fxf-firewall-fingerprint -p 443,80 <target>
```

### Via non-interactive CLI

```bash
python fxf.py -c "install-nse"
python fxf.py -c "install-nse --force"
python fxf.py -c "install-nse --path /usr/local/share/nmap/scripts"
python fxf.py -c "install-nse --check"
```

### When nmap is not installed

```
fxf > install-nse
[-] nmap not found in PATH. Install nmap first:
     Linux/Debian:  sudo apt-get install nmap
     Linux/RHEL:    sudo yum install nmap
     macOS:         brew install nmap
     Windows:       https://nmap.org/download.html
[*] Bundled scripts are available at:
     /path/to/firewallxpl/resources/arsenal/nse/
     Copy .nse files manually to your nmap scripts directory when ready.
```

### Permission error (Linux/macOS)

```bash
# Run with sudo to write to /usr/share/nmap/scripts
sudo python fxf.py -c "install-nse"
# Or install to a user-writable directory
python fxf.py -c "install-nse --path ~/.nmap/scripts"
```

---

## `install-nse` command reference

```
install-nse [OPTIONS]
```

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| *(no flag)* | — | — | Auto-detect nmap, install all bundled scripts |
| `--check` | flag | false | Dry-run: show what would be installed without copying |
| `--force` | flag | false | Overwrite scripts that already exist in the target dir |
| `--path <dir>` | `string` (path) | auto-detected | Custom destination directory for NSE scripts |
| `--list` | flag | false | List bundled scripts and exit, no install |

### Examples

```
fxf > install-nse
fxf > install-nse --check
fxf > install-nse --force
fxf > install-nse --path /opt/nmap/scripts
fxf > install-nse --list
```

**Sample output — `--list`:**
```
fxf > install-nse --list
[*] Bundled NSE scripts (5 total):
  fxf-cisco-asa-detect.nse
  fxf-firewall-fingerprint.nse
  fxf-fortios-detect.nse
  fxf-globalprotect-auth-bypass-cve-2026-0257.nse
  fxf-globalprotect-detect.nse
```

**Sample output — `--check` (dry-run):**
```
fxf > install-nse --check
[+] nmap found: /usr/bin/nmap (7.95)
[*] NSE scripts directory: /usr/share/nmap/scripts
[*] Bundled NSE scripts: 5
[*] Dry-run — no files will be copied.
     Would install: fxf-globalprotect-detect.nse
     Would install: fxf-globalprotect-auth-bypass-cve-2026-0257.nse
     Would install: fxf-fortios-detect.nse
     Would install: fxf-cisco-asa-detect.nse
     Would install: fxf-firewall-fingerprint.nse
```

---

## Bundled NSE scripts

### `fxf-firewall-fingerprint.nse`

Generic firewall/NGFW fingerprinting across 11 vendors.

**Supported vendors:** Palo Alto, Fortinet, Cisco ASA/FTD, SonicWall, Sophos,
Check Point, Juniper, Zyxel, pfSense, WatchGuard, Barracuda.

**Parameters:**

| Script argument | Type | Default | Description |
|-----------------|------|---------|-------------|
| `fxf.timeout` | `integer` (seconds) | `10` | Per-probe HTTP timeout |
| `fxf.verbose` | `"0"` or `"1"` | `"0"` | Print additional scoring details |

**Usage:**
```bash
nmap -p 443,80,8443 --script fxf-firewall-fingerprint <target>
nmap -p 443 --script fxf-firewall-fingerprint \
    --script-args "fxf.timeout=15,fxf.verbose=1" <target>
```

**Sample output:**
```
PORT    STATE SERVICE
443/tcp open  https
| fxf-firewall-fingerprint:
|   Vendor: SonicWall
|   Product: SonicOS
|   Confidence: HIGH (3 pattern(s) matched)
|   Match path: /auth.html
|
|   Notable CVEs:
|     CVE-2021-20034 (path traversal, CVSS 9.8)
|     CVE-2024-40766 (SSL-VPN access control, CVSS 9.3)
|     CVE-2024-53704 (auth bypass)
|
|   fxf modules: exploits/perimeter/sonicwall/
|_    fxf> search sonicwall
```

---

### `fxf-globalprotect-detect.nse`

Detects Palo Alto Networks GlobalProtect portal and/or gateway.

**Parameters:**

| Script argument | Type | Default | Description |
|-----------------|------|---------|-------------|
| `fxf.timeout` | `integer` (seconds) | `10` | Per-probe HTTP timeout |

**Usage:**
```bash
nmap -p 443 --script fxf-globalprotect-detect <target>
nmap -p 443,8443 --script fxf-globalprotect-detect \
    --script-args "fxf.timeout=15" 10.0.0.0/24
```

**Sample output (detected):**
```
PORT    STATE SERVICE
443/tcp open  https
| fxf-globalprotect-detect:
|   GlobalProtect: DETECTED
|   Component: portal, gateway
|   PAN-OS version: not disclosed in pre-login response
|   Auth-override: referenced in response — check CVE-2026-0257 exposure
|_    Run: nmap --script fxf-globalprotect-auth-bypass-cve-2026-0257 10.0.0.1
```

**Sample output (not detected):**
```
PORT    STATE SERVICE
443/tcp open  https
(no output — host is not a GlobalProtect target)
```

---

### `fxf-globalprotect-auth-bypass-cve-2026-0257.nse`

Passive pre-check for CVE-2026-0257 exposure on a PAN-OS GlobalProtect target.

> **Note:** This script performs a **passive** check only (confirms GlobalProtect presence
> and retrieves TLS certificate metadata). It does **not** forge or submit cookies.
> For active E2E exploitation use the Python module:
> `use exploits/perimeter/paloalto/globalprotect_auth_bypass_cve_2026_0257`

**Parameters:**

| Script argument | Type | Default | Description |
|-----------------|------|---------|-------------|
| `fxf.timeout` | `integer` (seconds) | `10` | Per-probe HTTP timeout |

**Usage:**
```bash
nmap -p 443 --script fxf-globalprotect-auth-bypass-cve-2026-0257 <target>
nmap -p 443 --script fxf-globalprotect-auth-bypass-cve-2026-0257 \
    --script-args fxf.timeout=20 <target>
```

**Sample output:**
```
PORT    STATE SERVICE
443/tcp open  https
| fxf-globalprotect-auth-bypass-cve-2026-0257:
|   CVE-2026-0257 -- GlobalProtect Auth Override Cookie Bypass
|   CVSS: 7.8 HIGH (CVSS 4.0) | CISA KEV: 2026-05-29 | Active exploitation confirmed
|   GlobalProtect: DETECTED (portal + gateway)
|   TLS Certificate CN: vpn.corp.example.com (RSA 2048-bit)
|   Certificate is publicly exposed via TLS handshake
|
|   Status: POTENTIALLY VULNERABLE
|   Condition: vulnerable IF auth override cookies are enabled
|     AND this TLS cert is used for cookie encryption (common default)
|
|   Active bypass (E2E):
|     fxf> use exploits/perimeter/paloalto/globalprotect_auth_bypass_cve_2026_0257
|     fxf> set target 10.0.0.1
|     fxf> run
|
|   Remediation:
|     Patch: PAN-OS 10.2.18-h6+ / 11.1.15+ / 11.2.12+ / 12.1.7+
|     Or: use a DEDICATED certificate for auth override cookies
|     Or: disable auth override cookies entirely
|_  Advisory: https://security.paloaltonetworks.com/CVE-2026-0257
```

---

### `fxf-fortios-detect.nse`

Detects Fortinet FortiOS SSL-VPN portal and FortiGate management interface.

**Parameters:**

| Script argument | Type | Default | Description |
|-----------------|------|---------|-------------|
| `fxf.timeout` | `integer` (seconds) | `10` | Per-probe HTTP timeout |

**Usage:**
```bash
nmap -p 443,10443,8443 --script fxf-fortios-detect <target>
nmap -p 443 --script fxf-fortios-detect 192.168.1.0/24
```

**Sample output:**
```
PORT    STATE SERVICE
443/tcp open  https
| fxf-fortios-detect:
|   FortiOS: DETECTED
|   Component: SSL-VPN portal, Management interface
|   Server header: FortiHTTP
|
|   Notable CVEs (use fxf to exploit):
|     CVE-2018-13379 (path traversal, CVSS 9.8)
|     CVE-2022-40684 (auth bypass, CVSS 9.8)
|     CVE-2023-27997 (SSL-VPN heap RCE, CVSS 9.8)
|     CVE-2024-21762 (SSL-VPN OOB write RCE, CVSS 9.6)
|     CVE-2024-55591 (WebSocket auth bypass, CVSS 9.8)
|
|   fxf modules: exploits/perimeter/fortinet/
|_    fxf> search vendor=fortinet
```

---

### `fxf-cisco-asa-detect.nse`

Detects Cisco ASA and FTD (Firepower Threat Defense) firewalls.

**Parameters:**

| Script argument | Type | Default | Description |
|-----------------|------|---------|-------------|
| `fxf.timeout` | `integer` (seconds) | `10` | Per-probe HTTP timeout |

**Usage:**
```bash
nmap -p 443,8443 --script fxf-cisco-asa-detect <target>
nmap -p 443 --script fxf-cisco-asa-detect 10.0.0.0/24
```

**Sample output:**
```
PORT    STATE SERVICE
443/tcp open  https
| fxf-cisco-asa-detect:
|   Cisco ASA/FTD: DETECTED
|   Component: Clientless SSL-VPN, WebVPN
|
|   Notable CVEs (use fxf to exploit):
|     CVE-2020-3452 (path traversal, CVSS 7.5)
|     CVE-2023-20269 (VPN brute-force, CVSS 9.1)
|     CVE-2023-20198 (IOS XE WebUI privesc, CVSS 10.0)
|     CVE-2025-20362+20333 (FIRESTARTER chain RCE)
|
|   fxf modules: exploits/perimeter/cisco/
|_    fxf> search vendor=cisco
```

---

## Running multiple fxf scripts together

```bash
# Full firewall survey: fingerprint + GlobalProtect check
nmap -p 443,80,8443 \
    --script "fxf-firewall-fingerprint,fxf-globalprotect-detect,fxf-globalprotect-auth-bypass-cve-2026-0257" \
    --script-args "fxf.timeout=15" \
    <target-range>

# Perimeter sweep with NSE + version detection
nmap -sV -p 443 \
    --script "fxf-firewall-fingerprint,fxf-globalprotect-detect,fxf-fortios-detect,fxf-cisco-asa-detect" \
    192.168.0.0/24
```

---

## Manual installation (without `install-nse`)

If nmap is not in PATH or you want to copy files yourself:

```bash
# Linux / macOS
cp /path/to/firewallxpl/resources/arsenal/nse/*.nse /usr/share/nmap/scripts/
nmap --script-updatedb

# Windows (PowerShell)
Copy-Item "C:\...\firewallxpl\resources\arsenal\nse\*.nse" `
    "C:\Program Files (x86)\Nmap\scripts\"
nmap --script-updatedb
```

The bundled scripts are also listed by `install-nse --list`.

---

## Bundled script path (in installed package)

```
firewallxpl/resources/arsenal/nse/
├── fxf-firewall-fingerprint.nse
├── fxf-globalprotect-detect.nse
├── fxf-globalprotect-auth-bypass-cve-2026-0257.nse
├── fxf-fortios-detect.nse
└── fxf-cisco-asa-detect.nse
```

---

[Wiki hub](../README.md)
