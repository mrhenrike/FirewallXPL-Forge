# `generic` modules

**Language:** English (en-US). **pt-BR:** [../pt-BR/08-modulos-generic.md](../pt-BR/08-modulos-generic.md)

Generic modules cover cross-vendor capabilities: CVE lookup, PCAP analysis, SNMP
traps, UPnP/SSDP discovery, wordlist generation, and Bluetooth LE scanning.

---

## CVE lookup — `generic/cve/cve_lookup`

Queries the embedded offline CVE database for network/perimeter devices.

```text
fxf > use generic/cve/cve_lookup
fxf (CVE Lookup) > set vendor paloalto
fxf (CVE Lookup) > run
```

**Options:**

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `vendor` | `OptString` | `""` | Vendor name (fuzzy matched; e.g. `paloalto`, `fortinet`, `cisco`) |
| `product` | `OptString` | `""` | Product name or model |
| `version` | `OptString` | `""` | Firmware/software version string |
| `banner` | `OptString` | `""` | Raw banner text (tokens extracted automatically) |
| `remote_only` | `OptBool` | `true` | Show only remotely exploitable CVEs |
| `show_physical` | `OptBool` | `false` | Include physical-access-only CVEs |

**Sample output — CVE-2026-0257:**
```
fxf > use generic/cve/cve_lookup
fxf (CVE Lookup) > set vendor paloalto
fxf (CVE Lookup) > set product pan-os
fxf (CVE Lookup) > run

[+] CVE-2026-0257 | CVSS: 7.8 | paloalto / pan-os | REMOTE
    GlobalProtect auth override cookie bypass (CWE-565). Active exploitation confirmed.
    EXPLOITABLE (rxf module available)
    Module: exploits/perimeter/paloalto/globalprotect_auth_bypass_cve_2026_0257
    Refs: https://security.paloaltonetworks.com/CVE-2026-0257

[+] CVE-2024-3400 | CVSS: 10.0 | paloalto / pan-os | REMOTE
    Command injection in GlobalProtect leading to RCE
    EXPLOITABLE (rxf module available)
    Module: exploits/perimeter/paloalto/globalprotect_cmd_injection_cve_2024_3400
```

---

## Exploit-DB offline — `generic/external/exploitdb_embedded_lookup`

Searches the bundled `files_exploits.csv` from the Exploit-DB mirror. No
`searchsploit` or external CLI required.

Location: `firewallxpl/resources/arsenal/pocs/integrated_modules/`

> Preserve GPLv2 notices when redistributing mirror contents.

---

## PCAP / Wi-Fi offline — `generic/pcap/*`

Requires **Scapy**. For authorized lab / forensic use only.

| Module | Role |
|--------|------|
| `pcap_ap_station_mapper` | Map APs and stations from a capture |
| `pcap_handshake_extractor` | Extract WPA handshakes |
| `pcap_offline_wpa_crack` | Offline WPA cracking workflow |
| `pcap_wep_crack` | WEP statistical attacks |
| `pcap_pmkid_attack` | PMKID extraction and offline attack workflow |
| `pcap_tkip_downgrade` | TKIP / Michael analysis |
| `pcap_dragonblood` | WPA3/SAE-related signal analysis |
| `pcap_wpe_harvest` | EAP/MSCHAPv2 harvest-style analysis |
| `pcap_credential_sniffer` | Extract credential patterns from capture |

**Common options:**

| Option | Type | Description |
|--------|------|-------------|
| `pcap_file` | `OptString` | Path to `.pcap` or `.pcapng` file |
| `interface` | `OptString` | Network interface for live capture (Linux, with Scapy) |
| `wordlist` | `OptString` | Path to wordlist for offline cracking modules |

---

## Wordlist generator — `generic/wordlist_generator`

Parameterized wordlist generation to feed credential and brute-force modules.

```text
fxf > use generic/wordlist_generator
fxf (Wordlist Generator) > show options
fxf (Wordlist Generator) > run
```

---

## SNMP trap listener — `generic/snmp_trap_listener`

Listens for SNMP traps in lab environments to collect device-generated alerts.

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `bind_address` | `OptString` | `0.0.0.0` | Bind address |
| `port` | `OptPort` | `162` | UDP trap port |
| `community` | `OptString` | `public` | SNMP community string |

---

## UPnP / SSDP — `generic/ssdp_msearch`

Discovers UPnP devices on the LAN via SSDP M-SEARCH.

```text
fxf > use generic/ssdp_msearch
fxf (SSDP M-SEARCH) > set timeout 5
fxf (SSDP M-SEARCH) > run
```

---

## Bluetooth LE — `generic/bluetooth/*`

Linux-only with optional `bluepy`. Requires appropriate Bluetooth adapter and
permissions.

---

[Wiki hub](../README.md)
