# FirewallXPL-Forge — Full Module Catalog

> Generated: 2026-06-02T05:09:41.652128+00:00
> Author: Andre Henrique (@mrhenrike) | Uniao Geek

## Summary

| Category | Modules | Vendor / group buckets |
|---|---:|---:|
| Exploits | 89 | 26 |
| Credential Modules | 28 | 19 |
| Scanners | 3 | 3 |
| Generic Modules | 7 | 5 |
| Encoders | 13 | 3 |
| Payloads | 32 | 9 |
| **Total Modules** | **172** | — |
| Distinct CVEs | 77 | — |

## Program footprint

Approximate on-disk size (file bytes only; binary prefixes). Walk skips caches such as ``__pycache__`` and ``.git``.

| Metric | Value |
|---|---|
| Repository root | `D:/Projetos-SafeLabs/submodules/IoT/FirewallXPL-Forge` |
| Total file bytes | 105.23 MiB |
| Files (repo walk) | 3200 |
| Files under ``firewallxpl/`` | 2168 |

### Largest top-level paths (repository)

| Path | Size | Share of total |
|---|---:|---:|
| `firewallxpl` | 90.82 MiB | 86.3% |
| `build` | 8.36 MiB | 7.9% |
| `docs` | 5.76 MiB | 5.5% |
| `tools` | 188.21 KiB | 0.2% |
| `firewallxpl.egg-info` | 63.18 KiB | 0.1% |
| `(repo root files)` | 56.63 KiB | 0.1% |

### ``firewallxpl/`` breakdown (first-level folders)

| Area | Size | Share of total |
|---|---:|---:|
| `resources` | 90.04 MiB | 85.6% |
| `modules` | 445.81 KiB | 0.4% |
| `core` | 306.84 KiB | 0.3% |
| `(firewallxpl root files)` | 29.32 KiB | 0.0% |
| `libs` | 13.68 KiB | 0.0% |

### ``firewallxpl/resources/*`` (largest direct children)

| Subfolder | Size | Share of total |
|---|---:|---:|
| `mibs` | 85.09 MiB | 80.9% |
| `vendors` | 4.52 MiB | 4.3% |
| `catalogs` | 323.82 KiB | 0.3% |
| `arsenal` | 55.98 KiB | 0.1% |
| `wordlists` | 49.83 KiB | 0.0% |
| `ssh_keys` | 9.89 KiB | 0.0% |
| `ml` | 1.22 KiB | 0.0% |

### First-party Python files (``.py`` count, excluding ``__pycache__``)

| Tree | Files |
|---|---:|
| `firewallxpl/core` | 77 |
| `firewallxpl/modules` | 244 |
| `firewallxpl/libs` | 5 |
| `tools` | 25 |
| `rxf.py` | 0 |

---

## Exploits (89)

### a10 (1)

1. **A10 SoftAX/ACOS Directory Traversal**
   - Path: `exploits/lb/a10/softax_path_traversal.py`
   - Unauthenticated directory traversal in A10 SoftAX / ACOS management interface allows reading files with root privileges.
   - Devices: lb

### aruba (2)

2. **Aruba ClearPass Stored XSS**
   - Path: `exploits/nac/aruba/clearpass_xss_stored.py`
   - Stored XSS in Aruba ClearPass Policy Manager 6.4 login page allows injection into audit/access tracker. Requires prior session.
   - Devices: nac

3. **Aruba ClearPass Unauthenticated RCE (CVE-2023-25594)**
   - Path: `exploits/nac/aruba/clearpass_unauth_rce_cve_2023_25594.py`
   - Unauthenticated remote code execution in Aruba ClearPass Policy Manager REST API. An attacker with network access to the management interface can send a crafted request to the login/guest endpoint to 
   - CVEs: CVE-2023-25594
   - Devices: nac

### barracuda (2)

4. **Barracuda ESG Command Injection (CVE-2023-2868)**
   - Path: `exploits/waf/barracuda/esg_cmd_injection_cve_2023_2868.py`
   - Remote command injection via crafted TAR file in Barracuda ESG appliance versions 5.1.3.001-9.2.0.006. Exploited by state-sponsored UNC4841. FBI recommends full replacement. CVSS 9.4.
   - CVEs: CVE-2023-2868
   - Devices: waf

5. **Barracuda ESG Spreadsheet RCE (CVE-2023-7102)**
   - Path: `exploits/waf/barracuda/esg_spreadsheet_rce_cve_2023_7102.py`
   - RCE via parameter injection in Spreadsheet ParseExcel library. CVSS 9.8.
   - CVEs: CVE-2023-7102
   - Devices: waf

### checkpoint (1)

6. **Check Point Gateway Info Disclosure (CVE-2024-24919)**
   - Path: `exploits/perimeter/checkpoint/gateway_info_disclosure_cve_2024_24919.py`
   - Unauthenticated arbitrary file read via path traversal in /clients/MyCRL. Affects Check Point R77.20 through R81.20.
   - CVEs: CVE-2024-24919
   - Devices: perimeter

### cisco (11)

7. **Cisco ASA/FTD Path Traversal (CVE-2020-3452)**
   - Path: `exploits/perimeter/cisco/asa_ftd_path_traversal_cve_2020_3452.py`
   - Directory traversal in Cisco ASA/FTD WebVPN allows unauthenticated read of web service files via /+CSCOT+/translation-table. Affects ASA 9.6-9.14 and FTD 6.2.3-6.6.0.
   - CVEs: CVE-2020-3452
   - Devices: perimeter

8. **Cisco ASA/FTD VPN Brute-Force (CVE-2023-20269)**
   - Path: `exploits/perimeter/cisco/asa_vpn_bruteforce_cve_2023_20269.py`
   - Unauthorized access vulnerability in Cisco ASA/FTD remote access VPN allows unauthenticated brute-force of VPN credentials without triggering lockout. Actively exploited by Akira/LockBit ransomware.
   - CVEs: CVE-2023-20269
   - Devices: perimeter

