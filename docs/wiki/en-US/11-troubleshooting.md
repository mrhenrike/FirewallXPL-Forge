# Troubleshooting

**Language:** English (en-US). **pt-BR:** [../pt-BR/11-troubleshooting.md](../pt-BR/11-troubleshooting.md)

---

## Installation issues

### `ModuleNotFoundError: firewallxpl`

Cause: running from a directory where the package is not installed.

```bash
pip install -e .
# or
pip install firewallxpl
```

### Python version too old

```
FirewallXPL requires Python 3.8+ (detected: 3.7.x)
```

Upgrade to Python 3.8 or later. Use `pyenv` or system packages.

---

## Interactive shell

### `stdin is not a TTY`

Cause: piped input or non-terminal context (e.g. CI).

Solution: use non-interactive mode:
```bash
python fxf.py -m <module> -s "option value"
```

### `Unknown command`

- Commands are case-sensitive.
- Ensure you are at the `fxf >` prompt (not inside a module prompt that does not accept that command).
- Module commands (`run`, `set`, `check`, `back`) only work when a module is loaded.

### Tab completion not working (Windows)

Windows does not have GNU readline by default. Typed-out commands work normally.
Install `pyreadline3` for basic completion support:
```bash
pip install pyreadline3
```

---

## NSE script installer

### `[-] nmap not found in PATH`

Install nmap for your OS:
```bash
sudo apt-get install nmap        # Debian/Ubuntu
sudo yum install nmap            # RHEL/CentOS
brew install nmap                # macOS Homebrew
# Windows: https://nmap.org/download.html
```

Then re-run `fxf > install-nse`.

### `Permission denied` when installing NSE scripts

Linux/macOS: the nmap scripts directory (`/usr/share/nmap/scripts/`) requires
root/sudo to write.

```bash
sudo python fxf.py -c "install-nse"
# Or install to a user-writable directory:
python fxf.py -c "install-nse --path ~/.nmap/scripts"
mkdir -p ~/.nmap/scripts
nmap --datadir ~/.nmap --script-updatedb
```

### NSE scripts installed but nmap does not find them

Run `nmap --script-updatedb` manually:
```bash
nmap --script-updatedb
# or
sudo nmap --script-updatedb
```

### `No bundled NSE scripts found`

Cause: package installed without `resources/` data (editable install or incomplete build).

```bash
# From source, ensure resources are present:
ls firewallxpl/resources/arsenal/nse/
# Should list 5 .nse files

# If missing, clone fresh:
git clone https://github.com/mrhenrike/FirewallXPL-Forge.git
```

---

## Network / protocol issues

### Paramiko SSL / cryptography errors

```bash
# Recreate the virtual environment with updated packages:
pip install --upgrade pip
pip install --upgrade paramiko cryptography
```

### SNMP timeouts

Checklist:
1. UDP/161 open on target (not blocked by firewall).
2. Community string is correct (`public` is the default but often changed).
3. SNMP service is enabled on the device.
4. Correct SNMP version (v1, v2c, v3).

### Python 3.13+ Telnet errors

```
ImportError: No module named 'telnetlib'
```

Install the replacement:
```bash
pip install "firewallxpl[telnet]"
# or directly:
pip install telnetlib3
```

### Scapy / PCAP `ImportError`

```bash
pip install scapy
# Windows: live capture may need Npcap (https://npcap.com)
# Offline .pcap analysis often works without Npcap
```

---

## CVE-2026-0257 exploit issues

### `Could not forge cookies — target may use EC certificates`

Cause: The target's TLS certificate uses an EC (elliptic curve) key instead of RSA.
The CVE-2026-0257 bypass requires RSA-PKCS1v15 encryption.

Check: run `fxf-globalprotect-auth-bypass-cve-2026-0257.nse` to inspect the cert type.

### Auth bypass not confirmed after forging

Possible causes:
- Authentication override cookies are **disabled** on this device (not vulnerable).
- The TLS certificate **is not** the same as the cookie-signing certificate (patched config).
- The device is **patched** (PAN-OS 10.2.18-h6+ / 11.1.15+ / 11.2.12+ / 12.1.7+).

Check the forged cookie values in the output and test manually against
`/ssl-vpn/prelogin.esp` using a web proxy tool.

---

## AutoPwn issues

### AutoPwn overloads the target / causes DoS

Use a lower timing template:
```text
fxf (AutoPwn) > set timing_template paranoid
fxf (AutoPwn) > set threads 2
fxf (AutoPwn) > set module_timeout_s 60
```

### AutoPwn runs indefinitely

Set `module_timeout_s` and ensure `threads` is not too high:
```text
fxf (AutoPwn) > set module_timeout_s 30
```

---

## Log file management

```bash
# Truncate
> firewallxpl.log
# Rotate manually
mv firewallxpl.log firewallxpl.log.bak
```

**Never commit `firewallxpl.log`** — it may contain credentials or sensitive banners.

---

[Wiki hub](../README.md)
