# Changelog — FirewallXPL-Forge

## [2.4.0] — 2026-09-26

### Added — Critical CVEs (CVSS 10.0)
- CVE-2026-15409: SonicWall SMA1000 /wsproxy SSRF→Erlang dist→OS cmd chain (CISA KEV)
- CVE-2026-76460: Cisco ISE API authentication bypass (no credentials required)
- CVE-2026-94127: F5 BIG-IP APM pre-authentication RCE (watchTowr Labs PoC)
- CVE-2026-85102: Check Point Security Gateway VPN pre-auth RCE (exploited before advisory)
- CVE-2026-8451: Citrix NetScaler ADC/Gateway pre-auth RCE (watchTowr Labs PoC)

## [minor-sync-2026-09-26] - 2026-09-26

### Changed
- EmbedXPL v5.0.0 sync: search engine + autopwn modules deployed
- Domain contracts updated (DOMAIN-CONTRACTS.md)

## [2.2.1] - 2026-06-25

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