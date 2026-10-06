# Changelog - FirewallXPL-Forge

All notable changes to FirewallXPL-Forge are documented here.

---

## [2.5.1] — 2026-10-06

### Changed
- Release alignment: package version synced to 2.5.1 for GitHub Release + PyPI (HEAD beyond v2.5.0).

## [2.4.0] — 2026-09-26

### Added — Critical CVEs (CVSS 10.0)
- CVE-2026-15409: SonicWall SMA1000 /wsproxy SSRF→Erlang dist→OS cmd chain (CISA KEV)
- CVE-2026-76460: Cisco ISE API authentication bypass (no credentials required)
- CVE-2026-94127: F5 BIG-IP APM pre-authentication RCE (watchTowr Labs PoC)
- CVE-2026-85102: Check Point Security Gateway VPN pre-auth RCE (exploited before advisory)
- CVE-2026-8451: Citrix NetScaler ADC/Gateway pre-auth RCE (watchTowr Labs PoC)

### Added — High CVEs (CVSS 9.8)
- CVE-2026-10520/10523: Ivanti Sentry auth bypass + command injection chain
- CVE-2025-9242: WatchGuard Firebox pre-auth RCE (watchTowr Labs PoC)
- CVE-2026-32746: telnetd stack buffer overflow pre-auth RCE
- CVE-2025-25257: Fortinet FortiWeb pre-auth RCE (watchTowr Labs PoC)
- CVE-2024-47575: FortiJump — Fortinet FortiManager FGFM missing auth → RCE (CISA KEV, Chinese APT)
- CVE-2023-36844: Juniper EX/SRX J-Web PHP env injection + file upload → pre-auth RCE (CISA KEV)
- CVE-2024-4577: PHP CGI argument injection RCE on Windows (CISA KEV)
- CVE-2026-2699: Progress ShareFile pre-auth RCE (watchTowr Labs PoC)
## [2.3.0] — 2026-09-23

### Added — MikroTik RouterOS CVEs
- CVE-2022-45316: DHCPv6 heap overflow RCE (CVSS 9.8)
- CVE-2023-30799: FOISted full chain priv-esc to superadmin (CVSS 9.1)
- CVE-2023-32154: IPv6 Router Advertisement heap overflow, zero-click (CVSS 9.8)
- CVE-2025-2848: IPsec IKE phase-1 command injection (CVSS 9.8)
- CVE-2025-7178: RouterOS API auth bypass (CVSS 9.8)

### Added — FortiSIEM
- CVE-2023-34992: FortiSIEM pre-auth OS command injection (CVSS 10.0, exploited ITW)

### Added — Tier 3 Medium CVEs
- CVE-2024-26010: FortiGate SSL-VPN info disclosure (CVSS 5.3)
- CVE-2023-41843: FortiGate WebUI stored XSS (CVSS 6.4)
- CVE-2023-6789: PAN-OS GlobalProtect XSS (CVSS 6.1)
- CVE-2024-20341: Cisco ASA WebVPN SSRF (CVSS 6.1)
- CVE-2024-24909: Check Point gateway SSRF (CVSS 6.4)
## [2.2.1] — 2026-09-19 (previous release)

## [minor-sync-2026-09-26] - 2026-09-26

### Changed
- EmbedXPL v5.0.0 sync: search engine + autopwn modules deployed
- Domain contracts updated (DOMAIN-CONTRACTS.md)

## [2.2.1] - 2026-06-25

### Added
- Global CLI flags via `tools/xpl_cli.py`: `-h`/`--help`, `-V`/`--version`, `-i`/`--interactive`, `--doctor`/`--check`

---

## [2.1.1] - 2026-06-02

### Added

**PAN-OS GlobalProtect - CVE-2026-0257 (High, CVSS 7.8, CISA KEV 2026-05-29)**
- `exploits/perimeter/paloalto/globalprotect_auth_bypass_cve_2026_0257.py`
  - Full E2E: TLS cert extraction -> RSA-PKCS1v15 cookie forge -> pre-auth VPN bypass
  - CISA KEV deadline: 2026-06-19 | Active exploitation from 2026-05-17
  - Affects PAN-OS 10.2/11.1/11.2/12.1 and Prisma Access (pre-fix versions)

**Fortinet FortiWeb - CVE-2025-25257 (Critical, CVSS 9.8)**
- `exploits/perimeter/fortinet/fortiweb/fortiweb_auth_bypass_rce_cve_2025_25257.py`
  - Authentication bypass in FortiWeb WAF management interface leads to RCE
  - Crafted HTTP headers bypass session validation on the management REST API
  - Post-exploitation: WAF rule enumeration, OS command injection via configuration endpoint
  - Affects FortiWeb 6.4.x < 6.4.4, 7.0.x < 7.0.4, 7.2.x < 7.2.2

**Fortinet FortiWeb - CVE-2025-64446 (Critical, CVSS 9.8)**
- `exploits/perimeter/fortinet/fortiweb/fortiweb_admin_rce_cve_2025_64446.py`
  - OS command injection in FortiWeb admin REST API endpoint
  - Unsanitized `name` parameter passed to internal shell call in admin provisioning
  - Unauthenticated or low-privileged attacker can achieve arbitrary OS command execution
  - Affects FortiWeb 7.2.x < 7.2.5, 7.4.x < 7.4.1

**Aruba ClearPass Policy Manager - CVE-2023-25594 (Critical, CVSS 9.8)**
- `exploits/nac/aruba/clearpass_unauth_rce_cve_2023_25594.py`
  - Unauthenticated RCE via guest provisioning API command injection
  - Pre-auth path injects into internal shell account resolution, executes as root
  - Affects ClearPass 6.10.x < 6.10.8, 6.11.x < 6.11.2

