# Scanners and AutoPwn

**Language:** English (en-US). **pt-BR:** [../pt-BR/07-scanners-e-autopwn.md](../pt-BR/07-scanners-e-autopwn.md)

Scanner modules orchestrate multi-module campaigns against a single target or subnet.
`scanners/autopwn` is the main entry point for automated perimeter testing.

---

## `scanners/autopwn`

Parallel credential and exploit scanning with **Nmap-style timing templates** (T0–T5).

### Usage

```text
fxf > use scanners/autopwn
fxf (AutoPwn) > set target 192.168.50.1
fxf (AutoPwn) > set timing_template polite
fxf (AutoPwn) > set target_device_class ngfw
fxf (AutoPwn) > run
```

### Core options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `target` | `OptIP` / `string` | `""` | Target IP or subnet (CIDR) |
| `target_device_class` | `OptString` | `"multi"` | Device class filter: `multi`, `router`, `switch`, `tap`, `fw`, `ngfw`, `isp_cpe` |
| `vendor` | `OptString` | `""` | Vendor name filter (e.g. `fortinet`, `cisco`) |
| `timing_template` | `OptString` | `"normal"` | `t0`–`t5` or `paranoid`, `sneaky`, `polite`, `normal`, `aggressive`, `insane` |
| `check_exploits` | `OptBool` | `true` | Run exploit `check()` methods |
| `check_creds` | `OptBool` | `true` | Run credential modules |
| `threads` | `OptInteger` | `8` | Concurrent module threads |
| `module_timeout_s` | `OptInteger` | `30` | Per-module timeout in seconds |
| `verify_positive_twice` | `OptBool` | `false` | Re-verify positive results |

### Timing template reference

| Template | Alias | Speed | Stealth | Use case |
|----------|-------|-------|---------|---------|
| `t0` | `paranoid` | Slowest | Highest | IDS evasion, high detection sensitivity |
| `t1` | `sneaky` | Slow | High | Low-detection environments |
| `t2` | `polite` | Moderate | Moderate | Standard authorized audits |
| `t3` | `normal` | Default | Moderate | General use |
| `t4` | `aggressive` | Fast | Low | Robust networks, lab |
| `t5` | `insane` | Fastest | None | Lab-only, may lose data |

### Protocol-specific options

| Option | Type | Description |
|--------|------|-------------|
| `http_use` | `OptBool` | Enable HTTP checks |
| `https_use` | `OptBool` | Enable HTTPS checks |
| `ssh_use` | `OptBool` | Enable SSH checks |
| `ftp_use` | `OptBool` | Enable FTP checks |
| `telnet_use` | `OptBool` | Enable Telnet checks |
| `snmp_use` | `OptBool` | Enable SNMP checks |
| `tcp_use` | `OptBool` | Enable raw TCP checks |
| `udp_use` | `OptBool` | Enable UDP checks |
| `http_port` | `OptPort` | HTTP port override |
| `https_port` | `OptPort` | HTTPS port override |
| `ssh_port` | `OptPort` | SSH port override |

---

### Optional ML advisor (show advanced)

**Off by default.** Reorders the exploit/credential module queue and can suggest or
auto-apply a timing template using a lightweight linear model (feature vector + JSON weights).

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `ml_advisor` | `OptBool` | `false` | Enable ML advisor |
| `ml_auto_timing` | `OptBool` | `false` | Auto-apply advisor timing suggestion |
| `ml_use_gpu` | `OptBool` | `false` | Use GPU for logits (requires `pip install .[ml-gpu]`) |

> CPU/RAM overhead of the ML layer is small; network I/O dominates total scan time.

**Example with ML:**
```text
fxf (AutoPwn) > set ml_advisor true
fxf (AutoPwn) > set ml_auto_timing true
fxf (AutoPwn) > run
```

---

## `scanners/routers/fortigate_sslvpn_scan`

FortiGate SSL-VPN–oriented recon and vulnerability enumeration.

```text
fxf > use scanners/routers/fortigate_sslvpn_scan
fxf (FortiGate SSL-VPN Scanner) > set target 10.0.0.1
fxf (FortiGate SSL-VPN Scanner) > run
```

---

## `scanners/misc/misc_scan`

General perimeter recon scanner; covers HTTP fingerprinting and banner collection
across multiple ports.

```text
fxf > use scanners/misc/misc_scan
fxf (Misc Scan) > set target 10.0.0.0/24
fxf (Misc Scan) > run
```

---

## NSE scripts for pre-scanning

Before running AutoPwn, use the bundled NSE scripts for lightweight fingerprinting:

```bash
# Identify firewall vendor
nmap -p 443,80,8443 --script fxf-firewall-fingerprint 192.168.0.0/24

# Check for GlobalProtect CVE-2026-0257 exposure
nmap -p 443 --script fxf-globalprotect-auth-bypass-cve-2026-0257 10.0.0.1
```

Then run the corresponding fxf exploit module on confirmed targets. See
[12-nse-scripts.md](12-nse-scripts.md) for the full NSE reference.

---

[Wiki hub](../README.md)
