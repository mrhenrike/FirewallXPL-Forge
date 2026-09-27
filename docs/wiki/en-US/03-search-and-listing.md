# Search and listing

**Language:** English (en-US). **pt-BR:** [../pt-BR/03-busca-e-listagem.md](../pt-BR/03-busca-e-listagem.md)

---

## `search` — find modules

```
search [type=<type>] [device=<device>] [vendor=<vendor>] [language=<lang>] [payload=<payload>] <keyword(s)>
```

Keywords are lowercased. Multiple keywords are joined with logical **AND** (all must appear in the module path).

### Keyword-only search

```
fxf > search cisco
fxf > search fortinet ssl-vpn
fxf > search paloalto globalprotect
fxf > search cve_2026_0257
```

**Sample output:**
```
fxf > search paloalto
exploits/perimeter/paloalto/globalprotect_auth_bypass_cve_2026_0257
exploits/perimeter/paloalto/globalprotect_cmd_injection_cve_2024_3400
exploits/perimeter/paloalto/panos_auth_bypass_cve_2025_0108
exploits/perimeter/paloalto/panos_mgmt_auth_bypass_cve_2024_0012
exploits/perimeter/paloalto/panos_privesc_cve_2024_9474
exploits/perimeter/paloalto/panos_saml_auth_bypass_cve_2020_2021
```

### Named filter parameters

| Parameter | Type | Valid values | Description |
|-----------|------|-------------|-------------|
| `type=` | `string` | `exploits`, `creds`, `scanners`, `generic`, `payloads`, `encoders` | Top-level module type |
| `device=` | `string` | `perimeter`, `waf`, `vpn`, `nac`, `lb` (see scope JSON) | Subpackage under `exploits/` |
| `vendor=` | `string` | e.g. `fortinet`, `cisco`, `paloalto`, `sonicwall` | Vendor path segment |
| `language=` | `string` | `python`, `php`, `perl` | Under `encoders/` |
| `payload=` | `string` | `x86`, `x64`, `arm`, `mips`, `cmd`, `python`, `php` | Under `payloads/` |

**Examples:**
```
fxf > search type=exploits vendor=fortinet
fxf > search type=exploits device=perimeter cisco rce
fxf > search type=creds generic ssh
fxf > search type=encoders language=php
fxf > search type=payloads payload=arm
```

**Error output (invalid filter):**
```
fxf > search device=cameras
[-] Unknown exploit type.
```

*(Domain `cameras` is disabled in this distribution.)*

---

## `show` — list modules and categories

```
show <subcommand>
```

### Global subcommands (no module required)

| Subcommand | Description |
|------------|-------------|
| `all` | All indexed modules |
| `exploits` | All exploit modules |
| `scanners` | All scanner modules |
| `creds` | All credential modules |
| `generic` | All generic modules |
| `encoders` | All encoder modules |
| `payloads` | All payload modules |
| `wordlists` | List available wordlist resources |
| `perimeter` | Exploits under `perimeter/` category |
| `waf` | Exploits under `waf/` category |
| `vpn` | Exploits under `vpn/` category |
| `nac` | Exploits under `nac/` category |
| `lb` | Exploits under `lb/` (load balancers) category |

**Examples:**
```
fxf > show perimeter
fxf > show exploits
fxf > show scanners
fxf > show wordlists
```

### Module subcommands (requires a loaded module)

| Subcommand | Description |
|------------|-------------|
| `info` | `__info__` metadata: name, description, authors, references |
| `options` | Standard options with current values and descriptions |
| `advanced` | All options including hidden/advanced ones |
| `devices` | Target device list |

**Sample `show info` output:**
```
fxf (GlobalProtect Auth Bypass CVE-2026-0257) > show info
name         : PAN-OS GlobalProtect Auth Override Cookie Bypass (CVE-2026-0257)
description  : CVSS 7.8 HIGH. Authentication override cookies in GlobalProtect are
               encrypted with RSA-PKCS1v15 using a certificate whose public key is
               exposed via the device's public HTTPS TLS handshake...
authors      : ('Andre Henrique (@mrhenrike) | Uniao Geek',)
references   : ('https://security.paloaltonetworks.com/CVE-2026-0257', ...)
```

**Sample `show options` output:**
```
fxf (GlobalProtect Auth Bypass CVE-2026-0257) > show options
Name              Current settings    Description
target            192.168.1.1         Target IP or hostname
port              443                 HTTPS port (default: 443)
ssl               true                Use HTTPS
forge_user        admin               Username to forge in the auth cookie
forge_domain                          Domain for the forged cookie
probe_gateway     true                Also probe the GlobalProtect gateway
dump_session      false               Dump session metadata if bypass confirmed
```

---

## Full module index

For a complete list of all module paths, see:

```bash
# Generate / refresh the index
python tools/gen_wiki_module_index.py
```

Output: [../ANEXO-INDICE-MODULOS.md](../ANEXO-INDICE-MODULOS.md)

---

## `use` — path mapping

| Shell path | Python module |
|-----------|---------------|
| `exploits/perimeter/paloalto/globalprotect_auth_bypass_cve_2026_0257` | `firewallxpl.modules.exploits.perimeter.paloalto.globalprotect_auth_bypass_cve_2026_0257` |
| `creds/generic/ssh_default` | `firewallxpl.modules.creds.generic.ssh_default` |
| `scanners/autopwn` | `firewallxpl.modules.scanners.autopwn` |

Dots and slashes are interchangeable in the shell input.

---

[Wiki hub](../README.md)