9. **Cisco ASA/FTD VPN Server FIRESTARTER Chain (CVE-2025-20362 + CVE-2025-20333)**
   - Path: `exploits/perimeter/cisco/cisco_asa_ftd_firestarter_chain_cve_2025_20362_20333.py`
   - Chained exploitation of two Cisco ASA/FTD VPN web server vulnerabilities used by APT actor UAT4356 (ArcaneDoor/FIRESTARTER campaign, CISA AR26-113A). CVE-2025-20362 (pre-auth buffer overflow/URL bypas
   - CVEs: CVE-2025-20333, CVE-2025-20362
   - Devices: Cisco ASA 9.12 < 9.12.4.72, Cisco ASA 9.14 < 9.14.4.28, Cisco FTD 7.0.x < 7.0.8.1, Cisco FTD 7.1.x-7.2.x < 7.2.9, Cisco FTD 7.3.x-7.4.x < 7.4.2.4

10. **Cisco Firepower Management 6.0 Path Traversal**
   - Path: `exploits/perimeter/cisco/firepower_management60_path_traversal.py`
   - Module exploits Cisco Firepower Management 6.0 Path Traversal vulnerability. If the target is vulnerable, it is possible to retrieve content of the arbitrary files.
   - CVEs: CVE-2016-6435
   - Devices: Cisco Firepower Management Console 6.0

11. **Cisco Firepower Management 6.0 RCE**
   - Path: `exploits/perimeter/cisco/firepower_management60_rce.py`
   - Module exploits Cisco Firepower Management 6.0 Remote Code Execution vulnerability. If the target is vulnerable, it is create backdoor account and authenticate through SSH service.
   - CVEs: CVE-2016-6433
   - Devices: Cisco Firepower Management Console 6.0

12. **Cisco IOS XE Web UI Privilege Escalation (CVE-2023-20198)**
   - Path: `exploits/perimeter/cisco/ios_xe_webui_privesc_cve_2023_20198.py`
   - Privilege escalation in IOS XE Web UI allows unauth admin creation. CVSS 10.0.
   - CVEs: CVE-2023-20198
   - Devices: perimeter

13. **Cisco ISA-3000/ASA Double Free RCE (CVE-2018-0101)**
   - Path: `exploits/perimeter/cisco/isa3000_asa_rce_cve_2018_0101.py`
   - Double free in Cisco ASA/ISA-3000 XML parser allows unauth RCE. CVSS 10.0. 55+ PoCs on GitHub.
   - CVEs: CVE-2018-0101
   - Devices: perimeter

14. **Cisco Secure ACS Unauthorized Password Change**
   - Path: `exploits/nac/cisco/secure_acs_bypass.py`
   - Module exploits an authentication bypass issue which allows arbitrary password change requests to be issued for any user in the local store. Instances of Secure ACS running version 5.1 with patches 3,
   - Devices: Cisco Secure ACS version 5.1 with patch 3, 4, or 5 installed and without patch 6 or later installed, Cisco Secure ACS version 5.2 without any patches installed, Cisco Secure ACS version 5.2 with patch 1 or 2 installed and without patch 3 or later installed

15. **Cisco UCM Info Disclosure**
   - Path: `exploits/perimeter/cisco/ucm_info_disclosure.py`
   - Module exploits information disclosure vulnerability in Cisco UCM devices. If the target is vulnerable it is possible to read sensitive information through TFTP service.
   - CVEs: CVE-2013-7030
   - Devices: Cisco UCM

16. **Cisco UCS Manager RCE**
   - Path: `exploits/perimeter/cisco/ucs_manager_rce.py`
   - Module exploits Cisco UCS Manager 2.1 (1b) Remote Code Execution vulnerability which allows executing commands on operating system level.
   - Devices: Cisco UCS Manager 2.1 (1b)

17. **Cisco Unified Multi Path Traversal**
   - Path: `exploits/perimeter/cisco/unified_multi_path_traversal.py`
   - Module exploits path traversal vulnerability in Cisco Unified Communications Manager, Cisco Unified Contact Center Express and Cisco Unified IP Interactive Voice Response devices.If the target is vuln
   - CVEs: CVE-2011-3315
   - Devices: Cisco Unified Communications Manager 5.x, Cisco Unified Communications Manager 6.x < 6.1(5), Cisco Unified Communications Manager 7.x < 7.1(5b), Cisco Unified Communications Manager 8.x < 8.0(3), Cisco Unified Contact Center Express, Cisco Unified IP Interactive Voice Response < 6.0(1), Cisco Unified IP Interactive Voice Response 7.0(x) < 7.0(2), Cisco Unified IP Interactive Voice Response 8.0(x) < 8.5(1)

### citrix (3)

18. **Citrix ADC/Gateway RCE (CVE-2019-19781)**
   - Path: `exploits/vpn/citrix/adc_rce_cve_2019_19781.py`
   - Directory traversal in Citrix ADC (NetScaler) allows unauthenticated remote code execution via template injection through /vpn/../vpns/portal/scripts/newbm.pl. Affects Citrix ADC and Gateway 10.5, 11.
   - CVEs: CVE-2019-19781
   - Devices: vpn

19. **NetScaler ADC Gateway Unauth RCE (CVE-2023-3519)**
   - Path: `exploits/vpn/citrix/netscaler_rce_cve_2023_3519.py`
   - Unauth RCE in NetScaler when configured as Gateway or AAA vserver. CVSS 9.8.
   - CVEs: CVE-2023-3519
   - Devices: vpn

20. **NetScaler CitrixBleed Session Leak (CVE-2023-4966)**
   - Path: `exploits/vpn/citrix/netscaler_citrixbleed_cve_2023_4966.py`
   - Buffer overflow leaks session tokens (CitrixBleed). CVSS 9.4.
   - CVEs: CVE-2023-4966
   - Devices: vpn

### ewon (1)

21. **Ewon Cosy+ Unauth RCE (CVE-2026-25823)**
   - Path: `exploits/vpn/ewon/cosy_unauth_rce_cve_2026_25823.py`
   - Unauthenticated RCE in Ewon/HMS Cosy+ industrial VPN gateway. CVSS 9.8.
   - CVEs: CVE-2026-25823
   - Devices: vpn

### f5 (5)

22. **F5 BIG-IP APM Buffer Overflow RCE (CVE-2025-53521)**
   - Path: `exploits/lb/f5/bigip_apm_buffer_overflow_cve_2025_53521.py`
   - Stack buffer overflow in BIG-IP APM virtual server. Pre-auth RCE. CVSS 9.8.
   - CVEs: CVE-2025-53521
   - Devices: lb

23. **F5 BIG-IP Config Utility RCE (CVE-2023-46747)**
   - Path: `exploits/lb/f5/bigip_config_rce_cve_2023_46747.py`
   - Unauthenticated RCE via request smuggling in BIG-IP Configuration Utility (TMUI). Bypasses authentication to execute system commands. CVSS 9.8. Affects BIG-IP 13.x-17.x.
   - CVEs: CVE-2023-46747
   - Devices: lb

24. **F5 BIG-IP TMUI LFI (CVE-2020-5902)**
   - Path: `exploits/lb/f5/bigip_tmui_lfi_cve_2020_5902.py`
   - Local file inclusion via TMUI path traversal allows unauthenticated read of /etc/passwd, admin credentials, license and other files. Affects BIG-IP <= 13.1.3.
   - CVEs: CVE-2020-5902
   - Devices: lb

25. **F5 BIG-IP iControl REST Auth Bypass (CVE-2022-1388)**
   - Path: `exploits/lb/f5/bigip_icontrol_auth_bypass_cve_2022_1388.py`
   - Authentication bypass in iControl REST allows unauthenticated command execution via /mgmt/tm/util/bash with crafted headers. Affects BIG-IP 11.6.x through 16.1.x.
   - CVEs: CVE-2022-1388
   - Devices: lb

26. **F5 BIG-IP iControl REST RCE (CVE-2021-22986)**
   - Path: `exploits/lb/f5/bigip_icontrol_rest_rce_cve_2021_22986.py`
   - Unauthenticated remote command execution via iControl REST /mgmt/tm/util/bash. Affects BIG-IP 16.0.x before 16.0.1.1.
   - CVEs: CVE-2021-22986
   - Devices: lb

### fortinet (14)

27. **FortiClient EMS Pre-Auth API Bypass + Post-Exploitation (CVE-2026-35616)**
   - Path: `exploits/perimeter/fortinet/forticlient_ems_preauth_api_bypass_cve_2026_35616.py`
   - Critical (CVSS 9.1) pre-authentication bypass in Fortinet FortiClient EMS 7.4.5-7.4.6. Generates a real X.509 certificate with Fortinet CA DN strings and injects it via X-SSL-CLIENT-VERIFY header spoo
   - CVEs: CVE-2026-35616
   - Devices: Fortinet FortiClient EMS 7.4.5, Fortinet FortiClient EMS 7.4.6

28. **FortiClientEMS SQL Injection RCE (CVE-2023-48788)**
   - Path: `exploits/perimeter/fortinet/forticlientems_sqli_rce_cve_2023_48788.py`
   - SQL injection in FortiClientEMS DAS allows unauth code execution. CVSS 9.8.
   - CVEs: CVE-2023-48788
   - Devices: perimeter

29. **FortiCloud SSO Authentication Bypass & Post-Exploitation (CVE-2026-24858)**
   - Path: `exploits/perimeter/fortinet/forticloud_sso_auth_bypass_cve_2026_24858.py`
   - Critical (CVSS 9.8) cross-tenant FortiCloud SSO auth bypass in FortiOS/FortiManager/FortiAnalyzer. Attacker JWT token replayed to SSO callback grants admin session on any device registered to a differ
   - CVEs: CVE-2026-24858
   - Devices: FortiOS 7.0.0-7.0.16, FortiOS 7.2.0-7.2.10, FortiOS 7.4.0-7.4.4, FortiManager 7.0.x / 7.2.x / 7.4.x, FortiAnalyzer 7.0.x / 7.2.x / 7.4.x

30. **FortiGate OS 4.x-5.0.7 Backdoor**
   - Path: `exploits/perimeter/fortinet/fortigate_os_backdoor.py`
   - SSH misuse / Fortimanager_Access interactive auth against legacy FortiGate OS 4.x–5.0.7 (historical administrative channel; not FortiOS 7 SSL-VPN CVE class).
   - CVEs: CVE-2014-3413
   - Devices: FortiGate OS Version 4.x-5.0.7

31. **FortiManager FortiJump RCE (CVE-2024-47575)**
   - Path: `exploits/perimeter/fortinet/fortimanager_fortijump_cve_2024_47575.py`
   - Missing authentication for critical function in FortiManager fgfmd daemon allows unauthenticated RCE via crafted requests. CVSS 9.8. Known as 'FortiJump'. Affects FortiManager 6.2-7.6.0.
   - CVEs: CVE-2024-47575
   - Devices: perimeter

32. **FortiOS Auth Bypass via REST API (CVE-2022-40684)**
   - Path: `exploits/perimeter/fortinet/fortios_auth_bypass_cve_2022_40684.py`
   - Authentication bypass using crafted Forwarded/X-Forwarded-Vdom headers allows unauthenticated access to /api/v2/cmdb/system/admin on FortiOS 7.0.0-7.0.6, 7.2.0-7.2.1, FortiProxy 7.0.x-7.2.0, FortiSwit
   - CVEs: CVE-2022-40684
   - Devices: perimeter

33. **FortiOS SSL-VPN Heap Overflow RCE (CVE-2022-42475)**
   - Path: `exploits/perimeter/fortinet/fortios_sslvpn_heap_rce_cve_2022_42475.py`
   - Heap-based buffer overflow in FortiOS sslvpnd allows pre-auth RCE. CVSS 9.8.
   - CVEs: CVE-2022-42475
   - Devices: perimeter

34. **FortiOS SSL-VPN OOB Write RCE (CVE-2024-21762)**
   - Path: `exploits/perimeter/fortinet/fortios_sslvpn_rce_cve_2024_21762.py`
   - Pre-authentication out-of-bounds write in FortiOS SSL-VPN daemon allows RCE via crafted HTTP requests. CVSS 9.6. Affects FortiOS 6.0 through 7.4.2. 14,700+ devices compromised.
   - CVEs: CVE-2024-21762
   - Devices: perimeter

35. **FortiOS SSL-VPN Path Traversal (CVE-2018-13379)**
   - Path: `exploits/perimeter/fortinet/fortios_sslvpn_path_traversal_cve_2018_13379.py`
   - Path traversal via /remote/fgt_lang allows unauthenticated read of sslvpn_websession, leaking plaintext VPN credentials. Affects FortiOS 5.6.3-5.6.7 and 6.0.0-6.0.4.
   - CVEs: CVE-2018-13379
   - Devices: perimeter

36. **FortiOS SSL-VPN Pre-Auth RCE XORtigate (CVE-2023-27997)**
   - Path: `exploits/perimeter/fortinet/fortios_sslvpn_preauth_rce_cve_2023_27997.py`
   - Pre-auth heap overflow in FortiOS SSL-VPN (XORtigate). CVSS 9.8.
   - CVEs: CVE-2023-27997
   - Devices: perimeter

37. **FortiOS SSL-VPN Session Cookie Reuse after Logout (CVE-2024-50562)**
   - Path: `exploits/perimeter/fortinet/fortios_sslvpn_session_reuse_cve_2024_50562.py`
   - After a user logs out of the FortiOS SSL-VPN portal the server-side session is not properly invalidated. A captured session cookie can be replayed to regain authenticated portal access. Affects FortiO
   - CVEs: CVE-2024-50562
   - Devices: perimeter

38. **FortiOS WebSocket Auth Bypass (CVE-2024-55591)**
   - Path: `exploits/perimeter/fortinet/fortios_websocket_auth_bypass_cve_2024_55591.py`
   - Auth bypass via Node.js WebSocket in FortiOS grants super-admin. CVSS 9.8.
   - CVEs: CVE-2024-55591
   - Devices: perimeter

39. **FortiWeb Admin REST API Command Injection (CVE-2025-64446)**
   - Path: `exploits/perimeter/fortinet/fortiweb/fortiweb_admin_rce_cve_2025_64446.py`
   - Command injection in Fortinet FortiWeb admin REST API endpoint allows an attacker to execute arbitrary OS commands. The vulnerable parameter in the admin API is not sanitized before being passed to a 
   - CVEs: CVE-2025-64446
   - Devices: perimeter, waf

40. **FortiWeb Auth Bypass to RCE (CVE-2025-25257)**
   - Path: `exploits/perimeter/fortinet/fortiweb/fortiweb_auth_bypass_rce_cve_2025_25257.py`
   - Authentication bypass in Fortinet FortiWeb WAF management interface allows an unauthenticated attacker to access the management API and achieve RCE via configuration injection. Affects FortiWeb 6.4.x 
   - CVEs: CVE-2025-25257
   - Devices: perimeter, waf

### generic (11)

41. **DNP3 Firewall Evasion (N/A)**
   - Path: `exploits/perimeter/generic/dnp3_firewall_evasion.py`
   - DNP3 protocol evasion techniques for industrial firewall bypass. Fragment reassembly attacks, unsolicited response injection.
   - Devices: perimeter

42. **EtherNet/IP CIP Firewall Bypass (N/A)**
   - Path: `exploits/perimeter/generic/ethernetip_cip_bypass.py`
   - EtherNet/IP Common Industrial Protocol bypass via encapsulation manipulation. Affects Rockwell/Allen-Bradley environments.
   - Devices: perimeter

43. **HTTP Form Char-by-Char Oracle**
   - Path: `exploits/perimeter/generic/http_form_char_by_char_oracle.py`
   - Generic framework for character-by-character password probing when the login page leaks a content or timing oracle. Not bound to a specific vendor/model/year in the market-priority catalog — you must 
   - Devices: Any in-scope device with a vulnerable web login oracle (lab-validated only)

44. **HTTP Request Smuggling Checker**
   - Path: `exploits/perimeter/generic/http_smuggling_checker.py`
   - Tests for HTTP request smuggling vectors (CL.TE, TE.CL) that can bypass firewall/WAF inspection and access controls. Applicable to any device with HTTP-based management or proxy.
   - Devices: perimeter

45. **IEC 60870-5-104 Protocol Manipulation (N/A)**
   - Path: `exploits/perimeter/generic/iec104_manipulation.py`
   - IEC 104 SCADA protocol manipulation to bypass industrial firewall rules. ASDU type confusion, cause-of-transmission spoofing.
   - Devices: perimeter

46. **Modbus TCP Deep Packet Inspection Bypass (N/A)**
   - Path: `exploits/perimeter/generic/modbus_dpi_bypass.py`
   - Techniques to bypass Modbus TCP DPI in industrial firewalls via fragmentation, function code manipulation, and timing evasion.
   - Devices: perimeter

47. **Multi SSH Authorized Keys**
   - Path: `exploits/perimeter/generic/ssh_auth_keys.py`
   - Module exploits private key exposure vulnerability. If the target is vulnerable it is possible to authentiate to the device.
   - Devices: ExaGrid firmware < 4.8 P26, Quantum DXi V1000, Array Networks vxAG 9.2.0.34 and vAPV 8.3.2.17 appliances, Barracuda Load Balancer, Ceragon FibeAir IP-10, F5 BigIP, Loadbalancer.org Enterprise VA 7.5.2, Digital Alert Systems DASDEC and Monroe Electronics One-Net E189 Emergency Alert System

48. **OPC UA Firewall Bypass (N/A)**
   - Path: `exploits/perimeter/generic/opcua_firewall_bypass.py`
   - OPC UA protocol manipulation to bypass industrial firewall inspection. Uses chunking, security policy downgrade, and endpoint manipulation.
   - Devices: perimeter

49. **OpenSSL Heartbleed**
   - Path: `exploits/perimeter/generic/heartbleed.py`
   - Exploits OpenSSL Heartbleed vulnerability. Vulnerability exists in the handling of heartbeat requests, where fake length can be used to leak memory data in the response. This module is heavily based o
   - Devices: Multi

50. **Shellshock**
   - Path: `exploits/perimeter/generic/shellshock.py`
   - Exploits shellshock vulnerability that allows executing commands on operating system level.
   - CVEs: CVE-2014-6271, CVE-2014-6278, CVE-2014-7169
   - Devices: Multi

51. **VLAN Hopping / 802.1Q Checker**
   - Path: `exploits/nac/generic/vlan_hopping_checker.py`
   - Checks for VLAN hopping susceptibility via DTP negotiation, double-tagging, and 802.1Q tag injection. Tests NAC bypass via MAC spoofing and unauthorized VLAN access.
   - Devices: nac

### hirschmann (1)

52. **Hirschmann EAGLE20/30 Auth Bypass (CVE-2020-6994)**
   - Path: `exploits/perimeter/hirschmann/eagle_auth_bypass_cve_2020_6994.py`
   - Use of hard-coded credentials in Hirschmann EAGLE20/30 industrial firewall. CVSS 9.8.
   - CVEs: CVE-2020-6994
   - Devices: perimeter

### imperva (1)

53. **Imperva SecureSphere MX Blind SQLi**
   - Path: `exploits/waf/imperva/securesphere_sqli_cve_2013_xxxx.py`
   - Blind SQL injection in Imperva SecureSphere WAF management console (MX) allows extraction of admin password hashes. Affects SecureSphere 9.5.6 and similar versions.
   - Devices: waf

### ivanti (2)

54. **Ivanti Connect Secure Auth Bypass + RCE (CVE-2023-46805 + CVE-2024-21887)**
   - Path: `exploits/vpn/ivanti/connect_secure_auth_rce_cve_2023_46805.py`
   - Auth bypass via /api/v1/totp/user-backup-code chains with command injection in /api/v1/license/keys-status for unauthenticated RCE. Affects ICS 9.x-22.x, IPS 9.x-22.x. 1,700+ devices compromised.
   - CVEs: CVE-2023-46805, CVE-2024-21887
   - Devices: vpn

55. **Ivanti Connect Secure Buffer Overflow RCE (CVE-2025-0282)**
   - Path: `exploits/vpn/ivanti/ics_buffer_overflow_rce_cve_2025_0282.py`
   - Stack buffer overflow in ICS allows pre-auth RCE. CVSS 9.0.
   - CVEs: CVE-2025-0282
   - Devices: vpn

### juniper (2)

56. **Juniper J-Web OOB Write RCE (CVE-2024-21591)**
   - Path: `exploits/perimeter/juniper/jweb_oob_write_rce_cve_2024_21591.py`
   - Out-of-bounds write in J-Web allows pre-auth RCE. CVSS 9.8. SRX and EX series.
   - CVEs: CVE-2024-21591
   - Devices: perimeter

57. **Juniper J-Web PHP RCE (CVE-2023-36845)**
   - Path: `exploits/perimeter/juniper/jweb_php_rce_cve_2023_36845.py`
   - Unauthenticated RCE via PHP environment variable injection (PHPRC) in J-Web on Juniper SRX and EX series. Allows execution of arbitrary PHP code including phpinfo() and system commands.
   - CVEs: CVE-2023-36845
   - Devices: perimeter

### moxa (2)

58. **Moxa EDR Series Command Injection (CVE-2024-9138)**
   - Path: `exploits/perimeter/moxa/edr_cmd_injection_cve_2024_9138.py`
   - OS command injection in Moxa EDR industrial router/firewall. CVSS 9.8.
   - CVEs: CVE-2024-9138
   - Devices: perimeter

59. **Moxa EDR-G Series Hardcoded JWT (CVE-2024-9137)**
   - Path: `exploits/perimeter/moxa/edr_g_jwt_hardcoded_cve_2024_9137.py`
   - Hardcoded JWT secret in Moxa EDR-G9010/G9004 allows admin access. CVSS 9.9.
   - CVEs: CVE-2024-9137
   - Devices: perimeter

### paloalto (6)

60. **PAN-OS Auth Bypass (CVE-2025-0108)**
   - Path: `exploits/perimeter/paloalto/panos_auth_bypass_cve_2025_0108.py`
   - Auth bypass in PAN-OS management web interface. CVSS 9.1. Actively exploited.
   - CVEs: CVE-2025-0108
   - Devices: perimeter

61. **PAN-OS GlobalProtect Auth Override Cookie Bypass (CVE-2026-0257)**
   - Path: `exploits/perimeter/paloalto/globalprotect_auth_bypass_cve_2026_0257.py`
   - CVSS 7.8 HIGH. Authentication override cookies in GlobalProtect are encrypted with RSA-PKCS1v15 using a certificate whose public key is exposed via the device's public HTTPS TLS handshake. gpsvc perfo
   - CVEs: CVE-2026-0257
   - Devices: Palo Alto Networks PAN-OS 10.2.x (pre-fix), Palo Alto Networks PAN-OS 11.1.x (pre-fix), Palo Alto Networks PAN-OS 11.2.x (pre-fix), Palo Alto Networks PAN-OS 12.1.x (pre-fix), Prisma Access 10.2.x / 11.2.x (pre-fix)

62. **PAN-OS GlobalProtect Command Injection (CVE-2024-3400)**
   - Path: `exploits/perimeter/paloalto/globalprotect_cmd_injection_cve_2024_3400.py`
   - Unauthenticated command injection in GlobalProtect via crafted SESSID cookie path traversal. Affects PAN-OS 10.2, 11.0, 11.1 with GlobalProtect gateway enabled.
   - CVEs: CVE-2024-3400
   - Devices: perimeter

63. **PAN-OS Management Auth Bypass (CVE-2024-0012)**
   - Path: `exploits/perimeter/paloalto/panos_mgmt_auth_bypass_cve_2024_0012.py`
   - Authentication bypass in PAN-OS management web interface via X-PAN-AUTHCHECK: off header. Chains with CVE-2024-9474 for privilege escalation to root. CVSS 9.3.
   - CVEs: CVE-2024-0012, CVE-2024-9474
   - Devices: perimeter

64. **PAN-OS Privilege Escalation (CVE-2024-9474)**
   - Path: `exploits/perimeter/paloalto/panos_privesc_cve_2024_9474.py`
   - OS command injection in PAN-OS management escalates to root. Chains with CVE-2024-0012.
   - CVEs: CVE-2024-0012, CVE-2024-9474
   - Devices: perimeter

65. **PAN-OS SAML Auth Bypass (CVE-2020-2021)**
   - Path: `exploits/perimeter/paloalto/panos_saml_auth_bypass_cve_2020_2021.py`
   - SAML auth bypass in PAN-OS when Validate IdP Certificate disabled. CVSS 10.0.
   - CVEs: CVE-2020-2021
   - Devices: perimeter

### pfsense (3)

66. **pfSense Anti-Brute-Force Bypass (CVE-2023-27100)**
   - Path: `exploits/perimeter/pfsense/antibruteforce_bypass_cve_2023_27100.py`
   - Bypasses anti-brute-force protection in pfSense CE, enabling unlimited authentication attempts. Affects pfSenseCE versions before 2.7.0.
   - CVEs: CVE-2023-27100
   - Devices: perimeter

67. **pfSense Interfaces Command Injection (CVE-2023-42326)**
   - Path: `exploits/perimeter/pfsense/interfaces_cmd_injection_cve_2023_42326.py`
   - Command injection in pfSense interfaces_gif_edit.php and interfaces_gre_edit.php allows authenticated OS command execution. CVSS 8.8. Affects pfSense CE before 2.7.1.
   - CVEs: CVE-2023-42326
   - Devices: perimeter

68. **pfSense pfBlockerNG Unauth RCE (CVE-2022-31814)**
   - Path: `exploits/perimeter/pfsense/pfblockerng_rce_cve_2022_31814.py`
   - OS command injection in pfBlockerNG via HTTP Host header. Unauth RCE. CVSS 9.8.
   - CVEs: CVE-2022-31814
   - Devices: perimeter

### phoenix (1)

69. **Phoenix Contact mGuard Command Injection (CVE-2024-43386)**
   - Path: `exploits/perimeter/phoenix/mguard_cmd_injection_cve_2024_43386.py`
   - OS command injection in Phoenix Contact FL MGUARD firewall via web interface. CVSS 8.8.
   - CVEs: CVE-2024-43386
   - Devices: perimeter

### pulsesecure (1)

70. **Pulse Secure SSL VPN Arbitrary File Read (CVE-2019-11510)**
   - Path: `exploits/vpn/pulsesecure/sslvpn_arbitrary_file_read_cve_2019_11510.py`
   - Pre-auth arbitrary file read in Pulse Connect Secure 8.1-8.3 via crafted URI allows reading /etc/passwd, session files, and plaintext VPN credentials.
   - CVEs: CVE-2019-11510
   - Devices: vpn

### schneider (1)

71. **Schneider ConneXium/Tofino SSH Hardcoded Credentials (CVE-2017-6026)**
   - Path: `exploits/perimeter/schneider/connexium_ssh_hardcoded_cve_2017_6026.py`
   - Hard-coded SSH keys in Schneider ConneXium Tofino industrial firewall. CVSS 9.8.
   - CVEs: CVE-2017-6026
   - Devices: perimeter

### secomea (1)

72. **Secomea GateManager Unauth RCE (CVE-2020-14500)**
   - Path: `exploits/vpn/secomea/gatemanager_rce_cve_2020_14500.py`
   - Critical vulnerability in Secomea GateManager OT remote access allows unauth RCE. CVSS 10.0.
   - CVEs: CVE-2020-14500
   - Devices: vpn

### siemens (3)

73. **Siemens RUGGEDCOM ROX Web RCE (CVE-2023-24845)**
   - Path: `exploits/perimeter/siemens/ruggedcom_web_rce_cve_2023_24845.py`
   - Command injection in RUGGEDCOM ROX web interface allows authenticated RCE. CVSS 9.1.
   - CVEs: CVE-2023-24845
   - Devices: perimeter

74. **Siemens SCALANCE Command Injection (CVE-2023-44373)**
   - Path: `exploits/perimeter/siemens/scalance_cmd_injection_cve_2023_44373.py`
   - OS command injection in SCALANCE S/SC/W products via crafted HTTP requests. CVSS 9.1. Affects industrial firewalls/switches.
   - CVEs: CVE-2023-44373
   - Devices: perimeter

75. **Siemens SINEMA Remote Connect Path Traversal (CVE-2022-32257)**
   - Path: `exploits/perimeter/siemens/sinema_rc_path_traversal_cve_2022_32257.py`
   - Path traversal in SINEMA Remote Connect Server allows unauth file access. CVSS 9.8.
   - CVEs: CVE-2022-32257
   - Devices: perimeter

### sonicwall (6)

76. **SonicWall SMA Password Reset (CVE-2021-20034)**
   - Path: `exploits/perimeter/sonicwall/sma_password_reset_cve_2021_20034.py`
   - Unauthenticated path traversal in SonicWall SMA 100 series allows deleting the persistent DB, forcing admin password reset. Affects SMA 200/210/400/410/500v.
   - CVEs: CVE-2021-20034
   - Devices: perimeter

77. **SonicWall SMA100 SQL Injection (CVE-2021-20016)**
   - Path: `exploits/perimeter/sonicwall/sma100_sqli_cve_2021_20016.py`
   - SQL injection in SMA100 SSLVPN extracts credentials. CVSS 9.8.
   - CVEs: CVE-2021-20016
   - Devices: perimeter

78. **SonicWall SSL-VPN Shellshock RCE (VisualDoor)**
   - Path: `exploits/perimeter/sonicwall/sslvpn_shellshock_rce_visualdoor.py`
   - Unauthenticated RCE via Shellshock in SonicWall SSL-VPN cgi-bin/jarrewrite.sh. Affects SMA versions < 8.0.0.4.
   - CVEs: CVE-2014-6271
   - Devices: perimeter

79. **SonicWall SSLVPN Auth Bypass (CVE-2024-53704)**
   - Path: `exploits/perimeter/sonicwall/sonicos_sslvpn_auth_bypass_cve_2024_53704.py`
   - Auth bypass in SonicOS SSLVPN allows session hijacking. CVSS 9.8.
   - CVEs: CVE-2024-53704
   - Devices: perimeter

80. **SonicWall SonicOS SSLVPN Access Control (CVE-2024-40766)**
   - Path: `exploits/perimeter/sonicwall/sonicos_sslvpn_access_cve_2024_40766.py`
   - Improper access control in SonicOS SSLVPN allows unauthenticated access to resources and potential firewall crash. CVSS 9.3. Actively exploited by Akira/Black Basta/Fog ransomware.
   - CVEs: CVE-2024-40766
   - Devices: perimeter

81. **SonicWall SonicOS VPN Buffer Overflow (CVE-2020-5135)**
   - Path: `exploits/perimeter/sonicwall/sonicos_vpn_buffer_overflow_cve_2020_5135.py`
   - Stack buffer overflow in SonicOS VPN Portal. Pre-auth RCE. CVSS 9.8.
   - CVEs: CVE-2020-5135
   - Devices: perimeter

### sophos (3)

82. **Sophos Firewall Code Injection (CVE-2022-3236)**
   - Path: `exploits/perimeter/sophos/firewall_code_injection_cve_2022_3236.py`
   - Code injection in Sophos Firewall User Portal. Pre-auth RCE. CVSS 9.8.
   - CVEs: CVE-2022-3236
   - Devices: perimeter

83. **Sophos XG Firewall Auth Bypass (CVE-2022-1040)**
   - Path: `exploits/perimeter/sophos/xg_auth_bypass_cve_2022_1040.py`
   - Authentication bypass in Sophos Firewall User Portal and Webadmin allows unauthenticated access to management. Affects SFOS <= v18.5 MR3.
   - CVEs: CVE-2022-1040
   - Devices: perimeter

84. **Sophos XG SQLi RCE Asnarok (CVE-2020-12271)**
   - Path: `exploits/perimeter/sophos/xg_sqli_asnarok_cve_2020_12271.py`
   - SQL injection in Sophos XG User Portal allows pre-auth RCE. CVSS 9.8.
   - CVEs: CVE-2020-12271
   - Devices: perimeter

### watchguard (2)

85. **WatchGuard Cyclops Blink Priv Esc (CVE-2022-23176)**
   - Path: `exploits/perimeter/watchguard/firebox_cyclops_blink_cve_2022_23176.py`
   - Privilege escalation exploited by Sandworm GRU (Cyclops Blink). CVSS 8.8.
   - CVEs: CVE-2022-23176
   - Devices: perimeter

86. **Watchguard XCS Remote Command Execution**
   - Path: `exploits/perimeter/watchguard/xcs_9_rce.py`
   - This module exploits two separate vulnerabilities found in the Watchguard XCS virtualappliance to gain command execution. By exploiting an unauthenticated SQL injection, a remote attacker may insert a
   - Devices: Watchguard XCS 9.2/10.0

### zyxel (3)

87. **Zyxel ATP USG Buffer Overflow (CVE-2023-33009)**
   - Path: `exploits/perimeter/zyxel/buffer_overflow_cve_2023_33009.py`
   - Buffer overflow in notification function. Pre-auth RCE. CVSS 9.8.
   - CVEs: CVE-2023-33009
   - Devices: perimeter

88. **Zyxel IKE Command Injection (CVE-2023-28771)**
   - Path: `exploits/perimeter/zyxel/ike_cmd_injection_cve_2023_28771.py`
   - OS command injection via IKE packet decoder. Pre-auth RCE. CVSS 9.8. Mirai botnet.
   - CVEs: CVE-2023-28771
   - Devices: perimeter

89. **Zyxel USG FLEX/ATP Command Injection (CVE-2022-30525)**
   - Path: `exploits/perimeter/zyxel/usg_flex_cmd_injection_cve_2022_30525.py`
   - Unauthenticated OS command injection in Zyxel USG FLEX 100(W)/200/500/700 and ATP series via ZTP interface. Affects ZLD 5.00-5.21 Patch 1.
   - CVEs: CVE-2022-30525
   - Devices: perimeter

## Credential Modules (28)

### cisco (3)

1. **Cisco Router Default FTP Creds**
   - Path: `creds/perimeter/cisco/ftp_default_creds.py`
   - Module performs dictionary attack against Cisco Router FTP service. If valid credentials are found, they are displayed to the user.
   - Devices: Cisco Router

2. **Cisco Router Default SSH Creds**
   - Path: `creds/perimeter/cisco/ssh_default_creds.py`
   - Module performs dictionary attack against Cisco Router SSH service. If valid credentials are found, they are displayed to the user.
   - Devices: Cisco Router

3. **Cisco Router Default Telnet Creds**
   - Path: `creds/perimeter/cisco/telnet_default_creds.py`
   - Module performs dictionary attack against Cisco Router Telnet service. If valid credentials are found, they are displayed to the user.
   - Devices: Cisco Router

### fortinet (3)

4. **Fortinet Router Default FTP Creds**
   - Path: `creds/perimeter/fortinet/ftp_default_creds.py`
   - Module performs dictionary attack against Fortinet Router FTP service. If valid credentials are found, they are displayed to the user.
   - Devices: Fortinet Router

5. **Fortinet Router Default SSH Creds**
   - Path: `creds/perimeter/fortinet/ssh_default_creds.py`
   - Module performs dictionary attack against Fortinet Router SSH service. If valid credentials are found, they are displayed to the user.
   - Devices: Fortinet Router

6. **Fortinet Router Default Telnet Creds**
   - Path: `creds/perimeter/fortinet/telnet_default_creds.py`
   - Module performs dictionary attack against Fortinet Router Telnet service. If valid credentials are found, they are displayed to the user.
   - Devices: Fortinet Router

### ftp_bruteforce.py (1)

7. **FTP Bruteforce**
   - Path: `creds/generic/ftp_bruteforce.py`
   - Module performs bruteforce attack against FTP service.If valid credentials are found, the are displayed to the user.
   - Devices: Multiple devices

### ftp_default.py (1)

8. **FTP Default Creds**
   - Path: `creds/generic/ftp_default.py`
   - Module performs dictionary attack with default credentials against FTP service.If valid credentials are found, the are displayed to the user.
   - Devices: Multiple devices

### http_basic_digest_bruteforce.py (1)

9. **HTTP Basic/Digest Bruteforce**
   - Path: `creds/generic/http_basic_digest_bruteforce.py`
   - Module performs bruteforce attack against HTTP Basic/Digest Auth service. If valid credentials are found, they are displayed to the user.
   - Devices: Multiple devices

### http_basic_digest_default.py (1)

10. **HTTP Basic/Digest Default Creds**
   - Path: `creds/generic/http_basic_digest_default.py`
   - Module performs dictionary attack with default credentials against HTTP Basic/Digest Auth service. If valid credentials are found, they are displayed to the user.
   - Devices: Multiple devices

### http_multi_auth_default.py (1)

11. **HTTP/HTTPS Multi-Auth Default Creds**
   - Path: `creds/generic/http_multi_auth_default.py`
   - Module validates multiple HTTP auth methods (basic, digest, bearer, custom headers, form).
   - Devices: Routers, Switches, TAPs, FW, NGFW

### http_web_form_bruteforce.py (1)

12. **HTTP Web Form Bruteforce (Hydra-style)**
   - Path: `creds/generic/http_web_form_bruteforce.py`
   - Dictionary attack against HTTP/HTTPS login forms. Set failure/success body substrings, status codes, or Location fragments—similar to Hydra/JtR web modules. Respect rate limits and authorization; for 
   - Devices: Routers, Switches, Gateways, CPE

### ipfire (3)

13. **IPFire Router Default FTP Creds**
   - Path: `creds/perimeter/ipfire/ftp_default_creds.py`
   - Module performs dictionary attack against IPFire Router FTP service. If valid credentials are found, they are displayed to the user.
   - Devices: IPFire Router

14. **IPFire Router Default SSH Creds**
   - Path: `creds/perimeter/ipfire/ssh_default_creds.py`
   - Module performs dictionary attack against IPFire Router SSH service. If valid credentials are found, they are displayed to the user.
   - Devices: IPFire Router

15. **IPFire Router Default Telnet Creds**
   - Path: `creds/perimeter/ipfire/telnet_default_creds.py`
   - Module performs dictionary attack against IPFire Router Telnet service. If valid credentials are found, they are displayed to the user.
   - Devices: IPFire Router

### juniper (3)

16. **Juniper Router Default FTP Creds**
   - Path: `creds/perimeter/juniper/ftp_default_creds.py`
   - Module performs dictionary attack against Juniper Router FTP service. If valid credentials are foundm they are displayed to the user.
   - Devices: Juniper Router

17. **Juniper Router Default SSH Creds**
   - Path: `creds/perimeter/juniper/ssh_default_creds.py`
   - Module performs dictionary attack against Juniper Router SSH service. If valid credentials are foundm they are displayed to the user.
   - Devices: Juniper Router

18. **Juniper Router Default Telnet Creds**
   - Path: `creds/perimeter/juniper/telnet_default_creds.py`
   - Module performs dictionary attack against Juniper Router Telnet service. If valid credentials are foundm they are displayed to the user.
   - Devices: Juniper Router

### pfsense (2)

19. **PFSense Router Default Web Interface Creds - HTTP Form**
   - Path: `creds/perimeter/pfsense/webinterface_http_form_default_creds.py`
   - Module performs dictionary attack against PFSense Router web interface. If valid credentials are found, they are displayed to the user.
   - Devices: PFSense Router

20. **PFSense Router SSH Creds**
   - Path: `creds/perimeter/pfsense/ssh_default_creds.py`
   - Module performs dictionary attack against PFSense Router SSH service. If valid credentials are found, they are displayed to the user.
   - Devices: PFSense Router

### sftp_bruteforce.py (1)

21. **SFTP Bruteforce**
   - Path: `creds/generic/sftp_bruteforce.py`
   - Module performs bruteforce attack against SFTP service. If valid credentials are found, they are displayed to the user.
   - Devices: Multiple devices

### sftp_default.py (1)

22. **SFTP Default Creds**
   - Path: `creds/generic/sftp_default.py`
   - Module performs dictionary attack with default credentials against SFTP service. If valid credentials are found, they are displayed to the user.
   - Devices: Multiple devices

### snmp_bruteforce.py (1)

23. **SNMP Bruteforce**
   - Path: `creds/generic/snmp_bruteforce.py`
   - Module performs bruteforce attack against SNMP service. If valid community string is found, it is displayed to the user
   - Devices: Multiple devices

### snmpv3_default.py (1)

24. **SNMPv3 Default Creds**
   - Path: `creds/generic/snmpv3_default.py`
   - Module validates default SNMPv3 credentials against target service.
   - Devices: Routers, Switches, TAPs, FW, NGFW

### ssh_bruteforce.py (1)

25. **SSH Bruteforce**
   - Path: `creds/generic/ssh_bruteforce.py`
   - Module performs bruteforce attack against SSH service. If valid credentials are found, they are displayed to the user.
   - Devices: Multiple devices

### ssh_default.py (1)

26. **SSH Default Creds**
   - Path: `creds/generic/ssh_default.py`
   - Module performs bruteforce attack against SSH service. If valid credentials are found, they are displayed to the user.
   - Devices: Multiple devices

### telnet_bruteforce.py (1)

27. **Telnet Bruteforce**
   - Path: `creds/generic/telnet_bruteforce.py`
   - Module performs bruteforce attack against Telnet service. If valid credentials are found, they are displayed to the user.
   - Devices: Multiple devices

### telnet_default.py (1)

28. **Telnet Default Creds**
   - Path: `creds/generic/telnet_default.py`
   - Module performs dictionary attack with default credentials against Telnet service. If valid credentials are found, they are displayed to the user.
   - Devices: Multiple devices

## Scanners (3)

### autopwn.py (1)

1. **AutoPwn**
   - Path: `scanners/autopwn.py`
   - Module scans for vulnerabilities and weaknesses. Supports timing templates T0..T5 (default: balanced/T3).
   - Devices: FW, NGFW, UTM, WAF, SSL-VPN, NAC, ELB

### generic (1)

2. **Misc Scanner**
   - Path: `scanners/generic/misc_scan.py`
   - Module that scans for generic device vulnerabilities and weaknesses.
   - Devices: Misc Device

### vpn (1)

3. **FortiGate SSL-VPN / Web CVE Correlation Scan**
   - Path: `scanners/vpn/fortinet/fortigate_sslvpn_scan.py`
   - Fetches common FortiOS SSL-VPN paths (/remote/login, etc.), extracts version hints when present, and lists matching CVEs from the embedded + extended FirewallXPL-Forge catalog (CVE-2018-13379, CVE-202
   - CVEs: CVE-2018-13379, CVE-2022-40684, CVE-2023-27997, CVE-2024-21762, CVE-2025-59718
   - Devices: Fortinet FortiGate / FortiOS SSL-VPN

## Generic Modules (7)

### cve (1)

1. **CVE Lookup by Banner / Vendor / Product**
   - Path: `generic/cve/cve_lookup.py`
   - Queries the embedded CVE database for known vulnerabilities matching a target's vendor, product, version or raw banner. Classifies each CVE as REMOTE (exploitable by rxf), LOCAL or PHYSICAL. Lists ava
   - Devices: Any — database covers routers, switches, firewalls, NGFW in scope

### external (3)

2. **Metasploit Console Bridge**
   - Path: `generic/external/metasploit_console_bridge.py`
   - Invokes local msfconsole with 'use <module>; setg RHOSTS; …; check|run'. MSF modules and license remain under Rapid7/BSD at your install path — this module only orchestrates the CLI. Not legal advice:
   - Devices: Any (depends on chosen Metasploit module)

3. **Metasploit Ruby Module Metadata (read-only)**
   - Path: `generic/external/metasploit_rb_inspect.py`
   - Loads a .rb path from your Metasploit tree and prints Name/Author/References heuristics. Does not run Ruby or MSF; original file is not modified. Credit remains with module authors and Rapid7 license.
   - Devices: Documentation

4. **MikrotikAPI-BF Bridge**
   - Path: `generic/external/mikrotikapi_bf_bridge.py`
   - Runs MikrotikAPI-BF (https://github.com/mrhenrike/MikrotikAPI-BF) via subprocess. Set script_path to your repo's mikrotikapi-bf.py or leave empty to use PATH (mikrotikapi-bf).
   - Devices: MikroTik RouterOS

### snmp (1)

5. **SNMP Trap Listener**
   - Path: `generic/snmp/snmp_trap_listener.py`
   - Operational validation module for SNMP trap reception over UDP.
   - Devices: Routers, Switches, TAPs, FW, NGFW

### upnp (1)

6. **SSDP M-SEARCH Info Discovery**
   - Path: `generic/upnp/ssdp_msearch.py`
   - Sends M-SEARCH request to target and retrieve information from UPnP enabled systems.

### wordlist (1)

7. **Interactive Wordlist Generator**
   - Path: `generic/wordlist/wordlist_generator.py`
   - Generates custom password and username wordlists based on target profile (corporate or personal). Applies mutation rules (leet speak, case variations, number suffixes, date fragments, word combination
   - Devices: Any target — wordlist generation is target-independent

## Encoders (13)

### perl (4)

1. **Perl Base64 Encoder**
   - Path: `encoders/perl/base64.py`
   - Module encodes PERL payload to Base64 format.

2. **Perl Hex Encoder**
   - Path: `encoders/perl/hex.py`
   - Module encodes PERL payload to Hex format.

3. **Perl ROT13 Encoder**
   - Path: `encoders/perl/rot13.py`
   - Module encodes PERL payload to ROT13 format.

4. **Perl URL Encoder**
   - Path: `encoders/perl/url.py`
   - Module encodes PERL payload to URL-encoded format.

### php (4)

5. **PHP Base64 Encoder**
   - Path: `encoders/php/base64.py`
   - Module encodes PHP payload to Base64 format.

6. **PHP Hex Encoder**
   - Path: `encoders/php/hex.py`
   - Module encodes PHP payload to Hex format.

7. **PHP ROT13 Encoder**
   - Path: `encoders/php/rot13.py`
   - Module encodes PHP payload to ROT13 format.

8. **PHP URL Encoder**
   - Path: `encoders/php/url.py`
   - Module encodes PHP payload to URL-encoded format.

### python (5)

9. **Python Base32 Encoder**
   - Path: `encoders/python/base32.py`
   - Module encodes Python payload to Base32 format.

10. **Python Base64 Encoder**
   - Path: `encoders/python/base64.py`
   - Module encodes Python payload to Base64 format.

11. **Python Hex Encoder**
   - Path: `encoders/python/hex.py`
   - Module encodes Python payload to Hex format.

12. **Python ROT13 Encoder**
   - Path: `encoders/python/rot13.py`
   - Module encodes Python payload to ROT13 format.

13. **Python URL Encoder**
   - Path: `encoders/python/url.py`
   - Module encodes Python payload to URL-encoded format.

## Payloads (32)

### armle (2)

1. **ARMLE Bind TCP**
   - Path: `payloads/armle/bind_tcp.py`
   - Creates interactive tcp bind shell for ARMLE architecture.

2. **ARMLE Reverse TCP**
   - Path: `payloads/armle/reverse_tcp.py`
   - Creates interactive tcp reverse shell for ARMLE architecture.

### cmd (14)

3. **Awk Bind TCP**
   - Path: `payloads/cmd/awk_bind_tcp.py`
   - Creates an interactive tcp bind shell by using (g)awk.

4. **Awk Bind UDP**
   - Path: `payloads/cmd/awk_bind_udp.py`
   - Creates an interactive udp bind shell by using (g)awk.

5. **Awk Reverse TCP**
   - Path: `payloads/cmd/awk_reverse_tcp.py`
   - Creates an interactive tcp reverse shell by using (g)awk.

6. **Bash Reverse TCP**
   - Path: `payloads/cmd/bash_reverse_tcp.py`
   - Creates interactive tcp reverse shell by using bash.

7. **Netcat Bind TCP**
   - Path: `payloads/cmd/netcat_bind_tcp.py`
   - Creates interactive tcp bind shell by using netcat.

8. **Netcat Reverse TCP**
   - Path: `payloads/cmd/netcat_reverse_tcp.py`
   - Creates interactive tcp reverse shell by using netcat.

9. **PHP Bind TCP One-Liner**
   - Path: `payloads/cmd/php_bind_tcp.py`
   - Creates interactive tcp bind shell by using php one-liner.

10. **PHP Reverse TCP One-Liner**
   - Path: `payloads/cmd/php_reverse_tcp.py`
   - Creates interactive tcp reverse shell by using php one-liner.

11. **Perl Bind TCP One-Liner**
   - Path: `payloads/cmd/perl_bind_tcp.py`
   - Creates interactive tcp bind shell by using perl one-liner.

12. **Perl Reverse TCP One-Liner**
   - Path: `payloads/cmd/perl_reverse_tcp.py`
   - Creates interactive tcp reverse shell by using perl one-liner.

13. **Python Bind UDP One-Liner**
   - Path: `payloads/cmd/python_bind_udp.py`
   - Creates interactive udp bind shell by using python one-liner.

14. **Python Reverse TCP One-Liner**
   - Path: `payloads/cmd/python_bind_tcp.py`
   - Creates interactive tcp bind shell by using python one-liner.

15. **Python Reverse TCP One-Liner**
   - Path: `payloads/cmd/python_reverse_tcp.py`
   - Creates interactive tcp reverse shell by using python one-liner.

16. **Python Reverse UDP One-Liner**
   - Path: `payloads/cmd/python_reverse_udp.py`
   - Creates interactive udp reverse shell by using python one-liner.

### mipsbe (2)

17. **MIPSBE Bind TCP**
   - Path: `payloads/mipsbe/bind_tcp.py`
   - Creates interactive tcp bind shell for MIPSBE architecture.

18. **MIPSBE Reverse TCP**
   - Path: `payloads/mipsbe/reverse_tcp.py`
   - Creates interactive tcp reverse shell for MIPSBE architecture.

### mipsle (2)

19. **MIPSLE Bind TCP**
   - Path: `payloads/mipsle/bind_tcp.py`
   - Creates interactive tcp bind shell for MIPSLE architecture.

20. **MIPSLE Reverse TCP**
   - Path: `payloads/mipsle/reverse_tcp.py`
   - Creates interactive tcp reverse shell for MIPSLE architecture.

### perl (2)

21. **Perl Bind TCP**
   - Path: `payloads/perl/bind_tcp.py`
   - Creates interactive tcp bind shell by using perl.

22. **Perl Reverse TCP**
   - Path: `payloads/perl/reverse_tcp.py`
   - Creates interactive tcp reverse shell by using perl.

### php (2)

23. **PHP Bind TCP**
   - Path: `payloads/php/bind_tcp.py`
   - Creates interactive tcp bind shell by using php.

24. **PHP Reverse TCP**
   - Path: `payloads/php/reverse_tcp.py`
   - Creates interactive tcp reverse shell by using php.

### python (4)

25. **Python Bind TCP**
   - Path: `payloads/python/bind_tcp.py`
   - Creates interactive tcp bind shell by using python.

26. **Python Bind UDP**
   - Path: `payloads/python/bind_udp.py`
   - Creates interactive udp bind shell by using python.

27. **Python Reverse TCP**
   - Path: `payloads/python/reverse_tcp.py`
   - Creates interactive tcp reverse shell by using python.

28. **Python Reverse UDP**
   - Path: `payloads/python/reverse_udp.py`
   - Creates interactive udp reverse shell by using python.

### x64 (2)

29. **X64 Bind TCP**
   - Path: `payloads/x64/bind_tcp.py`
   - Creates interactive tcp bind shell for X64 architecture.

30. **X64 Reverse TCP**
   - Path: `payloads/x64/reverse_tcp.py`
   - Creates interactive tcp reverse shell for X64 architecture.

### x86 (2)

31. **X86 Bind TCP**
   - Path: `payloads/x86/bind_tcp.py`
   - Creates interactive tcp bind shell for X86 architecture.

32. **X86 Reverse TCP**
   - Path: `payloads/x86/reverse_tcp.py`
   - Creates interactive tcp reverse shell for X86 architecture.

---

## CVE Master List (77)

| # | CVE ID | Modules |
|---:|---|---|
| 1 | CVE-2011-3315 | `exploits/perimeter/cisco/unified_multi_path_traversal.py` |
| 2 | CVE-2013-7030 | `exploits/perimeter/cisco/ucm_info_disclosure.py` |
| 3 | CVE-2014-3413 | `exploits/perimeter/fortinet/fortigate_os_backdoor.py` |
| 4 | CVE-2014-6271 | `exploits/perimeter/generic/shellshock.py`, `exploits/perimeter/sonicwall/sslvpn_shellshock_rce_visualdoor.py` |
| 5 | CVE-2014-6278 | `exploits/perimeter/generic/shellshock.py` |
| 6 | CVE-2014-7169 | `exploits/perimeter/generic/shellshock.py` |
| 7 | CVE-2016-6433 | `exploits/perimeter/cisco/firepower_management60_rce.py` |
| 8 | CVE-2016-6435 | `exploits/perimeter/cisco/firepower_management60_path_traversal.py` |
| 9 | CVE-2017-6026 | `exploits/perimeter/schneider/connexium_ssh_hardcoded_cve_2017_6026.py` |
| 10 | CVE-2018-0101 | `exploits/perimeter/cisco/isa3000_asa_rce_cve_2018_0101.py` |
| 11 | CVE-2018-13379 | `exploits/perimeter/fortinet/fortios_sslvpn_path_traversal_cve_2018_13379.py`, `scanners/vpn/fortinet/fortigate_sslvpn_scan.py` |
| 12 | CVE-2019-11510 | `exploits/vpn/pulsesecure/sslvpn_arbitrary_file_read_cve_2019_11510.py` |
| 13 | CVE-2019-19781 | `exploits/vpn/citrix/adc_rce_cve_2019_19781.py` |
| 14 | CVE-2020-12271 | `exploits/perimeter/sophos/xg_sqli_asnarok_cve_2020_12271.py` |
| 15 | CVE-2020-14500 | `exploits/vpn/secomea/gatemanager_rce_cve_2020_14500.py` |
| 16 | CVE-2020-2021 | `exploits/perimeter/paloalto/panos_saml_auth_bypass_cve_2020_2021.py` |
| 17 | CVE-2020-3452 | `exploits/perimeter/cisco/asa_ftd_path_traversal_cve_2020_3452.py` |
| 18 | CVE-2020-5135 | `exploits/perimeter/sonicwall/sonicos_vpn_buffer_overflow_cve_2020_5135.py` |
| 19 | CVE-2020-5902 | `exploits/lb/f5/bigip_tmui_lfi_cve_2020_5902.py` |
| 20 | CVE-2020-6994 | `exploits/perimeter/hirschmann/eagle_auth_bypass_cve_2020_6994.py` |
| 21 | CVE-2021-20016 | `exploits/perimeter/sonicwall/sma100_sqli_cve_2021_20016.py` |
| 22 | CVE-2021-20034 | `exploits/perimeter/sonicwall/sma_password_reset_cve_2021_20034.py` |
| 23 | CVE-2021-22986 | `exploits/lb/f5/bigip_icontrol_rest_rce_cve_2021_22986.py` |
| 24 | CVE-2022-1040 | `exploits/perimeter/sophos/xg_auth_bypass_cve_2022_1040.py` |
| 25 | CVE-2022-1388 | `exploits/lb/f5/bigip_icontrol_auth_bypass_cve_2022_1388.py` |
| 26 | CVE-2022-23176 | `exploits/perimeter/watchguard/firebox_cyclops_blink_cve_2022_23176.py` |
| 27 | CVE-2022-30525 | `exploits/perimeter/zyxel/usg_flex_cmd_injection_cve_2022_30525.py` |
| 28 | CVE-2022-31814 | `exploits/perimeter/pfsense/pfblockerng_rce_cve_2022_31814.py` |
| 29 | CVE-2022-32257 | `exploits/perimeter/siemens/sinema_rc_path_traversal_cve_2022_32257.py` |
| 30 | CVE-2022-3236 | `exploits/perimeter/sophos/firewall_code_injection_cve_2022_3236.py` |
| 31 | CVE-2022-40684 | `exploits/perimeter/fortinet/fortios_auth_bypass_cve_2022_40684.py`, `scanners/vpn/fortinet/fortigate_sslvpn_scan.py` |
| 32 | CVE-2022-42475 | `exploits/perimeter/fortinet/fortios_sslvpn_heap_rce_cve_2022_42475.py` |
| 33 | CVE-2023-20198 | `exploits/perimeter/cisco/ios_xe_webui_privesc_cve_2023_20198.py` |
| 34 | CVE-2023-20269 | `exploits/perimeter/cisco/asa_vpn_bruteforce_cve_2023_20269.py` |
| 35 | CVE-2023-24845 | `exploits/perimeter/siemens/ruggedcom_web_rce_cve_2023_24845.py` |
| 36 | CVE-2023-25594 | `exploits/nac/aruba/clearpass_unauth_rce_cve_2023_25594.py` |
| 37 | CVE-2023-27100 | `exploits/perimeter/pfsense/antibruteforce_bypass_cve_2023_27100.py` |
| 38 | CVE-2023-27997 | `exploits/perimeter/fortinet/fortios_sslvpn_preauth_rce_cve_2023_27997.py`, `scanners/vpn/fortinet/fortigate_sslvpn_scan.py` |
| 39 | CVE-2023-2868 | `exploits/waf/barracuda/esg_cmd_injection_cve_2023_2868.py` |
| 40 | CVE-2023-28771 | `exploits/perimeter/zyxel/ike_cmd_injection_cve_2023_28771.py` |
| 41 | CVE-2023-33009 | `exploits/perimeter/zyxel/buffer_overflow_cve_2023_33009.py` |
| 42 | CVE-2023-3519 | `exploits/vpn/citrix/netscaler_rce_cve_2023_3519.py` |
| 43 | CVE-2023-36845 | `exploits/perimeter/juniper/jweb_php_rce_cve_2023_36845.py` |
| 44 | CVE-2023-42326 | `exploits/perimeter/pfsense/interfaces_cmd_injection_cve_2023_42326.py` |
| 45 | CVE-2023-44373 | `exploits/perimeter/siemens/scalance_cmd_injection_cve_2023_44373.py` |
| 46 | CVE-2023-46747 | `exploits/lb/f5/bigip_config_rce_cve_2023_46747.py` |
| 47 | CVE-2023-46805 | `exploits/vpn/ivanti/connect_secure_auth_rce_cve_2023_46805.py` |
| 48 | CVE-2023-48788 | `exploits/perimeter/fortinet/forticlientems_sqli_rce_cve_2023_48788.py` |
| 49 | CVE-2023-4966 | `exploits/vpn/citrix/netscaler_citrixbleed_cve_2023_4966.py` |
| 50 | CVE-2023-7102 | `exploits/waf/barracuda/esg_spreadsheet_rce_cve_2023_7102.py` |
| 51 | CVE-2024-0012 | `exploits/perimeter/paloalto/panos_mgmt_auth_bypass_cve_2024_0012.py`, `exploits/perimeter/paloalto/panos_privesc_cve_2024_9474.py` |
| 52 | CVE-2024-21591 | `exploits/perimeter/juniper/jweb_oob_write_rce_cve_2024_21591.py` |
| 53 | CVE-2024-21762 | `exploits/perimeter/fortinet/fortios_sslvpn_rce_cve_2024_21762.py`, `scanners/vpn/fortinet/fortigate_sslvpn_scan.py` |
| 54 | CVE-2024-21887 | `exploits/vpn/ivanti/connect_secure_auth_rce_cve_2023_46805.py` |
| 55 | CVE-2024-24919 | `exploits/perimeter/checkpoint/gateway_info_disclosure_cve_2024_24919.py` |
| 56 | CVE-2024-3400 | `exploits/perimeter/paloalto/globalprotect_cmd_injection_cve_2024_3400.py` |
| 57 | CVE-2024-40766 | `exploits/perimeter/sonicwall/sonicos_sslvpn_access_cve_2024_40766.py` |
| 58 | CVE-2024-43386 | `exploits/perimeter/phoenix/mguard_cmd_injection_cve_2024_43386.py` |
| 59 | CVE-2024-47575 | `exploits/perimeter/fortinet/fortimanager_fortijump_cve_2024_47575.py` |
| 60 | CVE-2024-50562 | `exploits/perimeter/fortinet/fortios_sslvpn_session_reuse_cve_2024_50562.py` |
| 61 | CVE-2024-53704 | `exploits/perimeter/sonicwall/sonicos_sslvpn_auth_bypass_cve_2024_53704.py` |
| 62 | CVE-2024-55591 | `exploits/perimeter/fortinet/fortios_websocket_auth_bypass_cve_2024_55591.py` |
| 63 | CVE-2024-9137 | `exploits/perimeter/moxa/edr_g_jwt_hardcoded_cve_2024_9137.py` |
| 64 | CVE-2024-9138 | `exploits/perimeter/moxa/edr_cmd_injection_cve_2024_9138.py` |
| 65 | CVE-2024-9474 | `exploits/perimeter/paloalto/panos_mgmt_auth_bypass_cve_2024_0012.py`, `exploits/perimeter/paloalto/panos_privesc_cve_2024_9474.py` |
| 66 | CVE-2025-0108 | `exploits/perimeter/paloalto/panos_auth_bypass_cve_2025_0108.py` |
| 67 | CVE-2025-0282 | `exploits/vpn/ivanti/ics_buffer_overflow_rce_cve_2025_0282.py` |
| 68 | CVE-2025-20333 | `exploits/perimeter/cisco/cisco_asa_ftd_firestarter_chain_cve_2025_20362_20333.py` |
| 69 | CVE-2025-20362 | `exploits/perimeter/cisco/cisco_asa_ftd_firestarter_chain_cve_2025_20362_20333.py` |
| 70 | CVE-2025-25257 | `exploits/perimeter/fortinet/fortiweb/fortiweb_auth_bypass_rce_cve_2025_25257.py` |
| 71 | CVE-2025-53521 | `exploits/lb/f5/bigip_apm_buffer_overflow_cve_2025_53521.py` |
| 72 | CVE-2025-59718 | `scanners/vpn/fortinet/fortigate_sslvpn_scan.py` |
| 73 | CVE-2025-64446 | `exploits/perimeter/fortinet/fortiweb/fortiweb_admin_rce_cve_2025_64446.py` |
| 74 | CVE-2026-0257 | `exploits/perimeter/paloalto/globalprotect_auth_bypass_cve_2026_0257.py` |
| 75 | CVE-2026-24858 | `exploits/perimeter/fortinet/forticloud_sso_auth_bypass_cve_2026_24858.py` |
| 76 | CVE-2026-25823 | `exploits/vpn/ewon/cosy_unauth_rce_cve_2026_25823.py` |
| 77 | CVE-2026-35616 | `exploits/perimeter/fortinet/forticlient_ems_preauth_api_bypass_cve_2026_35616.py` |

## CVEs by Vendor

| Vendor | CVE Count | CVE IDs |
|---|---:|---|
| aruba | 1 | CVE-2023-25594 |
| barracuda | 2 | CVE-2023-2868, CVE-2023-7102 |
| checkpoint | 1 | CVE-2024-24919 |
| cisco | 10 | CVE-2011-3315, CVE-2013-7030, CVE-2016-6433, CVE-2016-6435, CVE-2018-0101, CVE-2020-3452, CVE-2023-20198, CVE-2023-20269, CVE-2025-20333, CVE-2025-20362 |
| citrix | 3 | CVE-2019-19781, CVE-2023-3519, CVE-2023-4966 |
| ewon | 1 | CVE-2026-25823 |
| f5 | 5 | CVE-2020-5902, CVE-2021-22986, CVE-2022-1388, CVE-2023-46747, CVE-2025-53521 |
| fortinet | 14 | CVE-2014-3413, CVE-2018-13379, CVE-2022-40684, CVE-2022-42475, CVE-2023-27997, CVE-2023-48788, CVE-2024-21762, CVE-2024-47575, CVE-2024-50562, CVE-2024-55591, CVE-2025-25257, CVE-2025-64446, CVE-2026-24858, CVE-2026-35616 |
| generic | 3 | CVE-2014-6271, CVE-2014-6278, CVE-2014-7169 |
| hirschmann | 1 | CVE-2020-6994 |
| ivanti | 3 | CVE-2023-46805, CVE-2024-21887, CVE-2025-0282 |
| juniper | 2 | CVE-2023-36845, CVE-2024-21591 |
| moxa | 2 | CVE-2024-9137, CVE-2024-9138 |
| paloalto | 6 | CVE-2020-2021, CVE-2024-0012, CVE-2024-3400, CVE-2024-9474, CVE-2025-0108, CVE-2026-0257 |
| pfsense | 3 | CVE-2022-31814, CVE-2023-27100, CVE-2023-42326 |
| phoenix | 1 | CVE-2024-43386 |
| pulsesecure | 1 | CVE-2019-11510 |
| schneider | 1 | CVE-2017-6026 |
| secomea | 1 | CVE-2020-14500 |
| siemens | 3 | CVE-2022-32257, CVE-2023-24845, CVE-2023-44373 |
| sonicwall | 6 | CVE-2014-6271, CVE-2020-5135, CVE-2021-20016, CVE-2021-20034, CVE-2024-40766, CVE-2024-53704 |
| sophos | 3 | CVE-2020-12271, CVE-2022-1040, CVE-2022-3236 |
| vpn | 5 | CVE-2018-13379, CVE-2022-40684, CVE-2023-27997, CVE-2024-21762, CVE-2025-59718 |
| watchguard | 1 | CVE-2022-23176 |
| zyxel | 3 | CVE-2022-30525, CVE-2023-28771, CVE-2023-33009 |

---

> Generated by tools/generate_full_catalog.py