**Nmap NSE Scripts**
- `fxf-firewall-fingerprint.nse`: passive fingerprinting for 11 firewall vendors
- `fxf-globalprotect-detect.nse`: GlobalProtect portal detection
- `fxf-globalprotect-auth-bypass-cve-2026-0257.nse`: passive TLS cert check
- `fxf-fortios-detect.nse`: FortiOS detection
- `fxf-cisco-asa-detect.nse`: Cisco ASA detection
- `nse_installer.py`: cross-platform NSE installer with auto nmap detection

### Changed

- `firewallxpl/modules/exploits/perimeter/fortinet/fortiweb/` created as new sub-namespace
- `pyproject.toml`: version bumped to 2.1.1
- `setup.py`: version bumped to 2.1.1
- `firewallxpl/core/cve/cve_db.py`: CVE-2026-0257 entry added
- `firewallxpl/interpreter.py`: `install-nse` command added

### Documentation

- `docs/wiki/ANEXO-INDICE-MODULOS.md`: regenerated with 172 modules
- `docs/COVERAGE_MATRIX.md` / `COVERAGE_MATRIX.txt`: updated coverage matrix
- `docs/FULL_CATALOG.md` / `FULL_CATALOG.txt`: updated full catalog (172 modules, 77 CVEs)
- All 11 wiki pages rewritten in EN-US and PT-BR with typed parameter tables
- New wiki page 12 in both languages covering NSE installer and scripts
- `README.md` and `README.pt-BR.md`: NSE installer section, CVE-2026-0257 vendor table

**Catalog**
- `cve_extended_catalog.json`: +1 entry (CVE-2026-0257), count 145->146

---
## [2.1.0] - 2026-05-28

### Added

**Fortinet FortiClient EMS - CVE-2026-35616 (Critical, CVSS 9.1)**
- `exploits/perimeter/fortinet/forticlient_ems_preauth_api_bypass_cve_2026_35616.py`
  - Pre-authentication API bypass via HTTP header spoofing in FortiClient EMS 7.4.5-7.4.6
  - Django middleware trusts user-controlled `X-SSL-CLIENT-VERIFY` and `X-SSL-Client-Cert` headers
  - Certificate chain validation uses only DN string matching (no X.509 signature verification)
  - Post-exploitation: managed endpoint enumeration, EKZ-style software update push simulation
  - CISA KEV 2026-04-06; actively exploited by threat cluster delivering EKZ infostealer
  - Fixed in: 7.4.7 / hotfix 7.4.5.2111 or 7.4.6.2170

**Fortinet FortiCloud SSO - CVE-2026-24858 (Critical, CVSS 9.8)**
- `exploits/perimeter/fortinet/forticloud_sso_auth_bypass_cve_2026_24858.py`
  - Cross-tenant SSO authentication bypass in FortiOS, FortiManager, FortiAnalyzer
  - FortiCloud JWT token accepted without org binding, enabling cross-tenant admin access
  - Post-exploitation: FortiOS REST API enumeration (config, admins, SSL-VPN, IPsec, SNMP)
  - Affects FortiOS 7.0.0-7.0.16, 7.2.0-7.2.10, 7.4.0-7.4.4

**FortiOS SSL-VPN Session Reuse - CVE-2024-50562**
- `exploits/perimeter/fortinet/fortios_sslvpn_session_reuse_cve_2024_50562.py`
  - Session cookie reuse after logout; captured SVPNCOOKIE replayed for persistent access
  - Affects FortiOS 7.4.x < 7.4.4, 7.2.x < 7.2.9, 7.0.x < 7.0.16

**Cisco ASA/FTD FIRESTARTER Chain - CVE-2025-20362 + CVE-2025-20333 (Critical, CVSS 9.9)**
- `exploits/perimeter/cisco/cisco_asa_ftd_firestarter_chain_cve_2025_20362_20333.py`
  - Two-stage chain used by UAT4356/ArcaneDoor APT (CISA AR26-113A, ED 25-03)
  - CVE-2025-20362: pre-auth restricted URL bypass in VPN web server (CWE-120)
  - CVE-2025-20333: post-auth RCE as root via crafted HTTPS requests (CWE-862)
  - FIRESTARTER backdoor hooks LINA process; persists post-patch via CSP_MOUNT_LIST
  - Full remediation: hard power cycle + reimaging (firmware update is insufficient)

### Catalog

- `firewallxpl/resources/catalogs/cve_extended_catalog.json`: +5 entries
  - CVE-2026-35616, CVE-2026-24858, CVE-2024-50562, CVE-2025-20362, CVE-2025-20333
  - Count: 140 -> 145 | Updated: 2026-05-28

---

## [2.0.0] - (initial release)

- Initial release with 164 modules covering perimeter, VPN, WAF, LB, NAC, OT/ICS
- 56+ CVEs with Python exploit modules
- 23 vendors: Fortinet, Cisco, Palo Alto, SonicWall, Sophos, Juniper, Check Point,
  Zyxel, pfSense, Barracuda, WatchGuard, F5, Citrix, Ivanti, Pulse Secure, Secomea,
  Siemens, Moxa, Hirschmann, Phoenix Contact, Schneider Electric, Ewon, Imperva
- ML-assisted fingerprinting, GPU acceleration, AutoPwn scanner (T0-T5)
- Rich TUI dashboard, Metasploit bridge integration
- Full bilingual documentation (en-US / pt-BR)
