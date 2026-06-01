# `creds` modules

**Language:** English (en-US). **pt-BR:** [../pt-BR/05-modulos-creds.md](../pt-BR/05-modulos-creds.md)

Credential modules test authentication services using default credentials or dictionary
attacks. Supported protocols: SSH, Telnet, FTP/SFTP, HTTP (basic, digest, form),
SNMP, and more.

---

## Typical flow

```text
fxf > use creds/generic/ssh_default
fxf (SSH Default Credentials) > set target 192.168.1.1
fxf (SSH Default Credentials) > set port 22
fxf (SSH Default Credentials) > set threads 4
fxf (SSH Default Credentials) > show options
fxf (SSH Default Credentials) > run
```

**Sample output:**
```
[*] Running module creds.generic.ssh_default...
[*] 192.168.1.1:22 — trying admin:admin
[*] 192.168.1.1:22 — trying admin:1234
[+] 192.168.1.1:22 — Found credentials: admin / admin
[*] 192.168.1.1:22 — trying root:root
[+] 192.168.1.1:22 — Found credentials: root / root
```

---

## Common options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `target` | `OptIP` / `string` | `""` | Target IP, IPv6, hostname, or `file://path` with `ip:port` entries |
| `port` | `OptPort` | protocol default | Service port (integer 1–65535) |
| `threads` | `OptInteger` | `8` | Concurrent connection threads |
| `defaults` | `OptString` | embedded list | Embedded `user:pass` list or `file://path/to/list.txt` |
| `stop_on_success` | `OptBool` | `false` | Stop after the first successful credential |
| `verbosity` | `OptBool` | `false` | Print every attempt |
| `timeout` | `OptInteger` | `10` | Per-attempt timeout in seconds |
| `ssl` | `OptBool` | `false` | Use TLS/SSL where applicable |

> **Note:** Option names vary by module. Always run `show options` after loading a module.

---

## Generic credential modules

| Module path | Protocol | Notes |
|-------------|----------|-------|
| `creds/generic/ssh_default` | SSH | Paramiko-based |
| `creds/generic/telnet_default` | Telnet | Plain + `telnetlib3` on Py 3.13+ |
| `creds/generic/ftp_default` | FTP | ftplib |
| `creds/generic/http_basic_digest_default` | HTTP Basic/Digest | `requests` |
| `creds/generic/http_basic_digest_bruteforce` | HTTP Basic/Digest | Dictionary attack |
| `creds/generic/http_multi_auth_default` | HTTP (multi-mode) | Basic, Digest, NTLM |
| `creds/generic/http_web_form_bruteforce` | HTTP form | Configurable field names and success/failure rules |
| `creds/generic/snmp_default` | SNMP v1/v2c | Community string brute-force |

---

## Vendor-specific credential modules

| Module prefix | Vendor / focus |
|---------------|----------------|
| `creds/perimeter/cisco/` | Cisco ASA, IOS |
| `creds/perimeter/fortinet/` | FortiGate, FortiOS |
| `creds/perimeter/juniper/` | Juniper SRX, JunOS |
| `creds/perimeter/ipfire/` | IPFire |
| `creds/perimeter/pfsense/` | pfSense |

See the full list: [../ANEXO-INDICE-MODULOS.md](../ANEXO-INDICE-MODULOS.md)

---

## Using `setg` across multiple modules

```text
fxf > setg target 10.0.0.1
target => 10.0.0.1
fxf > use creds/generic/ssh_default
fxf (SSH Default Credentials) > run

fxf > use creds/generic/ftp_default
fxf (FTP Default Credentials) > run
# target is already set to 10.0.0.1
```

---

## HTTP web form options (`http_web_form_bruteforce`)

| Option | Type | Description |
|--------|------|-------------|
| `url` | `OptString` | Full login URL |
| `username_field` | `OptString` | HTML form field name for username |
| `password_field` | `OptString` | HTML form field name for password |
| `success_pattern` | `OptString` | Regex or string indicating login success |
| `failure_pattern` | `OptString` | Regex or string indicating login failure |
| `usernames` | `OptString` | `file://path` or comma-separated list |
| `passwords` | `OptString` | `file://path` or comma-separated list |

---

## Non-interactive batch usage

```bash
python fxf.py \
    -m creds/generic/ssh_default \
    -s "target 192.168.0.50" \
    -s "port 22" \
    -s "threads 8" \
    -s "stop_on_success true"
```

---

[Wiki hub](../README.md)
