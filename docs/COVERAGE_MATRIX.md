# FirewallXPL-Forge Coverage Matrix

## Product Scope

- In scope: routers, switches, taps, fw and ngfw (residential, ISP, enterprise/corporate, industrial; IT/OT/AT/IoT/IIoT).
- Out of scope: camera/printer/dvr modules (disabled in this product line).

## Platform Compatibility Status

| Platform | Status |
|---|---|
| Windows | Compatible (validated locally) |
| WSL / Debian-based Linux | Compatible (validated locally) |
| RHEL-based Linux | Compatible by design, not tested effectively yet |
| macOS | Compatible by design, not tested effectively yet |
| Termux / Android / NetHunter | Compatible by design, not tested effectively yet |


## Global Capability Summary

- Module tree (firewallxpl/modules): fc41c8c2bfe0f1774c1cdfba05500447336e76a2
- Total modules indexed: 172
- Distinct vendor/product entries: 172
- Distinct CVEs mapped in modules: 77
- Attack classes identified: auth_bypass, backdoor, info_disclosure, password_reset_or_change, path_traversal, rce

### Module Type Counts
- creds: 28
- encoders: 13
- exploits: 89
- generic: 7
- payloads: 32
- scanners: 3

## Protocol Coverage (Inferred)

| Protocol | Covered |
|---|---|
| ftp | yes |
| ftps | no |
| sftp | yes |
| ssh | yes |
| telnet | yes |
| snmp | yes |
| snmp_trap | yes |
| api | yes |
| http | yes |
| https | yes |

## OSI/TCP-IP Coverage Matrix

### Priority Definitions

- P1: Critical first wave: management plane and service base protocols with immediate operational risk.
- P2: Second wave: control and environment-specific protocols with medium operational impact.
- P3: Third wave: legacy or lower-frequency protocols tracked until full closure.

### Environment Focus

| Environment | Priority Order | Focus |
|---|---|---|
| ISP | P1,P2,P3 | CPE and provider edge management plane, service availability, routing control and subscriber provisioning. |
| Corporate | P1,P2,P3 | Enterprise access/distribution/core, segmentation, identity-aware admin access and telemetry. |
| OT_IIoT | P1,P2,P3 | Availability first, deterministic network behavior, IT/OT boundary control and secure remote management. |

### Layer Attack/Test Matrix

| OSI | Layer | Attack Vectors | Test Types |
|---|---|---|---|
| L1 | Physical | link_disruption_or_flap_induction, tap_or_span_blind_spot_abuse, physical_plane_availability_degradation | link_state_validation, duplex_speed_mismatch_detection, capture_integrity_verification |
| L2 | Data Link | vlan_hopping_and_tagging_abuse, arp_spoofing_or_poisoning, stp_manipulation_or_loop_induction, mac_table_exhaustion_scenarios, wpa_wpa2_offline_handshake_crack, wireless_credential_harvest_from_pcap, rogue_ap_detection_via_pcap | vlan_segmentation_validation, arp_integrity_checks, stp_lacp_hardening_review, l2_discovery_surface_assessment, pcap_ap_station_enumeration, pcap_handshake_completeness_check, pcap_cleartext_credential_extraction |
| L3 | Network | route_injection_or_hijack_paths, icmp_or_control_plane_abuse, ipv6_transition_misconfig_exposure | routing_surface_enumeration, dual_stack_consistency_checks, control_plane_exposure_validation |
| L4 | Transport | service_enumeration_and_port_abuse, session_exhaustion_or_flood_paths, transport_timeout_and_retry_abuse | tcp_udp_surface_mapping, session_stability_validation, timeout_retry_behavior_checks |
| L5-L7 | Session/Presentation/Application | default_credential_and_bruteforce_paths, auth_bypass_and_session_abuse, protocol_parser_and_input_injection_paths, management_api_and_header_abuse, snmp_read_write_and_trap_plane_misuse | credential_validation_matrix, auth_method_coverage_checks, protocol_specific_exploitability_checks, snmpv2_snmpv3_trap_operational_validation, api_and_web_management_flow_validation |

### Layer and Protocol Coverage (Inferred)

| OSI | TCP/IP | Layer | Protocol | Module Hits | Covered | Attack Vectors | Test Types | ISP | Corporate | OT_IIoT |
|---|---|---|---|---:|---|---|---|---|---|---|
| L1 | Link | Physical | ethernet | 2 | yes | link_disruption_or_flap_induction, tap_or_span_blind_spot_abuse, physical_plane_availability_degradation | link_state_validation, duplex_speed_mismatch_detection, capture_integrity_verification | P2 | P2 | P2 |
| L2 | Link | Data Link | arp | 2 | yes | vlan_hopping_and_tagging_abuse, arp_spoofing_or_poisoning, stp_manipulation_or_loop_induction, mac_table_exhaustion_scenarios, wpa_wpa2_offline_handshake_crack, wireless_credential_harvest_from_pcap, rogue_ap_detection_via_pcap | vlan_segmentation_validation, arp_integrity_checks, stp_lacp_hardening_review, l2_discovery_surface_assessment, pcap_ap_station_enumeration, pcap_handshake_completeness_check, pcap_cleartext_credential_extraction | P1 | P1 | P1 |
| L2 | Link | Data Link | vlan_8021q_qinq | 1 | yes | vlan_hopping_and_tagging_abuse, arp_spoofing_or_poisoning, stp_manipulation_or_loop_induction, mac_table_exhaustion_scenarios, wpa_wpa2_offline_handshake_crack, wireless_credential_harvest_from_pcap, rogue_ap_detection_via_pcap | vlan_segmentation_validation, arp_integrity_checks, stp_lacp_hardening_review, l2_discovery_surface_assessment, pcap_ap_station_enumeration, pcap_handshake_completeness_check, pcap_cleartext_credential_extraction | P1 | P1 | P1 |
| L2 | Link | Data Link | 802.11_wifi | 2 | yes | offline_wpa_crack, handshake_capture_replay, credential_harvest | ap_enumeration, station_mapping, handshake_extraction, cleartext_sniffing | P2 | P1 | P2 |
| L2 | Link | Data Link | stp_rstp_mstp | 0 | no | vlan_hopping_and_tagging_abuse, arp_spoofing_or_poisoning, stp_manipulation_or_loop_induction, mac_table_exhaustion_scenarios, wpa_wpa2_offline_handshake_crack, wireless_credential_harvest_from_pcap, rogue_ap_detection_via_pcap | vlan_segmentation_validation, arp_integrity_checks, stp_lacp_hardening_review, l2_discovery_surface_assessment, pcap_ap_station_enumeration, pcap_handshake_completeness_check, pcap_cleartext_credential_extraction | P2 | P1 | P2 |
| L2 | Link | Data Link | lacp | 0 | no | vlan_hopping_and_tagging_abuse, arp_spoofing_or_poisoning, stp_manipulation_or_loop_induction, mac_table_exhaustion_scenarios, wpa_wpa2_offline_handshake_crack, wireless_credential_harvest_from_pcap, rogue_ap_detection_via_pcap | vlan_segmentation_validation, arp_integrity_checks, stp_lacp_hardening_review, l2_discovery_surface_assessment, pcap_ap_station_enumeration, pcap_handshake_completeness_check, pcap_cleartext_credential_extraction | P2 | P1 | P2 |
| L2 | Link | Data Link | lldp | 0 | no | vlan_hopping_and_tagging_abuse, arp_spoofing_or_poisoning, stp_manipulation_or_loop_induction, mac_table_exhaustion_scenarios, wpa_wpa2_offline_handshake_crack, wireless_credential_harvest_from_pcap, rogue_ap_detection_via_pcap | vlan_segmentation_validation, arp_integrity_checks, stp_lacp_hardening_review, l2_discovery_surface_assessment, pcap_ap_station_enumeration, pcap_handshake_completeness_check, pcap_cleartext_credential_extraction | P2 | P2 | P2 |
| L2 | Link | Data Link | pppoe | 0 | no | vlan_hopping_and_tagging_abuse, arp_spoofing_or_poisoning, stp_manipulation_or_loop_induction, mac_table_exhaustion_scenarios, wpa_wpa2_offline_handshake_crack, wireless_credential_harvest_from_pcap, rogue_ap_detection_via_pcap | vlan_segmentation_validation, arp_integrity_checks, stp_lacp_hardening_review, l2_discovery_surface_assessment, pcap_ap_station_enumeration, pcap_handshake_completeness_check, pcap_cleartext_credential_extraction | P1 | P3 | P3 |
| L3 | Internet | Network | ipv4_ipv6 | 0 | no | route_injection_or_hijack_paths, icmp_or_control_plane_abuse, ipv6_transition_misconfig_exposure | routing_surface_enumeration, dual_stack_consistency_checks, control_plane_exposure_validation | P1 | P1 | P1 |
| L3 | Internet | Network | icmp_icmpv6 | 0 | no | route_injection_or_hijack_paths, icmp_or_control_plane_abuse, ipv6_transition_misconfig_exposure | routing_surface_enumeration, dual_stack_consistency_checks, control_plane_exposure_validation | P1 | P1 | P2 |
| L3 | Internet | Network | ospf | 0 | no | route_injection_or_hijack_paths, icmp_or_control_plane_abuse, ipv6_transition_misconfig_exposure | routing_surface_enumeration, dual_stack_consistency_checks, control_plane_exposure_validation | P2 | P2 | P3 |
| L3 | Internet | Network | bgp | 0 | no | route_injection_or_hijack_paths, icmp_or_control_plane_abuse, ipv6_transition_misconfig_exposure | routing_surface_enumeration, dual_stack_consistency_checks, control_plane_exposure_validation | P2 | P3 | P3 |
| L4 | Transport | Transport | tcp | 28 | yes | service_enumeration_and_port_abuse, session_exhaustion_or_flood_paths, transport_timeout_and_retry_abuse | tcp_udp_surface_mapping, session_stability_validation, timeout_retry_behavior_checks | P1 | P1 | P1 |
| L4 | Transport | Transport | udp | 6 | yes | service_enumeration_and_port_abuse, session_exhaustion_or_flood_paths, transport_timeout_and_retry_abuse | tcp_udp_surface_mapping, session_stability_validation, timeout_retry_behavior_checks | P1 | P1 | P1 |
| L5-L7 | Application | Session/Presentation/Application | dns | 0 | no | default_credential_and_bruteforce_paths, auth_bypass_and_session_abuse, protocol_parser_and_input_injection_paths, management_api_and_header_abuse, snmp_read_write_and_trap_plane_misuse | credential_validation_matrix, auth_method_coverage_checks, protocol_specific_exploitability_checks, snmpv2_snmpv3_trap_operational_validation, api_and_web_management_flow_validation | P1 | P1 | P2 |
| L5-L7 | Application | Session/Presentation/Application | dhcp | 0 | no | default_credential_and_bruteforce_paths, auth_bypass_and_session_abuse, protocol_parser_and_input_injection_paths, management_api_and_header_abuse, snmp_read_write_and_trap_plane_misuse | credential_validation_matrix, auth_method_coverage_checks, protocol_specific_exploitability_checks, snmpv2_snmpv3_trap_operational_validation, api_and_web_management_flow_validation | P1 | P1 | P2 |
| L5-L7 | Application | Session/Presentation/Application | ntp_ptp | 0 | no | default_credential_and_bruteforce_paths, auth_bypass_and_session_abuse, protocol_parser_and_input_injection_paths, management_api_and_header_abuse, snmp_read_write_and_trap_plane_misuse | credential_validation_matrix, auth_method_coverage_checks, protocol_specific_exploitability_checks, snmpv2_snmpv3_trap_operational_validation, api_and_web_management_flow_validation | P1 | P2 | P1 |
| L5-L7 | Application | Session/Presentation/Application | snmp_snmpv3 | 4 | yes | default_credential_and_bruteforce_paths, auth_bypass_and_session_abuse, protocol_parser_and_input_injection_paths, management_api_and_header_abuse, snmp_read_write_and_trap_plane_misuse | credential_validation_matrix, auth_method_coverage_checks, protocol_specific_exploitability_checks, snmpv2_snmpv3_trap_operational_validation, api_and_web_management_flow_validation | P1 | P1 | P1 |
| L5-L7 | Application | Session/Presentation/Application | ssh | 11 | yes | default_credential_and_bruteforce_paths, auth_bypass_and_session_abuse, protocol_parser_and_input_injection_paths, management_api_and_header_abuse, snmp_read_write_and_trap_plane_misuse | credential_validation_matrix, auth_method_coverage_checks, protocol_specific_exploitability_checks, snmpv2_snmpv3_trap_operational_validation, api_and_web_management_flow_validation | P1 | P1 | P1 |
| L5-L7 | Application | Session/Presentation/Application | telnet | 6 | yes | default_credential_and_bruteforce_paths, auth_bypass_and_session_abuse, protocol_parser_and_input_injection_paths, management_api_and_header_abuse, snmp_read_write_and_trap_plane_misuse | credential_validation_matrix, auth_method_coverage_checks, protocol_specific_exploitability_checks, snmpv2_snmpv3_trap_operational_validation, api_and_web_management_flow_validation | P2 | P3 | P2 |
| L5-L7 | Application | Session/Presentation/Application | ftp_ftps_sftp | 9 | yes | default_credential_and_bruteforce_paths, auth_bypass_and_session_abuse, protocol_parser_and_input_injection_paths, management_api_and_header_abuse, snmp_read_write_and_trap_plane_misuse | credential_validation_matrix, auth_method_coverage_checks, protocol_specific_exploitability_checks, snmpv2_snmpv3_trap_operational_validation, api_and_web_management_flow_validation | P2 | P2 | P2 |
| L5-L7 | Application | Session/Presentation/Application | http_https_api | 23 | yes | default_credential_and_bruteforce_paths, auth_bypass_and_session_abuse, protocol_parser_and_input_injection_paths, management_api_and_header_abuse, snmp_read_write_and_trap_plane_misuse | credential_validation_matrix, auth_method_coverage_checks, protocol_specific_exploitability_checks, snmpv2_snmpv3_trap_operational_validation, api_and_web_management_flow_validation | P1 | P1 | P1 |
| L5-L7 | Application | Session/Presentation/Application | radius_tacacs | 0 | no | default_credential_and_bruteforce_paths, auth_bypass_and_session_abuse, protocol_parser_and_input_injection_paths, management_api_and_header_abuse, snmp_read_write_and_trap_plane_misuse | credential_validation_matrix, auth_method_coverage_checks, protocol_specific_exploitability_checks, snmpv2_snmpv3_trap_operational_validation, api_and_web_management_flow_validation | P3 | P2 | P3 |
| L5-L7 | Application | Session/Presentation/Application | tr069_cwmp | 1 | yes | default_credential_and_bruteforce_paths, auth_bypass_and_session_abuse, protocol_parser_and_input_injection_paths, management_api_and_header_abuse, snmp_read_write_and_trap_plane_misuse | credential_validation_matrix, auth_method_coverage_checks, protocol_specific_exploitability_checks, snmpv2_snmpv3_trap_operational_validation, api_and_web_management_flow_validation | P2 | P3 | P3 |
| L5-L7 | Application | Session/Presentation/Application | syslog | 0 | no | default_credential_and_bruteforce_paths, auth_bypass_and_session_abuse, protocol_parser_and_input_injection_paths, management_api_and_header_abuse, snmp_read_write_and_trap_plane_misuse | credential_validation_matrix, auth_method_coverage_checks, protocol_specific_exploitability_checks, snmpv2_snmpv3_trap_operational_validation, api_and_web_management_flow_validation | P2 | P1 | P2 |
| L5-L7 | Application | Session/Presentation/Application | modbus_tcp | 1 | yes | default_credential_and_bruteforce_paths, auth_bypass_and_session_abuse, protocol_parser_and_input_injection_paths, management_api_and_header_abuse, snmp_read_write_and_trap_plane_misuse | credential_validation_matrix, auth_method_coverage_checks, protocol_specific_exploitability_checks, snmpv2_snmpv3_trap_operational_validation, api_and_web_management_flow_validation | P3 | P3 | P2 |
| L5-L7 | Application | Session/Presentation/Application | dnp3 | 1 | yes | default_credential_and_bruteforce_paths, auth_bypass_and_session_abuse, protocol_parser_and_input_injection_paths, management_api_and_header_abuse, snmp_read_write_and_trap_plane_misuse | credential_validation_matrix, auth_method_coverage_checks, protocol_specific_exploitability_checks, snmpv2_snmpv3_trap_operational_validation, api_and_web_management_flow_validation | P3 | P3 | P2 |
| L5-L7 | Application | Session/Presentation/Application | opc_ua | 1 | yes | default_credential_and_bruteforce_paths, auth_bypass_and_session_abuse, protocol_parser_and_input_injection_paths, management_api_and_header_abuse, snmp_read_write_and_trap_plane_misuse | credential_validation_matrix, auth_method_coverage_checks, protocol_specific_exploitability_checks, snmpv2_snmpv3_trap_operational_validation, api_and_web_management_flow_validation | P3 | P3 | P2 |
| L5-L7 | Application | Session/Presentation/Application | mqtt | 0 | no | default_credential_and_bruteforce_paths, auth_bypass_and_session_abuse, protocol_parser_and_input_injection_paths, management_api_and_header_abuse, snmp_read_write_and_trap_plane_misuse | credential_validation_matrix, auth_method_coverage_checks, protocol_specific_exploitability_checks, snmpv2_snmpv3_trap_operational_validation, api_and_web_management_flow_validation | P3 | P3 | P2 |
| L5-L7 | Application | Session/Presentation/Application | bacnet_ip | 0 | no | default_credential_and_bruteforce_paths, auth_bypass_and_session_abuse, protocol_parser_and_input_injection_paths, management_api_and_header_abuse, snmp_read_write_and_trap_plane_misuse | credential_validation_matrix, auth_method_coverage_checks, protocol_specific_exploitability_checks, snmpv2_snmpv3_trap_operational_validation, api_and_web_management_flow_validation | P3 | P3 | P2 |
| L5-L7 | Application | Session/Presentation/Application | profinet_ethernet | 0 | no | default_credential_and_bruteforce_paths, auth_bypass_and_session_abuse, protocol_parser_and_input_injection_paths, management_api_and_header_abuse, snmp_read_write_and_trap_plane_misuse | credential_validation_matrix, auth_method_coverage_checks, protocol_specific_exploitability_checks, snmpv2_snmpv3_trap_operational_validation, api_and_web_management_flow_validation | P3 | P3 | P2 |

### Layer Hit Totals

| Layer | Total Protocol Hits |
|---|---:|
| L1 Physical | 2 |
| L2 Data Link | 5 |
| L3 Network | 0 |
| L4 Transport | 34 |
| L5-L7 Session/Presentation/Application | 57 |

## Market Priority Coverage (2010-2026)

### Yearly Minimum Validation

- Brazil domestic minimum/year: 10
- Brazil corporate minimum/year: 10
- Global minimum/year: 5

#### Brazil Domestic Coverage By Year

| Year | Required | Cataloged | Status | Vendor Covered Count | Keyword Hits |
|---:|---:|---:|---|---:|---:|
| 2010 | 11 | 11 | ok | 0 | 0 |
| 2011 | 11 | 11 | ok | 0 | 0 |
| 2012 | 11 | 11 | ok | 0 | 0 |
| 2013 | 11 | 11 | ok | 0 | 0 |
| 2014 | 11 | 11 | ok | 0 | 0 |
| 2015 | 11 | 11 | ok | 0 | 0 |
| 2016 | 12 | 12 | ok | 0 | 0 |
| 2017 | 13 | 13 | ok | 0 | 0 |
| 2018 | 13 | 13 | ok | 0 | 0 |
| 2019 | 13 | 13 | ok | 0 | 0 |
| 2020 | 13 | 13 | ok | 0 | 0 |
| 2021 | 14 | 14 | ok | 0 | 0 |
| 2022 | 14 | 14 | ok | 0 | 0 |
| 2023 | 15 | 15 | ok | 0 | 0 |
| 2024 | 14 | 14 | ok | 0 | 0 |
| 2025 | 16 | 16 | ok | 0 | 0 |
| 2026 | 15 | 15 | ok | 0 | 0 |

#### Brazil Corporate Coverage By Year

| Year | Required | Cataloged | Status | Vendor Covered Count | Keyword Hits |
|---:|---:|---:|---|---:|---:|
| 2010 | 13 | 13 | ok | 6 | 0 |
| 2011 | 13 | 13 | ok | 6 | 0 |
| 2012 | 15 | 15 | ok | 6 | 0 |
| 2013 | 15 | 15 | ok | 6 | 0 |
| 2014 | 15 | 15 | ok | 7 | 0 |
| 2015 | 15 | 15 | ok | 7 | 0 |
| 2016 | 15 | 15 | ok | 8 | 2 |
| 2017 | 15 | 15 | ok | 8 | 2 |
| 2018 | 17 | 17 | ok | 9 | 0 |
| 2019 | 20 | 20 | ok | 9 | 0 |
| 2020 | 20 | 20 | ok | 9 | 0 |
| 2021 | 22 | 22 | ok | 9 | 2 |
| 2022 | 23 | 23 | ok | 10 | 2 |
| 2023 | 22 | 22 | ok | 10 | 2 |
| 2024 | 24 | 24 | ok | 10 | 2 |
| 2025 | 24 | 24 | ok | 10 | 2 |
| 2026 | 24 | 24 | ok | 10 | 2 |

#### Global Coverage By Year

| Year | Required | Cataloged | Status | Vendor Covered Count | Keyword Hits |
|---:|---:|---:|---|---:|---:|
| 2010 | 5 | 6 | ok | 1 | 0 |
| 2011 | 5 | 6 | ok | 1 | 0 |
| 2012 | 5 | 7 | ok | 2 | 0 |
| 2013 | 5 | 8 | ok | 2 | 0 |
| 2014 | 5 | 8 | ok | 1 | 0 |
| 2015 | 5 | 7 | ok | 1 | 0 |
| 2016 | 5 | 9 | ok | 2 | 0 |
| 2017 | 5 | 9 | ok | 2 | 0 |
| 2018 | 5 | 12 | ok | 3 | 0 |
| 2019 | 5 | 12 | ok | 2 | 0 |
| 2020 | 5 | 11 | ok | 2 | 0 |
| 2021 | 5 | 12 | ok | 2 | 0 |
| 2022 | 5 | 12 | ok | 3 | 0 |
| 2023 | 5 | 13 | ok | 3 | 0 |
| 2024 | 5 | 13 | ok | 3 | 0 |
| 2025 | 5 | 13 | ok | 3 | 0 |
| 2026 | 5 | 13 | ok | 3 | 0 |

### Brazil Domestic Device List (2010-2026)

| Year | Vendor | Product | Segment | Vendor Covered | Keyword Hits |
|---:|---|---|---|---|---:|
| 2010 | Netgear | WNDR3700 | router-home | no | 0 |
| 2010 | Linksys | WRT610N | router-home | no | 0 |
| 2010 | D-Link | DIR-655 | router-home | no | 0 |
| 2010 | TP-Link | TL-WR1043ND | router-home | no | 0 |
| 2010 | ASUS | RT-N13U | router-home | no | 0 |
| 2010 | Netgear | WNDR3800 | router-home | no | 0 |
| 2010 | Linksys | E3000 | router-home | no | 0 |
| 2010 | Trendnet | TEW-691GR | router-home | no | 0 |
| 2010 | Apple | AirPort Extreme 4th Gen | router-home | no | 0 |
| 2010 | Belkin | N750 DB | router-home | no | 0 |
| 2010 | BrazilFW | BrazilFW Firewall Router | fw-opensource | no | 0 |
| 2011 | Linksys | E4200 | router-home | no | 0 |
| 2011 | ASUS | RT-N56U | router-home | no | 0 |
| 2011 | Netgear | WNDR4000 | router-home | no | 0 |
| 2011 | Trendnet | TEW-692GR | router-home | no | 0 |
| 2011 | Belkin | N750 DB | router-home | no | 0 |
| 2011 | ASUS | RT-N66U | router-home | no | 0 |
| 2011 | D-Link | DIR-819 | router-home | no | 0 |
| 2011 | Linksys | E3200 | router-home | no | 0 |
| 2011 | Netgear | WNDR3700 | router-home | no | 0 |
| 2011 | Apple | AirPort Extreme 5th Gen | router-home | no | 0 |
| 2011 | BrazilFW | BrazilFW Firewall Router | fw-opensource | no | 0 |
| 2012 | TP-Link | Archer C20 | router-home | no | 0 |
| 2012 | TP-Link | Archer C6 | router-home | no | 0 |
| 2012 | TP-Link | Archer C7 | router-home | no | 0 |
| 2012 | D-Link | DIR-819 | router-home | no | 0 |
| 2012 | D-Link | DIR-822 | router-home | no | 0 |
| 2012 | ASUS | RT-AC86U | router-home | no | 0 |
| 2012 | Google | Nest Wi-Fi | router-mesh | no | 0 |
| 2012 | Intelbras | Action RG 1200 | router-home | no | 0 |
| 2012 | TP-Link | TL-WR940N | router-home | no | 0 |
| 2012 | TP-Link | TL-WR840N | router-home | no | 0 |
| 2012 | BrazilFW | BrazilFW Firewall Router | fw-opensource | no | 0 |
| 2013 | TP-Link | Archer C7 | router-home | no | 0 |
| 2013 | TP-Link | Archer C9 | router-home | no | 0 |
| 2013 | Netgear | Nighthawk Pro Gaming XR500 | router-home | no | 0 |
| 2013 | ASUS | RT-AC86U | router-home | no | 0 |
| 2013 | Google | Nest Wi-Fi | router-mesh | no | 0 |
| 2013 | TP-Link | Archer C6 | router-home | no | 0 |
| 2013 | TP-Link | TL-WR940N | router-home | no | 0 |
| 2013 | Intelbras | Action RG 1200 | router-home | no | 0 |
| 2013 | Huawei | AX3 Dual Core | router-home | no | 0 |
| 2013 | Mercusys | MR60X | router-home | no | 0 |
| 2013 | BrazilFW | BrazilFW Firewall Router | fw-opensource | no | 0 |
| 2014 | TP-Link | Archer C20 | router-home | no | 0 |
| 2014 | TP-Link | Archer C6 | router-home | no | 0 |
| 2014 | TP-Link | Archer C7 | router-home | no | 0 |
| 2014 | TP-Link | TL-WR940N | router-home | no | 0 |
| 2014 | Intelbras | Action RG 1200 | router-home | no | 0 |
| 2014 | ASUS | RT-AC86U | router-home | no | 0 |
| 2014 | Google | Nest Wi-Fi | router-mesh | no | 0 |
| 2014 | D-Link | DIR-819 | router-home | no | 0 |
| 2014 | D-Link | DIR-822 | router-home | no | 0 |
| 2014 | Mercusys | MR60X | router-home | no | 0 |
| 2014 | BrazilFW | BrazilFW Firewall Router | fw-opensource | no | 0 |
| 2015 | TP-Link | Archer C20 | router-home | no | 0 |
| 2015 | TP-Link | Archer C6 | router-home | no | 0 |
| 2015 | TP-Link | Archer C7 | router-home | no | 0 |
| 2015 | TP-Link | Archer C9 | router-home | no | 0 |
| 2015 | Google | Nest Wi-Fi | router-mesh | no | 0 |
| 2015 | ASUS | RT-AC86U | router-home | no | 0 |
| 2015 | D-Link | DIR-819 | router-home | no | 0 |
| 2015 | Intelbras | Action RG 1200 | router-home | no | 0 |
| 2015 | TP-Link | TL-WR840N | router-home | no | 0 |
| 2015 | TP-Link | TL-WR940N | router-home | no | 0 |
| 2015 | BrazilFW | BrazilFW Firewall Router | fw-opensource | no | 0 |
| 2016 | TP-Link | Archer C6 | router-home | no | 0 |
| 2016 | TP-Link | Archer C7 | router-home | no | 0 |
| 2016 | TP-Link | Archer C9 | router-home | no | 0 |
| 2016 | Google | Nest Wi-Fi | router-mesh | no | 0 |
| 2016 | Huawei | AX3 Dual Core | router-home | no | 0 |
| 2016 | Intelbras | Action RG 1200 | router-home | no | 0 |
| 2016 | D-Link | DIR-822 | router-home | no | 0 |
| 2016 | ASUS | RT-AC86U | router-home | no | 0 |
| 2016 | Mercusys | MR60X | router-home | no | 0 |
| 2016 | TP-Link | Deco M4 | router-mesh | no | 0 |
| 2016 | TP-Link | TL-SG108 | switch-soho | no | 0 |
| 2016 | Intelbras | SG 800 Q+ | switch-soho | no | 0 |
| 2017 | TP-Link | Deco M4 | router-mesh | no | 0 |
| 2017 | TP-Link | Archer C6 | router-home | no | 0 |
| 2017 | TP-Link | Archer C7 | router-home | no | 0 |
| 2017 | TP-Link | Archer C9 | router-home | no | 0 |
| 2017 | Intelbras | Action RG 1200 | router-home | no | 0 |
| 2017 | Huawei | AX3 Dual Core | router-home | no | 0 |
| 2017 | Mercusys | MR60X | router-home | no | 0 |
| 2017 | Google | Nest Wi-Fi | router-mesh | no | 0 |
| 2017 | ASUS | RT-AC86U | router-home | no | 0 |
| 2017 | Tenda | AC23 | router-home | no | 0 |
| 2017 | TP-Link | TL-SG108 | switch-soho | no | 0 |
| 2017 | Intelbras | SG 800 Q+ | switch-soho | no | 0 |
| 2017 | Mercusys | MS105G | switch-soho | no | 0 |
| 2018 | TP-Link | Deco M4 | router-mesh | no | 0 |
| 2018 | TP-Link | Archer C6 | router-home | no | 0 |
| 2018 | TP-Link | Archer C7 | router-home | no | 0 |
| 2018 | TP-Link | Archer C9 | router-home | no | 0 |
| 2018 | Intelbras | Action RG 1200 | router-home | no | 0 |
| 2018 | Huawei | AX3 Dual Core | router-home | no | 0 |
| 2018 | Mercusys | MR60X | router-home | no | 0 |
| 2018 | Google | Nest Wi-Fi | router-mesh | no | 0 |
| 2018 | ASUS | RT-AC86U | router-home | no | 0 |
| 2018 | Tenda | AC23 | router-home | no | 0 |
| 2018 | TP-Link | TL-SG108 | switch-soho | no | 0 |
| 2018 | Intelbras | SG 800 Q+ | switch-soho | no | 0 |
| 2018 | Mercusys | MS105G | switch-soho | no | 0 |
| 2019 | ASUS | RT-AC86U | router-home | no | 0 |
| 2019 | TP-Link | Archer C7 | router-home | no | 0 |
| 2019 | Netgear | Nighthawk Pro Gaming XR500 | router-home | no | 0 |
| 2019 | Google | Nest Wi-Fi | router-mesh | no | 0 |
| 2019 | TP-Link | Deco M4 | router-mesh | no | 0 |
| 2019 | D-Link | DIR-822 | router-home | no | 0 |
| 2019 | TP-Link | Archer C9 | router-home | no | 0 |
| 2019 | TP-Link | Archer C6 | router-home | no | 0 |
| 2019 | Mercusys | MR60X | router-home | no | 0 |
| 2019 | Intelbras | Action RG 1200 | router-home | no | 0 |
| 2019 | TP-Link | TL-SG108 | switch-soho | no | 0 |
| 2019 | Intelbras | SG 800 Q+ | switch-soho | no | 0 |
| 2019 | Mercusys | MS105G | switch-soho | no | 0 |
| 2020 | TP-Link | Archer C6 | router-home | no | 0 |
| 2020 | Intelbras | Action RG 1200 | router-home | no | 0 |
| 2020 | TP-Link | Archer C7 | router-home | no | 0 |
| 2020 | ASUS | RT-AC86U | router-home | no | 0 |
| 2020 | D-Link | DIR-819 | router-home | no | 0 |
| 2020 | TP-Link | Archer C20 | router-home | no | 0 |
| 2020 | TP-Link | Deco M4 | router-mesh | no | 0 |
| 2020 | TP-Link | Archer AX10 | router-home | no | 0 |
| 2020 | D-Link | DIR-822 | router-home | no | 0 |
| 2020 | TP-Link | TL-WR840N | router-home | no | 0 |
| 2020 | TP-Link | TL-SG108 | switch-soho | no | 0 |
| 2020 | Intelbras | SG 800 Q+ | switch-soho | no | 0 |
| 2020 | TP-Link | LS1005G | switch-soho | no | 0 |
| 2021 | TP-Link | Archer AX73 | router-home | no | 0 |
| 2021 | TP-Link | Archer AX10 | router-home | no | 0 |
| 2021 | ASUS | RT-AX88U | router-corporate | no | 0 |
| 2021 | TP-Link | Deco M4 | router-mesh | no | 0 |
| 2021 | Google | Nest Wi-Fi | router-mesh | no | 0 |
| 2021 | TP-Link | Archer C6 | router-home | no | 0 |
| 2021 | Intelbras | Action RG 1200 | router-home | no | 0 |
| 2021 | TP-Link | TL-WR940N | router-home | no | 0 |
| 2021 | Mercusys | MR60X | router-home | no | 0 |
| 2021 | Huawei | AX3 Dual Core | router-home | no | 0 |
| 2021 | OpenWrt | OpenWrt 21.02 Generic Targets | router-firmware | no | 0 |
| 2021 | TP-Link | TL-SG108 | switch-soho | no | 0 |
| 2021 | Intelbras | SG 800 Q+ | switch-soho | no | 0 |
| 2021 | TP-Link | LS1005G | switch-soho | no | 0 |
| 2022 | TP-Link | Archer AX73 | router-home | no | 0 |
| 2022 | TP-Link | Archer AX12 | router-home | no | 0 |
| 2022 | Huawei | AX3 Dual Core | router-home | no | 0 |
| 2022 | Mercusys | MR60X | router-home | no | 0 |
| 2022 | ASUS | RT-AX88U | router-corporate | no | 0 |
| 2022 | TP-Link | Archer C6 | router-home | no | 0 |
| 2022 | Intelbras | Action RG 1200 | router-home | no | 0 |
| 2022 | TP-Link | Deco M4 | router-mesh | no | 0 |
| 2022 | Huawei | AX2S | router-home | no | 0 |
| 2022 | Mercusys | MR80X | router-home | no | 0 |
| 2022 | TP-Link | TL-SG108 | switch-soho | no | 0 |
| 2022 | Intelbras | SG 800 Q+ | switch-soho | no | 0 |
| 2022 | TP-Link | LS1005G | switch-soho | no | 0 |
| 2022 | Netgear | GS305 | switch-soho | no | 0 |
| 2023 | TP-Link | Deco M4 | router-mesh | no | 0 |
| 2023 | TP-Link | Archer AX73 | router-home | no | 0 |
| 2023 | Intelbras | Action RG 1200 | router-home | no | 0 |
| 2023 | Huawei | AX3 Dual Core | router-home | no | 0 |
| 2023 | Mercusys | MR60X | router-home | no | 0 |
| 2023 | Google | Nest Wi-Fi | router-mesh | no | 0 |
| 2023 | ASUS | RT-AC86U | router-home | no | 0 |
| 2023 | TP-Link | Archer AX12 | router-home | no | 0 |
| 2023 | Intelbras | AX 1500 | router-home | no | 0 |
| 2023 | TP-Link | Archer C6 | router-home | no | 0 |
| 2023 | OpenWrt | OpenWrt 22.03 Generic Targets | router-firmware | no | 0 |
| 2023 | TP-Link | TL-SG108 | switch-soho | no | 0 |
| 2023 | Intelbras | SG 800 Q+ | switch-soho | no | 0 |
| 2023 | TP-Link | LS1005G | switch-soho | no | 0 |
| 2023 | Netgear | GS305 | switch-soho | no | 0 |
| 2024 | TP-Link | Archer AX73 | router-home | no | 0 |
| 2024 | Huawei | AX2S | router-home | no | 0 |
| 2024 | ASUS | AX5400 | router-home | no | 0 |
| 2024 | Mercusys | MR60X | router-home | no | 0 |
| 2024 | TP-Link | Deco M4 | router-mesh | no | 0 |
| 2024 | Intelbras | Action RG 1200 | router-home | no | 0 |
| 2024 | Google | Nest Wi-Fi | router-mesh | no | 0 |
| 2024 | TP-Link | Archer AX12 | router-home | no | 0 |
| 2024 | TP-Link | Archer C80 | router-home | no | 0 |
| 2024 | TP-Link | Deco BE85 | router-mesh | no | 0 |
| 2024 | TP-Link | TL-SG108 | switch-soho | no | 0 |
| 2024 | Intelbras | SG 800 Q+ | switch-soho | no | 0 |
| 2024 | TP-Link | LS1005G | switch-soho | no | 0 |
| 2024 | Netgear | GS305 | switch-soho | no | 0 |
| 2025 | Mercusys | MR60X | router-home | no | 0 |
| 2025 | TP-Link | Archer AXE75 | router-home | no | 0 |
| 2025 | ASUS | ROG Rapture GT-BE98 Pro | router-home | no | 0 |
| 2025 | TP-Link | Deco BE85 | router-mesh | no | 0 |
| 2025 | Huawei | AX3 Dual Core | router-home | no | 0 |
| 2025 | TP-Link | Archer AX10 | router-home | no | 0 |
| 2025 | TP-Link | Deco M4 | router-mesh | no | 0 |
| 2025 | TP-Link | Archer AX12 | router-home | no | 0 |
| 2025 | Google | Nest Wi-Fi | router-mesh | no | 0 |
| 2025 | TP-Link | Archer BE550 | router-home | no | 0 |
| 2025 | OpenWrt | OpenWrt 23.05 Generic Targets | router-firmware | no | 0 |
| 2025 | TP-Link | TL-SG108 | switch-soho | no | 0 |
| 2025 | Intelbras | SG 800 Q+ | switch-soho | no | 0 |
| 2025 | TP-Link | LS1005G | switch-soho | no | 0 |
| 2025 | Netgear | GS305 | switch-soho | no | 0 |
| 2025 | TP-Link | TL-SG108E | switch-smart | no | 0 |
| 2026 | TP-Link | Archer BE900 | router-home | no | 0 |
| 2026 | TP-Link | Archer BE550 | router-home | no | 0 |
| 2026 | TP-Link | Archer BE220 | router-home | no | 0 |
| 2026 | eero | Max 7 | router-mesh | no | 0 |
| 2026 | GL.iNet | Flint 3 (GL-BE9300) | router-home | no | 0 |
| 2026 | Mercusys | MR80X | router-home | no | 0 |
| 2026 | TP-Link | Deco M4 | router-mesh | no | 0 |
| 2026 | Huawei | AX2S | router-home | no | 0 |
| 2026 | Intelbras | Action RG 1200 | router-home | no | 0 |
| 2026 | TP-Link | Archer C80 | router-home | no | 0 |
| 2026 | TP-Link | TL-SG108 | switch-soho | no | 0 |
| 2026 | Intelbras | SG 800 Q+ | switch-soho | no | 0 |
| 2026 | TP-Link | LS1005G | switch-soho | no | 0 |
| 2026 | Netgear | GS305 | switch-soho | no | 0 |
| 2026 | TP-Link | TL-SG108E | switch-smart | no | 0 |

### Brazil Corporate Device List (2010-2026)

| Year | Vendor | Product | Segment | Vendor Covered | Keyword Hits |
|---:|---|---|---|---|---:|
| 2010 | DrayTek | Vigor2110n | router-corporate | no | 0 |
| 2010 | Cisco | ISR 4331 | router-corporate | yes | 0 |
| 2010 | Cisco | C1111-8P | router-corporate | yes | 0 |
| 2010 | Juniper | SRX300 | ngfw-corporate | yes | 0 |
| 2010 | Fortinet | FortiGate 60F | ngfw-corporate | yes | 0 |
| 2010 | Palo Alto Networks | PA-220 | ngfw-corporate | no | 0 |
| 2010 | Aruba | 2930F | switch-corporate | yes | 0 |
| 2010 | MikroTik | RB3011UiAS-RM | router-corporate | no | 0 |
| 2010 | MikroTik | CRS326 | switch-corporate | no | 0 |
| 2010 | Ubiquiti | UniFi Dream Router | router-corporate | no | 0 |
| 2010 | Cisco | Catalyst 2960-X | switch-enterprise | yes | 0 |
| 2010 | Intelbras | SG 800 Q+ | switch-soho | no | 0 |
| 2010 | BrazilFW | BrazilFW Firewall Router | fw-opensource | no | 0 |
| 2011 | DrayTek | Vigor2110n | router-corporate | no | 0 |
| 2011 | Cisco | ISR 4331 | router-corporate | yes | 0 |
| 2011 | Cisco | C1111-8P | router-corporate | yes | 0 |
| 2011 | Juniper | SRX300 | ngfw-corporate | yes | 0 |
| 2011 | Fortinet | FortiGate 60F | ngfw-corporate | yes | 0 |
| 2011 | Palo Alto Networks | PA-220 | ngfw-corporate | no | 0 |
| 2011 | Aruba | 2930F | switch-corporate | yes | 0 |
| 2011 | MikroTik | RB3011UiAS-RM | router-corporate | no | 0 |
| 2011 | MikroTik | CRS326 | switch-corporate | no | 0 |
| 2011 | Ubiquiti | UniFi Dream Router | router-corporate | no | 0 |
| 2011 | Cisco | Catalyst 2960-X | switch-enterprise | yes | 0 |
| 2011 | Intelbras | SG 800 Q+ | switch-soho | no | 0 |
| 2011 | BrazilFW | BrazilFW Firewall Router | fw-opensource | no | 0 |
| 2012 | MikroTik | RB3011UiAS-RM | router-corporate | no | 0 |
| 2012 | MikroTik | RB4011iGS+RM | router-corporate | no | 0 |
| 2012 | MikroTik | CRS326 | switch-corporate | no | 0 |
| 2012 | Cisco | ISR 4331 | router-corporate | yes | 0 |
| 2012 | Cisco | C1111-8P | router-corporate | yes | 0 |
| 2012 | Juniper | SRX300 | ngfw-corporate | yes | 0 |
| 2012 | Fortinet | FortiGate 60F | ngfw-corporate | yes | 0 |
| 2012 | Palo Alto Networks | PA-220 | ngfw-corporate | no | 0 |
| 2012 | Aruba | 2930F | switch-corporate | yes | 0 |
| 2012 | Ubiquiti | UniFi Dream Router | router-corporate | no | 0 |
| 2012 | Cisco | Catalyst 2960-X | switch-enterprise | yes | 0 |
| 2012 | Intelbras | SG 800 Q+ | switch-soho | no | 0 |
| 2012 | Intelbras | SG 1024 MR | switch-corporate | no | 0 |
| 2012 | BrazilFW | BrazilFW Firewall Router | fw-opensource | no | 0 |
| 2012 | DrayTek | Vigor2960 Firewall VPN | fw-smb | no | 0 |
| 2013 | MikroTik | RB3011UiAS-RM | router-corporate | no | 0 |
| 2013 | MikroTik | RB4011iGS+RM | router-corporate | no | 0 |
| 2013 | MikroTik | CRS326 | switch-corporate | no | 0 |
| 2013 | Cisco | ISR 4331 | router-corporate | yes | 0 |
| 2013 | Cisco | C1111-8P | router-corporate | yes | 0 |
| 2013 | Juniper | SRX300 | ngfw-corporate | yes | 0 |
| 2013 | Fortinet | FortiGate 60F | ngfw-corporate | yes | 0 |
| 2013 | Palo Alto Networks | PA-220 | ngfw-corporate | no | 0 |
| 2013 | Aruba | 2930F | switch-corporate | yes | 0 |
| 2013 | Ubiquiti | UniFi Dream Router | router-corporate | no | 0 |
| 2013 | Cisco | Catalyst 3850 | switch-enterprise | yes | 0 |
| 2013 | Intelbras | SG 800 Q+ | switch-soho | no | 0 |
| 2013 | Intelbras | SG 1024 MR | switch-corporate | no | 0 |
| 2013 | BrazilFW | BrazilFW Firewall Router | fw-opensource | no | 0 |
| 2013 | DrayTek | Vigor2960 Firewall VPN | fw-smb | no | 0 |
| 2014 | MikroTik | RB3011UiAS-RM | router-corporate | no | 0 |
| 2014 | MikroTik | RB4011iGS+RM | router-corporate | no | 0 |
| 2014 | MikroTik | CRS326 | switch-corporate | no | 0 |
| 2014 | Cisco | ISR 4331 | router-corporate | yes | 0 |
| 2014 | Cisco | C1111-8P | router-corporate | yes | 0 |
| 2014 | Juniper | SRX300 | ngfw-corporate | yes | 0 |
| 2014 | Fortinet | FortiGate 60F | ngfw-corporate | yes | 0 |
| 2014 | Palo Alto Networks | PA-220 | ngfw-corporate | no | 0 |
| 2014 | Aruba | 2930F | switch-corporate | yes | 0 |
| 2014 | Ubiquiti | UniFi Dream Router | router-corporate | no | 0 |
| 2014 | Cisco | Catalyst 3850 | switch-enterprise | yes | 0 |
| 2014 | Intelbras | SG 1024 MR | switch-corporate | no | 0 |
| 2014 | Fortinet | FortiGate 100F | ngfw-corporate | yes | 0 |
| 2014 | BrazilFW | BrazilFW Firewall Router | fw-opensource | no | 0 |
| 2014 | DrayTek | Vigor2960 Firewall VPN | fw-smb | no | 0 |
| 2015 | MikroTik | RB3011UiAS-RM | router-corporate | no | 0 |
| 2015 | MikroTik | RB4011iGS+RM | router-corporate | no | 0 |
| 2015 | MikroTik | CRS326 | switch-corporate | no | 0 |
| 2015 | Cisco | ISR 4331 | router-corporate | yes | 0 |
| 2015 | Cisco | C1111-8P | router-corporate | yes | 0 |
| 2015 | Juniper | SRX300 | ngfw-corporate | yes | 0 |
| 2015 | Fortinet | FortiGate 60F | ngfw-corporate | yes | 0 |
| 2015 | Palo Alto Networks | PA-220 | ngfw-corporate | no | 0 |
| 2015 | Aruba | 2930F | switch-corporate | yes | 0 |
| 2015 | Ubiquiti | UniFi Dream Router | router-corporate | no | 0 |
| 2015 | Cisco | Catalyst 3850 | switch-enterprise | yes | 0 |
| 2015 | Intelbras | SG 1024 MR | switch-corporate | no | 0 |
| 2015 | Fortinet | FortiGate 100F | ngfw-corporate | yes | 0 |
| 2015 | BrazilFW | BrazilFW Firewall Router | fw-opensource | no | 0 |
| 2015 | DrayTek | Vigor2960 Firewall VPN | fw-smb | no | 0 |
| 2016 | MikroTik | RB3011UiAS-RM | router-corporate | no | 0 |
| 2016 | MikroTik | RB4011iGS+RM | router-corporate | no | 0 |
| 2016 | MikroTik | CRS326 | switch-corporate | no | 0 |
| 2016 | Cisco | ISR 4331 | router-corporate | yes | 0 |
| 2016 | Cisco | C1111-8P | router-corporate | yes | 0 |
| 2016 | Juniper | SRX300 | ngfw-corporate | yes | 0 |
| 2016 | Fortinet | FortiGate 60F | ngfw-corporate | yes | 0 |
| 2016 | Palo Alto Networks | PA-220 | ngfw-corporate | no | 0 |
| 2016 | Aruba | 2930F | switch-corporate | yes | 0 |
| 2016 | Ubiquiti | UniFi Dream Router | router-corporate | no | 0 |
| 2016 | Cisco | Catalyst 9300 | switch-enterprise | yes | 0 |
| 2016 | Intelbras | SG 1024 MR | switch-corporate | no | 0 |
| 2016 | Fortinet | FortiGate 100F | ngfw-corporate | yes | 0 |
| 2016 | Sophos | XGS Firewall | ngfw-smb | yes | 2 |
| 2016 | DrayTek | Vigor2960 Firewall VPN | fw-smb | no | 0 |
| 2017 | MikroTik | RB3011UiAS-RM | router-corporate | no | 0 |
| 2017 | MikroTik | RB4011iGS+RM | router-corporate | no | 0 |
| 2017 | MikroTik | CRS326 | switch-corporate | no | 0 |
| 2017 | Cisco | ISR 4331 | router-corporate | yes | 0 |
| 2017 | Cisco | C1111-8P | router-corporate | yes | 0 |
| 2017 | Juniper | SRX300 | ngfw-corporate | yes | 0 |
| 2017 | Fortinet | FortiGate 60F | ngfw-corporate | yes | 0 |
| 2017 | Palo Alto Networks | PA-220 | ngfw-corporate | no | 0 |
| 2017 | Aruba | 2930F | switch-corporate | yes | 0 |
| 2017 | Ubiquiti | UniFi Dream Router | router-corporate | no | 0 |
| 2017 | Cisco | Catalyst 9300 | switch-enterprise | yes | 0 |
| 2017 | Intelbras | SG 1024 MR | switch-corporate | no | 0 |
| 2017 | Fortinet | FortiGate 100F | ngfw-corporate | yes | 0 |
| 2017 | Sophos | XGS Firewall | ngfw-smb | yes | 2 |
| 2017 | DrayTek | Vigor2960 Firewall VPN | fw-smb | no | 0 |
| 2018 | MikroTik | RB3011UiAS-RM | router-corporate | no | 0 |
| 2018 | MikroTik | RB4011iGS+RM | router-corporate | no | 0 |
| 2018 | MikroTik | CRS326 | switch-corporate | no | 0 |
| 2018 | Cisco | ISR 4331 | router-corporate | yes | 0 |
| 2018 | Cisco | C1111-8P | router-corporate | yes | 0 |
| 2018 | Juniper | SRX300 | ngfw-corporate | yes | 0 |
| 2018 | Fortinet | FortiGate 60F | ngfw-corporate | yes | 0 |
| 2018 | Palo Alto Networks | PA-220 | ngfw-corporate | no | 0 |
| 2018 | Aruba | 2930F | switch-corporate | yes | 0 |
| 2018 | Ubiquiti | UniFi Dream Router | router-corporate | no | 0 |
| 2018 | Cisco | Catalyst 9300 | switch-enterprise | yes | 0 |
| 2018 | Aruba | Instant On 1930 | switch-corporate | yes | 0 |
| 2018 | Intelbras | SG 2404 PoE | switch-poe | no | 0 |
| 2018 | Fortinet | FortiGate 100F | ngfw-corporate | yes | 0 |
| 2018 | SonicWall | TZ Series | fw-smb | yes | 0 |
| 2018 | Blockbit | Blockbit NGFW/UTM | ngfw-corporate | no | 0 |
| 2018 | DrayTek | Vigor2960 Firewall VPN | fw-smb | no | 0 |
| 2019 | MikroTik | RB3011UiAS-RM | router-corporate | no | 0 |
| 2019 | MikroTik | RB4011iGS+RM | router-corporate | no | 0 |
| 2019 | MikroTik | CRS326 | switch-corporate | no | 0 |
| 2019 | Cisco | ISR 4331 | router-corporate | yes | 0 |
| 2019 | Cisco | C1111-8P | router-corporate | yes | 0 |
| 2019 | Juniper | SRX300 | ngfw-corporate | yes | 0 |
| 2019 | Fortinet | FortiGate 60F | ngfw-corporate | yes | 0 |
| 2019 | Palo Alto Networks | PA-220 | ngfw-corporate | no | 0 |
| 2019 | Aruba | 2930F | switch-corporate | yes | 0 |
| 2019 | Ubiquiti | UniFi Dream Router | router-corporate | no | 0 |
| 2019 | OpenWrt | OpenWrt 19.07 Generic Targets | router-firmware | no | 0 |
| 2019 | Cisco | Catalyst 9300 | switch-enterprise | yes | 0 |
| 2019 | Aruba | Instant On 1930 | switch-corporate | yes | 0 |
| 2019 | Intelbras | SG 2404 PoE | switch-poe | no | 0 |
| 2019 | Fortinet | FortiGate 100F | ngfw-corporate | yes | 0 |
| 2019 | SonicWall | TZ Series | fw-smb | yes | 0 |
| 2019 | Netgate | pfSense | fw-opensource | no | 0 |
| 2019 | Starti | Edge Protect NGFW | ngfw-smb | no | 0 |
| 2019 | Blockbit | Blockbit NGFW/UTM | ngfw-corporate | no | 0 |
| 2019 | DrayTek | Vigor2960 Firewall VPN | fw-smb | no | 0 |
| 2020 | MikroTik | RB3011UiAS-RM | router-corporate | no | 0 |
| 2020 | MikroTik | RB4011iGS+RM | router-corporate | no | 0 |
| 2020 | MikroTik | CRS326 | switch-corporate | no | 0 |
| 2020 | Cisco | ISR 4331 | router-corporate | yes | 0 |
| 2020 | Cisco | C1111-8P | router-corporate | yes | 0 |
| 2020 | Juniper | SRX300 | ngfw-corporate | yes | 0 |
| 2020 | Fortinet | FortiGate 60F | ngfw-corporate | yes | 0 |
| 2020 | Palo Alto Networks | PA-220 | ngfw-corporate | no | 0 |
| 2020 | Aruba | 2930F | switch-corporate | yes | 0 |
| 2020 | Ubiquiti | UniFi Dream Router | router-corporate | no | 0 |
| 2020 | Cisco | Catalyst 9300 | switch-enterprise | yes | 0 |
| 2020 | Aruba | Instant On 1930 | switch-corporate | yes | 0 |
| 2020 | Intelbras | SG 2404 PoE | switch-poe | no | 0 |
| 2020 | Fortinet | FortiGate 100F | ngfw-corporate | yes | 0 |
| 2020 | SonicWall | TZ Series | fw-smb | yes | 0 |
| 2020 | Netgate | pfSense | fw-opensource | no | 0 |
| 2020 | Starti | Edge Protect NGFW | ngfw-smb | no | 0 |
| 2020 | Blockbit | Blockbit NGFW/UTM | ngfw-corporate | no | 0 |
| 2020 | Algar Telecom | Algar NGFW | ngfw-isp | no | 0 |
| 2020 | DrayTek | Vigor2960 Firewall VPN | fw-smb | no | 0 |
| 2021 | MikroTik | RB3011UiAS-RM | router-corporate | no | 0 |
| 2021 | MikroTik | RB4011iGS+RM | router-corporate | no | 0 |
| 2021 | MikroTik | CRS326 | switch-corporate | no | 0 |
| 2021 | Cisco | ISR 4331 | router-corporate | yes | 0 |
| 2021 | Cisco | C1111-8P | router-corporate | yes | 0 |
| 2021 | Juniper | SRX300 | ngfw-corporate | yes | 0 |
| 2021 | Fortinet | FortiGate 60F | ngfw-corporate | yes | 0 |
| 2021 | Palo Alto Networks | PA-220 | ngfw-corporate | no | 0 |
| 2021 | Aruba | 2930F | switch-corporate | yes | 0 |
| 2021 | Ubiquiti | UniFi Dream Router | router-corporate | no | 0 |
| 2021 | OpenWrt | OpenWrt 21.02 Generic Targets | router-firmware | no | 0 |
| 2021 | Cisco | Catalyst 9300 | switch-enterprise | yes | 0 |
| 2021 | Aruba | Instant On 1930 | switch-corporate | yes | 0 |
| 2021 | Intelbras | SG 2404 PoE | switch-poe | no | 0 |
| 2021 | Fortinet | FortiGate 100F | ngfw-corporate | yes | 0 |
| 2021 | Sophos | XGS Firewall | ngfw-smb | yes | 2 |
| 2021 | Netgate | pfSense | fw-opensource | no | 0 |
| 2021 | Starti | Edge Protect NGFW | ngfw-smb | no | 0 |
| 2021 | Blockbit | Blockbit NGFW/UTM | ngfw-corporate | no | 0 |
| 2021 | Algar Telecom | Algar NGFW | ngfw-isp | no | 0 |
| 2021 | Azion | Azion Edge Firewall/WAF | fw-cloud-edge | no | 0 |
| 2021 | DrayTek | Vigor2960 Firewall VPN | fw-smb | no | 0 |
| 2022 | MikroTik | RB3011UiAS-RM | router-corporate | no | 0 |
| 2022 | MikroTik | RB4011iGS+RM | router-corporate | no | 0 |
| 2022 | MikroTik | CRS326 | switch-corporate | no | 0 |
| 2022 | Cisco | ISR 4331 | router-corporate | yes | 0 |
| 2022 | Cisco | C1111-8P | router-corporate | yes | 0 |
| 2022 | Juniper | SRX300 | ngfw-corporate | yes | 0 |
| 2022 | Fortinet | FortiGate 60F | ngfw-corporate | yes | 0 |
| 2022 | Palo Alto Networks | PA-220 | ngfw-corporate | no | 0 |
| 2022 | Aruba | 2930F | switch-corporate | yes | 0 |
| 2022 | Ubiquiti | UniFi Dream Router | router-corporate | no | 0 |
| 2022 | OpenWrt | OpenWrt 22.03 Generic Targets | router-firmware | no | 0 |
| 2022 | Cisco | Catalyst 9300 | switch-enterprise | yes | 0 |
| 2022 | Aruba | Instant On 1930 | switch-corporate | yes | 0 |
| 2022 | Intelbras | SG 2404 PoE | switch-poe | no | 0 |
| 2022 | Fortinet | FortiGate 200F | ngfw-corporate | yes | 0 |
| 2022 | Sophos | XGS Firewall | ngfw-smb | yes | 2 |
| 2022 | Netgate | pfSense | fw-opensource | no | 0 |
| 2022 | Cisco | Business CBS250 | switch-corporate | yes | 0 |
| 2022 | Starti | Edge Protect NGFW | ngfw-smb | no | 0 |
| 2022 | Blockbit | Blockbit NGFW/UTM | ngfw-corporate | no | 0 |
| 2022 | Algar Telecom | Algar NGFW | ngfw-isp | no | 0 |
| 2022 | Azion | Azion Edge Firewall/WAF | fw-cloud-edge | no | 0 |
| 2022 | DrayTek | Vigor2960 Firewall VPN | fw-smb | no | 0 |
| 2023 | Ubiquiti | UniFi Dream Router | router-corporate | no | 0 |
| 2023 | Ubiquiti | Cloud Gateway Ultra | router-corporate | no | 0 |
| 2023 | MikroTik | RB3011UiAS-RM | router-corporate | no | 0 |
| 2023 | MikroTik | RB4011iGS+RM | router-corporate | no | 0 |
| 2023 | MikroTik | CRS326 | switch-corporate | no | 0 |
| 2023 | Cisco | ISR 4331 | router-corporate | yes | 0 |
| 2023 | Cisco | C1111-8P | router-corporate | yes | 0 |
| 2023 | Fortinet | FortiGate 60F | ngfw-corporate | yes | 0 |
| 2023 | Juniper | SRX300 | ngfw-corporate | yes | 0 |
| 2023 | Aruba | 2930F | switch-corporate | yes | 0 |
| 2023 | Cisco | Catalyst 9300 | switch-enterprise | yes | 0 |
| 2023 | Aruba | Instant On 1930 | switch-corporate | yes | 0 |
| 2023 | Intelbras | SG 2404 PoE | switch-poe | no | 0 |
| 2023 | Fortinet | FortiGate 200F | ngfw-corporate | yes | 0 |
| 2023 | Sophos | XGS Firewall | ngfw-smb | yes | 2 |
| 2023 | Cisco | Business CBS350 | switch-corporate | yes | 0 |
| 2023 | Ubiquiti | UniFi Switch 8/16/24/48 PoE | switch-corporate | no | 0 |
| 2023 | Starti | Edge Protect NGFW | ngfw-smb | no | 0 |
| 2023 | Blockbit | Blockbit NGFW/UTM | ngfw-corporate | no | 0 |
| 2023 | Algar Telecom | Algar NGFW | ngfw-isp | no | 0 |
| 2023 | Azion | Azion Edge Firewall/WAF | fw-cloud-edge | no | 0 |
| 2023 | DrayTek | Vigor2960 Firewall VPN | fw-smb | no | 0 |
| 2024 | Ubiquiti | UniFi Dream Router | router-corporate | no | 0 |
| 2024 | Ubiquiti | Cloud Gateway Ultra | router-corporate | no | 0 |
| 2024 | MikroTik | RB3011UiAS-RM | router-corporate | no | 0 |
| 2024 | MikroTik | RB4011iGS+RM | router-corporate | no | 0 |
| 2024 | MikroTik | CRS326 | switch-corporate | no | 0 |
| 2024 | Cisco | ISR 4331 | router-corporate | yes | 0 |
| 2024 | Cisco | C1111-8P | router-corporate | yes | 0 |
| 2024 | Fortinet | FortiGate 60F | ngfw-corporate | yes | 0 |
| 2024 | Juniper | SRX300 | ngfw-corporate | yes | 0 |
| 2024 | Aruba | 2930F | switch-corporate | yes | 0 |
| 2024 | OpenWrt | OpenWrt 23.05 Generic Targets | router-firmware | no | 0 |
| 2024 | Cisco | Catalyst 9300 | switch-enterprise | yes | 0 |
| 2024 | Aruba | Instant On 1930 | switch-corporate | yes | 0 |
| 2024 | Intelbras | SG 2404 PoE | switch-poe | no | 0 |
| 2024 | Fortinet | FortiGate 200F | ngfw-corporate | yes | 0 |
| 2024 | Sophos | XGS Firewall | ngfw-smb | yes | 2 |
| 2024 | Cisco | Business CBS350 | switch-corporate | yes | 0 |
| 2024 | Ubiquiti | UniFi Switch 8/16/24/48 PoE | switch-corporate | no | 0 |
| 2024 | Palo Alto Networks | PA-450 | ngfw-corporate | no | 0 |
| 2024 | Starti | Edge Protect NGFW | ngfw-smb | no | 0 |
| 2024 | Blockbit | Blockbit NGFW/UTM | ngfw-corporate | no | 0 |
| 2024 | Algar Telecom | Algar NGFW | ngfw-isp | no | 0 |
| 2024 | Azion | Azion Edge Firewall/WAF | fw-cloud-edge | no | 0 |
| 2024 | DrayTek | Vigor2960 Firewall VPN | fw-smb | no | 0 |
| 2025 | Ubiquiti | UniFi Dream Router | router-corporate | no | 0 |
| 2025 | Ubiquiti | Cloud Gateway Ultra | router-corporate | no | 0 |
| 2025 | MikroTik | RB3011UiAS-RM | router-corporate | no | 0 |
| 2025 | MikroTik | RB4011iGS+RM | router-corporate | no | 0 |
| 2025 | MikroTik | CRS326 | switch-corporate | no | 0 |
| 2025 | Cisco | ISR 4331 | router-corporate | yes | 0 |
| 2025 | Cisco | C1111-8P | router-corporate | yes | 0 |
| 2025 | Fortinet | FortiGate 60F | ngfw-corporate | yes | 0 |
| 2025 | Juniper | SRX300 | ngfw-corporate | yes | 0 |
| 2025 | Aruba | 2930F | switch-corporate | yes | 0 |
| 2025 | OpenWrt | OpenWrt 23.05 Generic Targets | router-firmware | no | 0 |
| 2025 | Cisco | Catalyst 9300 | switch-enterprise | yes | 0 |
| 2025 | Aruba | Instant On 1930 | switch-corporate | yes | 0 |
| 2025 | Intelbras | SG 2404 PoE | switch-poe | no | 0 |
| 2025 | Fortinet | FortiGate 200F | ngfw-corporate | yes | 0 |
| 2025 | Sophos | XGS Firewall | ngfw-smb | yes | 2 |
| 2025 | Cisco | Business CBS350 | switch-corporate | yes | 0 |
| 2025 | Ubiquiti | UniFi Switch 8/16/24/48 PoE | switch-corporate | no | 0 |
| 2025 | Palo Alto Networks | PA-450 | ngfw-corporate | no | 0 |
| 2025 | Starti | Edge Protect NGFW | ngfw-smb | no | 0 |
| 2025 | Blockbit | Blockbit NGFW/UTM | ngfw-corporate | no | 0 |
| 2025 | Algar Telecom | Algar NGFW | ngfw-isp | no | 0 |
| 2025 | Azion | Azion Edge Firewall/WAF | fw-cloud-edge | no | 0 |
| 2025 | DrayTek | Vigor2960 Firewall VPN | fw-smb | no | 0 |
| 2026 | Ubiquiti | UniFi Dream Router | router-corporate | no | 0 |
| 2026 | Ubiquiti | Cloud Gateway Ultra | router-corporate | no | 0 |
| 2026 | MikroTik | RB3011UiAS-RM | router-corporate | no | 0 |
| 2026 | MikroTik | RB4011iGS+RM | router-corporate | no | 0 |
| 2026 | MikroTik | CRS326 | switch-corporate | no | 0 |
| 2026 | Cisco | ISR 4331 | router-corporate | yes | 0 |
| 2026 | Cisco | C1111-8P | router-corporate | yes | 0 |
| 2026 | Fortinet | FortiGate 60F | ngfw-corporate | yes | 0 |
| 2026 | Juniper | SRX300 | ngfw-corporate | yes | 0 |
| 2026 | Aruba | 2930F | switch-corporate | yes | 0 |
| 2026 | OpenWrt | OpenWrt 23.05 Generic Targets | router-firmware | no | 0 |
| 2026 | Cisco | Catalyst 9300 | switch-enterprise | yes | 0 |
| 2026 | Aruba | Instant On 1930 | switch-corporate | yes | 0 |
| 2026 | Intelbras | SG 2404 PoE | switch-poe | no | 0 |
| 2026 | Fortinet | FortiGate 200F | ngfw-corporate | yes | 0 |
| 2026 | Sophos | XGS Firewall | ngfw-smb | yes | 2 |
| 2026 | Cisco | Business CBS350 | switch-corporate | yes | 0 |
| 2026 | Ubiquiti | UniFi Switch 8/16/24/48 PoE | switch-corporate | no | 0 |
| 2026 | Palo Alto Networks | PA-450 | ngfw-corporate | no | 0 |
| 2026 | Starti | Edge Protect NGFW | ngfw-smb | no | 0 |
| 2026 | Blockbit | Blockbit NGFW/UTM | ngfw-corporate | no | 0 |
| 2026 | Algar Telecom | Algar NGFW | ngfw-isp | no | 0 |
| 2026 | Azion | Azion Edge Firewall/WAF | fw-cloud-edge | no | 0 |
| 2026 | DrayTek | Vigor2960 Firewall VPN | fw-smb | no | 0 |

### Global Device List (2010-2026)

| Year | Vendor | Product | Segment | Vendor Covered | Keyword Hits |
|---:|---|---|---|---|---:|
| 2010 | Netgear | WNDR3700 | router-home | no | 0 |
| 2010 | Linksys | WRT610N | router-home | no | 0 |
| 2010 | D-Link | DIR-655 | router-home | no | 0 |
| 2010 | TP-Link | TL-WR1043ND | router-home | no | 0 |
| 2010 | Apple | AirPort Extreme 4th Gen | router-home | no | 0 |
| 2010 | Cisco | Catalyst 2960-X | switch-enterprise | yes | 0 |
| 2011 | Linksys | E4200 | router-home | no | 0 |
| 2011 | ASUS | RT-N56U | router-home | no | 0 |
| 2011 | Netgear | WNDR4000 | router-home | no | 0 |
| 2011 | Trendnet | TEW-692GR | router-home | no | 0 |
| 2011 | Apple | AirPort Extreme 5th Gen | router-home | no | 0 |
| 2011 | Cisco | Catalyst 2960-X | switch-enterprise | yes | 0 |
| 2012 | TP-Link | Archer C20 | router-home | no | 0 |
| 2012 | Linksys | E3200 | router-home | no | 0 |
| 2012 | Netgear | WNDR3700 | router-home | no | 0 |
| 2012 | D-Link | DIR-819 | router-home | no | 0 |
| 2012 | ASUS | RT-N66U | router-home | no | 0 |
| 2012 | Cisco | Catalyst 2960-X | switch-enterprise | yes | 0 |
| 2012 | Juniper | EX2300 | switch-enterprise | yes | 0 |
| 2013 | TP-Link | Archer C7 | router-home | no | 0 |
| 2013 | Netgear | Nighthawk Pro Gaming XR500 | router-home | no | 0 |
| 2013 | ASUS | RT-AC86U | router-home | no | 0 |
| 2013 | Linksys | E4200 | router-home | no | 0 |
| 2013 | Google | Nest Wi-Fi | router-mesh | no | 0 |
| 2013 | AT&T / Arris | NVG589 VDSL Gateway | isp-cpe/modem-router | no | 0 |
| 2013 | Cisco | Catalyst 3850 | switch-enterprise | yes | 0 |
| 2013 | Juniper | EX2300 | switch-enterprise | yes | 0 |
| 2014 | TP-Link | Archer C7 | router-home | no | 0 |
| 2014 | D-Link | DIR-822 | router-home | no | 0 |
| 2014 | ASUS | RT-AC86U | router-home | no | 0 |
| 2014 | Netgear | Nighthawk Pro Gaming XR500 | router-home | no | 0 |
| 2014 | Google | Nest Wi-Fi | router-mesh | no | 0 |
| 2014 | AT&T / Arris | NVG599 VDSL Gateway | isp-cpe/modem-router | no | 0 |
| 2014 | Cisco | Catalyst 3850 | switch-enterprise | yes | 0 |
| 2014 | Arista | 7000 Series | switch-datacenter | no | 0 |
| 2015 | TP-Link | Archer C9 | router-home | no | 0 |
| 2015 | ASUS | RT-AC86U | router-home | no | 0 |
| 2015 | Netgear | Nighthawk Pro Gaming XR500 | router-home | no | 0 |
| 2015 | Google | Nest Wi-Fi | router-mesh | no | 0 |
| 2015 | TP-Link | Archer C6 | router-home | no | 0 |
| 2015 | Cisco | Catalyst 3850 | switch-enterprise | yes | 0 |
| 2015 | Arista | 7000 Series | switch-datacenter | no | 0 |
| 2016 | TP-Link | Archer C9 | router-home | no | 0 |
| 2016 | ASUS | RT-AC86U | router-home | no | 0 |
| 2016 | Google | Nest Wi-Fi | router-mesh | no | 0 |
| 2016 | TP-Link | Archer C7 | router-home | no | 0 |
| 2016 | D-Link | DIR-822 | router-home | no | 0 |
| 2016 | AT&T / Pace | 5268AC U-Verse Gateway | isp-cpe/gateway | no | 0 |
| 2016 | Cisco | Catalyst 9300 | switch-enterprise | yes | 0 |
| 2016 | Arista | 7000 Series | switch-datacenter | no | 0 |
| 2016 | Fortinet | FortiGate 100F | ngfw-corporate | yes | 0 |
| 2017 | TP-Link | Deco M4 | router-mesh | no | 0 |
| 2017 | ASUS | RT-AC86U | router-home | no | 0 |
| 2017 | Google | Nest Wi-Fi | router-mesh | no | 0 |
| 2017 | TP-Link | Archer C7 | router-home | no | 0 |
| 2017 | Netgear | Nighthawk Pro Gaming XR500 | router-home | no | 0 |
| 2017 | AT&T / Pace | 5268AC U-Verse Gateway | isp-cpe/gateway | no | 0 |
| 2017 | Cisco | Catalyst 9300 | switch-enterprise | yes | 0 |
| 2017 | Arista | 7000 Series | switch-datacenter | no | 0 |
| 2017 | Fortinet | FortiGate 100F | ngfw-corporate | yes | 0 |
| 2018 | TP-Link | Deco M4 | router-mesh | no | 0 |
| 2018 | ASUS | RT-AC86U | router-home | no | 0 |
| 2018 | Google | Nest Wi-Fi | router-mesh | no | 0 |
| 2018 | TP-Link | Archer C7 | router-home | no | 0 |
| 2018 | Netgear | Nighthawk Pro Gaming XR500 | router-home | no | 0 |
| 2018 | OpenWrt | OpenWrt x86_64 Virtual Router | router-virtual | no | 0 |
| 2018 | AT&T / Pace | 5268AC U-Verse Gateway | isp-cpe/gateway | no | 0 |
| 2018 | AT&T / Arris | BGW210-700 Fiber Gateway | isp-cpe/gateway | no | 0 |
| 2018 | Cisco | Catalyst 9300 | switch-enterprise | yes | 0 |
| 2018 | Arista | 7000 Series | switch-datacenter | no | 0 |
| 2018 | Cisco | Nexus 9000 | switch-datacenter | yes | 0 |
| 2018 | Fortinet | FortiGate 100F | ngfw-corporate | yes | 0 |
| 2019 | ASUS | RT-AC86U | router-home | no | 0 |
| 2019 | TP-Link | Archer C7 | router-home | no | 0 |
| 2019 | Netgear | Nighthawk Pro Gaming XR500 | router-home | no | 0 |
| 2019 | Google | Nest Wi-Fi | router-mesh | no | 0 |
| 2019 | TP-Link | Deco M4 | router-mesh | no | 0 |
| 2019 | OpenWrt | OpenWrt x86_64 Virtual Router | router-virtual | no | 0 |
| 2019 | AT&T / Pace | 5268AC U-Verse Gateway | isp-cpe/gateway | no | 0 |
| 2019 | AT&T / Arris | BGW210-700 Fiber Gateway | isp-cpe/gateway | no | 0 |
| 2019 | Cisco | Catalyst 9300 | switch-enterprise | yes | 0 |
| 2019 | Arista | 7000 Series | switch-datacenter | no | 0 |
| 2019 | Cisco | Nexus 9000 | switch-datacenter | yes | 0 |
| 2019 | Palo Alto Networks | PA-450 | ngfw-corporate | no | 0 |
| 2020 | TP-Link | Archer C6 | router-home | no | 0 |
| 2020 | TP-Link | Deco M4 | router-mesh | no | 0 |
| 2020 | TP-Link | Archer AX10 | router-home | no | 0 |
| 2020 | ASUS | RT-AC86U | router-home | no | 0 |
| 2020 | D-Link | DIR-822 | router-home | no | 0 |
| 2020 | OpenWrt | OpenWrt x86_64 Virtual Router | router-virtual | no | 0 |
| 2020 | Cisco | Catalyst 9300 | switch-enterprise | yes | 0 |
| 2020 | Arista | 7000 Series | switch-datacenter | no | 0 |
| 2020 | Cisco | Nexus 9000 | switch-datacenter | yes | 0 |
| 2020 | Palo Alto Networks | PA-450 | ngfw-corporate | no | 0 |
| 2020 | Check Point | Quantum Security Gateway | ngfw-enterprise | no | 0 |
| 2021 | TP-Link | Archer AX73 | router-home | no | 0 |
| 2021 | ASUS | RT-AX88U | router-corporate | no | 0 |
| 2021 | TP-Link | Archer AX10 | router-home | no | 0 |
| 2021 | TP-Link | Deco M4 | router-mesh | no | 0 |
| 2021 | Google | Nest Wi-Fi | router-mesh | no | 0 |
| 2021 | OpenWrt | OpenWrt x86_64 Virtual Router | router-virtual | no | 0 |
| 2021 | AT&T / Arris | BGW210-700 Fiber Gateway | isp-cpe/gateway | no | 0 |
| 2021 | Cisco | Catalyst 9300 | switch-enterprise | yes | 0 |
| 2021 | Arista | 7000 Series | switch-datacenter | no | 0 |
| 2021 | Cisco | Nexus 9000 | switch-datacenter | yes | 0 |
| 2021 | Palo Alto Networks | PA-450 | ngfw-corporate | no | 0 |
| 2021 | Check Point | Quantum Security Gateway | ngfw-enterprise | no | 0 |
| 2022 | TP-Link | Archer AX73 | router-home | no | 0 |
| 2022 | Huawei | AX3 Dual Core | router-home | no | 0 |
| 2022 | ASUS | RT-AX88U | router-corporate | no | 0 |
| 2022 | TP-Link | Deco M4 | router-mesh | no | 0 |
| 2022 | Mercusys | MR60X | router-home | no | 0 |
| 2022 | OpenWrt | OpenWrt x86_64 Virtual Router | router-virtual | no | 0 |
| 2022 | AT&T / Arris | BGW210-700 Fiber Gateway | isp-cpe/gateway | no | 0 |
| 2022 | Cisco | Catalyst 9300 | switch-enterprise | yes | 0 |
| 2022 | Arista | 7000 Series | switch-datacenter | no | 0 |
| 2022 | Cisco | Nexus 9000 | switch-datacenter | yes | 0 |
| 2022 | Fortinet | FortiGate 200F | ngfw-corporate | yes | 0 |
| 2022 | Palo Alto Networks | PA-450 | ngfw-corporate | no | 0 |
| 2023 | TP-Link | Archer AX73 | router-home | no | 0 |
| 2023 | TP-Link | Deco M4 | router-mesh | no | 0 |
| 2023 | ASUS | RT-AC86U | router-home | no | 0 |
| 2023 | Huawei | AX3 Dual Core | router-home | no | 0 |
| 2023 | Mercusys | MR60X | router-home | no | 0 |
| 2023 | OpenWrt | OpenWrt x86_64 Virtual Router | router-virtual | no | 0 |
| 2023 | AT&T / Arris | BGW210-700 Fiber Gateway | isp-cpe/gateway | no | 0 |
| 2023 | AT&T / Nokia | BGW320-505 XGS-PON Gateway | isp-cpe/gateway | no | 0 |
| 2023 | Cisco | Catalyst 9300 | switch-enterprise | yes | 0 |
| 2023 | Arista | 7000 Series | switch-datacenter | no | 0 |
| 2023 | Cisco | Nexus 9000 | switch-datacenter | yes | 0 |
| 2023 | Fortinet | FortiGate 200F | ngfw-corporate | yes | 0 |
| 2023 | Palo Alto Networks | PA-450 | ngfw-corporate | no | 0 |
| 2024 | TP-Link | Archer AX73 | router-home | no | 0 |
| 2024 | ASUS | AX5400 | router-home | no | 0 |
| 2024 | TP-Link | Deco BE85 | router-mesh | no | 0 |
| 2024 | Mercusys | MR60X | router-home | no | 0 |
| 2024 | Huawei | AX2S | router-home | no | 0 |
| 2024 | OpenWrt | OpenWrt x86_64 Virtual Router | router-virtual | no | 0 |
| 2024 | AT&T / Arris | BGW210-700 Fiber Gateway | isp-cpe/gateway | no | 0 |
| 2024 | AT&T / Nokia | BGW320-505 XGS-PON Gateway | isp-cpe/gateway | no | 0 |
| 2024 | Cisco | Catalyst 9300 | switch-enterprise | yes | 0 |
| 2024 | Arista | 7000 Series | switch-datacenter | no | 0 |
| 2024 | Cisco | Nexus 9000 | switch-datacenter | yes | 0 |
| 2024 | Fortinet | FortiGate 200F | ngfw-corporate | yes | 0 |
| 2024 | Palo Alto Networks | PA-450 | ngfw-corporate | no | 0 |
| 2025 | TP-Link | Archer AXE75 | router-home | no | 0 |
| 2025 | ASUS | ROG Rapture GT-BE98 Pro | router-home | no | 0 |
| 2025 | TP-Link | Deco BE85 | router-mesh | no | 0 |
| 2025 | eero | Max 7 | router-mesh | no | 0 |
| 2025 | TP-Link | Archer BE550 | router-home | no | 0 |
| 2025 | OpenWrt | OpenWrt x86_64 Virtual Router | router-virtual | no | 0 |
| 2025 | AT&T / Arris | BGW210-700 Fiber Gateway | isp-cpe/gateway | no | 0 |
| 2025 | AT&T / Nokia | BGW320-505 XGS-PON Gateway | isp-cpe/gateway | no | 0 |
| 2025 | Cisco | Catalyst 9300 | switch-enterprise | yes | 0 |
| 2025 | Arista | 7000 Series | switch-datacenter | no | 0 |
| 2025 | Cisco | Nexus 9000 | switch-datacenter | yes | 0 |
| 2025 | Fortinet | FortiGate 200F | ngfw-corporate | yes | 0 |
| 2025 | Palo Alto Networks | PA-3200 | ngfw-enterprise | no | 0 |
| 2026 | TP-Link | Archer BE900 | router-home | no | 0 |
| 2026 | TP-Link | Archer BE550 | router-home | no | 0 |
| 2026 | eero | Max 7 | router-mesh | no | 0 |
| 2026 | GL.iNet | Flint 3 (GL-BE9300) | router-home | no | 0 |
| 2026 | Mercusys | MR80X | router-home | no | 0 |
| 2026 | OpenWrt | OpenWrt x86_64 Virtual Router | router-virtual | no | 0 |
| 2026 | AT&T / Arris | BGW210-700 Fiber Gateway | isp-cpe/gateway | no | 0 |
| 2026 | AT&T / Nokia | BGW320-505 XGS-PON Gateway | isp-cpe/gateway | no | 0 |
| 2026 | Cisco | Catalyst 9300 | switch-enterprise | yes | 0 |
| 2026 | Arista | 7000 Series | switch-datacenter | no | 0 |
| 2026 | Cisco | Nexus 9000 | switch-datacenter | yes | 0 |
| 2026 | Fortinet | FortiGate 200F | ngfw-corporate | yes | 0 |
| 2026 | Palo Alto Networks | PA-3200 | ngfw-enterprise | no | 0 |

### Yearly Reference (2010-2026)

| Year | Vendor | Product |
|---:|---|---|
| 2010 | Netgear | WNDR3700 |
| 2011 | Linksys | E4200 |
| 2012 | TP-Link | Archer C20 |
| 2013 | TP-Link | Archer C7 |
| 2014 | ASUS | RT-AC86U |
| 2015 | TP-Link | Archer C9 |
| 2016 | Google | Nest Wi-Fi |
| 2017 | TP-Link | Deco M4 |
| 2018 | TP-Link | Deco M4 |
| 2019 | Netgear | XR500 |
| 2020 | TP-Link | Archer AX10 |
| 2021 | TP-Link | Archer AX73 |
| 2022 | Huawei | AX3 Dual Core |
| 2023 | Intelbras | Action RG 1200 |
| 2024 | Ubiquiti | Cloud Gateway Ultra |
| 2025 | ASUS | ROG Rapture GT-BE98 Pro |
| 2026 | TP-Link | Archer BE900 |

## External Tooling and Code Intelligence

- No external intelligence catalog found.

## Discord Requested Devices Coverage

| Vendor | Model | Segment | Vendor Covered | Model Keyword Hits | Exploits | Creds | Scanners | Attack Classes | Context |
|---|---|---|---|---:|---:|---:|---:|---|---|
| TP-Link | AC1700 | router | no | 0 | 0 | 0 | 0 | - | user asked applicability to TP-Link AC1700 |
| TP-Link | AC1750 | router | no | 0 | 0 | 0 | 0 | - | home setup mention, landlord-provided router |
| Rogers/Shaw | XB7 (Gen2) | isp-cpe/modem-router | no | 0 | 0 | 0 | 0 | - | customer modem in bridged / passthrough chain |
| Hitron | CGNM-2250 | isp-cpe/modem-router | no | 0 | 0 | 0 | 0 | - | IP passthrough discussion and attack surface concerns |
| AT&T / Pace | 5268AC | isp-cpe/gateway | no | 0 | 0 | 0 | 0 | - | explicit pentest request in conversation |
| ADB / Pirelli | PRG EAV4202N / PRGAV4202N | dsl-gateway | no | 0 | 0 | 0 | 0 | - | default WPA algorithm weakness discussion |
| Technicolor | TG585v6 | dsl-gateway | no | 0 | 0 | 0 | 0 | - | legacy vulnerable fleet mentioned in thread |
| EasyBox | EasyBox (German variants) | dsl-gateway | no | 0 | 0 | 0 | 0 | - | algorithm request in discussion comments |
| Generic | Low-cost Chinese ONU/CPE | onu/isp-cpe | yes | 6 | 11 | 0 | 1 | info_disclosure, rce | claim that modern cheap ONUs are not covered |

## Architecture Inventory Snapshot

- Name: FirewallXPL-Forge Arsenal Index
- Scope: routers, switches, taps, fw, ngfw
- Out of scope: cameras, printers, dvr, dvrs
- Generated by: tools/build_arsenal_index.py

| Domain | Count |
|---|---:|
| catalogs | 16 |
| wordlists | 10 |
| ssh_keys | 8 |
| vendors datasets | 2 |
| mibs | 1758 |
| modules.exploits | 12 |
| modules.creds | 28 |
| modules.scanners | 3 |
| modules.generic | 7 |
| modules.encoders | 13 |
| modules.payloads | 32 |

| curated_arsenal domain | Count |
|---|---:|
| binaries | 2 |
| credentials | 1 |
| firmware | 2 |
| intel | 6 |
| mibs | 1 |
| pocs | 2 |
| wordlists | 1 |

## Workspace Reuse Inventory Snapshot

- workspace_reuse_inventory.json not found.

## Deep Intel Backlog Snapshot

- Total backlog items: 19
- Total keyword hits across backlog: 125

| Priority | Count |
|---|---:|
| p1 | 15 |
| p2 | 3 |
| p3 | 1 |

## Honeypot Final Validation Snapshot

- Campaign: honeypot_validation
- Checked at: 2026-04-03T21:56:54.046319+00:00

| Platform | Ready Queries | Blocked Queries |
|---|---:|---:|
| censys | 0 | 3 |
| fofa | 0 | 3 |
| netlas | 0 | 3 |
| shodan | 0 | 4 |
| zoomeye | 0 | 3 |

## Vendor/Product Capability Matrix

| Vendor | Product | Modules | Exploits | Creds | Scanners | Generic | Payloads | Encoders | CVEs | Attack Classes |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
| a10 | softax_path_traversal | 1 | 1 | 0 | 0 | 0 | 0 | 0 | - | path_traversal |
| armle | bind_tcp | 1 | 0 | 0 | 0 | 0 | 1 | 0 | - | - |
| armle | reverse_tcp | 1 | 0 | 0 | 0 | 0 | 1 | 0 | - | - |
| aruba | clearpass_unauth_rce_cve_2023_25594 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | CVE-2023-25594 | rce |
| aruba | clearpass_xss_stored | 1 | 1 | 0 | 0 | 0 | 0 | 0 | - | - |
| barracuda | esg_cmd_injection_cve_2023_2868 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | CVE-2023-2868 | rce |
| barracuda | esg_spreadsheet_rce_cve_2023_7102 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | CVE-2023-7102 | rce |
| checkpoint | gateway_info_disclosure_cve_2024_24919 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | CVE-2024-24919 | info_disclosure |
| cisco | asa_ftd_path_traversal_cve_2020_3452 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | CVE-2020-3452 | path_traversal |
| cisco | asa_vpn_bruteforce_cve_2023_20269 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | CVE-2023-20269 | - |
| cisco | cisco_asa_ftd_firestarter_chain_cve_2025_20362_20333 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | CVE-2025-20333, CVE-2025-20362 | backdoor |
| cisco | firepower_management60_path_traversal | 1 | 1 | 0 | 0 | 0 | 0 | 0 | CVE-2016-6435 | path_traversal |
| cisco | firepower_management60_rce | 1 | 1 | 0 | 0 | 0 | 0 | 0 | CVE-2016-6433 | backdoor, rce |
| cisco | ftp_default_creds | 1 | 0 | 1 | 0 | 0 | 0 | 0 | - | - |
| cisco | ios_xe_webui_privesc_cve_2023_20198 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | CVE-2023-20198 | - |
| cisco | isa3000_asa_rce_cve_2018_0101 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | CVE-2018-0101 | rce |
| cisco | secure_acs_bypass | 1 | 1 | 0 | 0 | 0 | 0 | 0 | - | auth_bypass |
| cisco | ssh_default_creds | 1 | 0 | 1 | 0 | 0 | 0 | 0 | - | - |
| cisco | telnet_default_creds | 1 | 0 | 1 | 0 | 0 | 0 | 0 | - | - |
| cisco | ucm_info_disclosure | 1 | 1 | 0 | 0 | 0 | 0 | 0 | CVE-2013-7030 | info_disclosure |
| cisco | ucs_manager_rce | 1 | 1 | 0 | 0 | 0 | 0 | 0 | - | rce |
| cisco | unified_multi_path_traversal | 1 | 1 | 0 | 0 | 0 | 0 | 0 | CVE-2011-3315 | path_traversal |
| citrix | adc_rce_cve_2019_19781 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | CVE-2019-19781 | path_traversal, rce |
| citrix | netscaler_citrixbleed_cve_2023_4966 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | CVE-2023-4966 | info_disclosure |
| citrix | netscaler_rce_cve_2023_3519 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | CVE-2023-3519 | rce |
| cmd | awk_bind_tcp | 1 | 0 | 0 | 0 | 0 | 1 | 0 | - | - |
| cmd | awk_bind_udp | 1 | 0 | 0 | 0 | 0 | 1 | 0 | - | - |
| cmd | awk_reverse_tcp | 1 | 0 | 0 | 0 | 0 | 1 | 0 | - | - |
| cmd | bash_reverse_tcp | 1 | 0 | 0 | 0 | 0 | 1 | 0 | - | - |
| cmd | netcat_bind_tcp | 1 | 0 | 0 | 0 | 0 | 1 | 0 | - | - |
| cmd | netcat_reverse_tcp | 1 | 0 | 0 | 0 | 0 | 1 | 0 | - | - |
| cmd | perl_bind_tcp | 1 | 0 | 0 | 0 | 0 | 1 | 0 | - | - |
| cmd | perl_reverse_tcp | 1 | 0 | 0 | 0 | 0 | 1 | 0 | - | - |
| cmd | php_bind_tcp | 1 | 0 | 0 | 0 | 0 | 1 | 0 | - | - |
| cmd | php_reverse_tcp | 1 | 0 | 0 | 0 | 0 | 1 | 0 | - | - |
| cmd | python_bind_tcp | 1 | 0 | 0 | 0 | 0 | 1 | 0 | - | - |
| cmd | python_bind_udp | 1 | 0 | 0 | 0 | 0 | 1 | 0 | - | - |
| cmd | python_reverse_tcp | 1 | 0 | 0 | 0 | 0 | 1 | 0 | - | - |
| cmd | python_reverse_udp | 1 | 0 | 0 | 0 | 0 | 1 | 0 | - | - |
| cve | cve_lookup | 1 | 0 | 0 | 0 | 1 | 0 | 0 | - | - |
| ewon | cosy_unauth_rce_cve_2026_25823 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | CVE-2026-25823 | rce |
| external | metasploit_console_bridge | 1 | 0 | 0 | 0 | 1 | 0 | 0 | - | - |
| external | metasploit_rb_inspect | 1 | 0 | 0 | 0 | 1 | 0 | 0 | - | - |
| external | mikrotikapi_bf_bridge | 1 | 0 | 0 | 0 | 1 | 0 | 0 | - | - |
| f5 | bigip_apm_buffer_overflow_cve_2025_53521 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | CVE-2025-53521 | - |
| f5 | bigip_config_rce_cve_2023_46747 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | CVE-2023-46747 | rce |
| f5 | bigip_icontrol_auth_bypass_cve_2022_1388 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | CVE-2022-1388 | auth_bypass |
| f5 | bigip_icontrol_rest_rce_cve_2021_22986 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | CVE-2021-22986 | rce |
| f5 | bigip_tmui_lfi_cve_2020_5902 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | CVE-2020-5902 | - |
| fortinet | forticlient_ems_preauth_api_bypass_cve_2026_35616 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | CVE-2026-35616 | auth_bypass, backdoor |
| fortinet | forticlientems_sqli_rce_cve_2023_48788 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | CVE-2023-48788 | rce |
| fortinet | forticloud_sso_auth_bypass_cve_2026_24858 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | CVE-2026-24858 | auth_bypass |
| fortinet | fortigate_os_backdoor | 1 | 1 | 0 | 0 | 0 | 0 | 0 | CVE-2014-3413 | backdoor |
| fortinet | fortimanager_fortijump_cve_2024_47575 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | CVE-2024-47575 | - |
| fortinet | fortios_auth_bypass_cve_2022_40684 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | CVE-2022-40684 | auth_bypass |
| fortinet | fortios_sslvpn_heap_rce_cve_2022_42475 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | CVE-2022-42475 | rce |
| fortinet | fortios_sslvpn_path_traversal_cve_2018_13379 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | CVE-2018-13379 | info_disclosure, path_traversal |
| fortinet | fortios_sslvpn_preauth_rce_cve_2023_27997 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | CVE-2023-27997 | rce |
| fortinet | fortios_sslvpn_rce_cve_2024_21762 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | CVE-2024-21762 | rce |
| fortinet | fortios_sslvpn_session_reuse_cve_2024_50562 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | CVE-2024-50562 | - |
| fortinet | fortios_websocket_auth_bypass_cve_2024_55591 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | CVE-2024-55591 | auth_bypass |
| fortinet | fortiweb_admin_rce_cve_2025_64446 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | CVE-2025-64446 | rce |
| fortinet | fortiweb_auth_bypass_rce_cve_2025_25257 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | CVE-2025-25257 | auth_bypass, rce |
| fortinet | ftp_default_creds | 1 | 0 | 1 | 0 | 0 | 0 | 0 | - | - |
| fortinet | ssh_default_creds | 1 | 0 | 1 | 0 | 0 | 0 | 0 | - | - |
| fortinet | telnet_default_creds | 1 | 0 | 1 | 0 | 0 | 0 | 0 | - | - |
| ftp_bruteforce.py | ftp_bruteforce | 1 | 0 | 1 | 0 | 0 | 0 | 0 | - | - |
| ftp_default.py | ftp_default | 1 | 0 | 1 | 0 | 0 | 0 | 0 | - | - |
| generic | dnp3_firewall_evasion | 1 | 1 | 0 | 0 | 0 | 0 | 0 | - | - |
| generic | ethernetip_cip_bypass | 1 | 1 | 0 | 0 | 0 | 0 | 0 | - | - |
| generic | heartbleed | 1 | 1 | 0 | 0 | 0 | 0 | 0 | - | info_disclosure |
| generic | http_form_char_by_char_oracle | 1 | 1 | 0 | 0 | 0 | 0 | 0 | - | info_disclosure |
| generic | http_smuggling_checker | 1 | 1 | 0 | 0 | 0 | 0 | 0 | - | - |
| generic | iec104_manipulation | 1 | 1 | 0 | 0 | 0 | 0 | 0 | - | - |
| generic | misc_scan | 1 | 0 | 0 | 1 | 0 | 0 | 0 | - | - |
| generic | modbus_dpi_bypass | 1 | 1 | 0 | 0 | 0 | 0 | 0 | - | - |
| generic | opcua_firewall_bypass | 1 | 1 | 0 | 0 | 0 | 0 | 0 | - | - |
| generic | shellshock | 1 | 1 | 0 | 0 | 0 | 0 | 0 | CVE-2014-6271, CVE-2014-6278, CVE-2014-7169 | rce |
| generic | ssh_auth_keys | 1 | 1 | 0 | 0 | 0 | 0 | 0 | - | - |
| generic | vlan_hopping_checker | 1 | 1 | 0 | 0 | 0 | 0 | 0 | - | - |
| hirschmann | eagle_auth_bypass_cve_2020_6994 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | CVE-2020-6994 | auth_bypass |
| http_basic_digest_bruteforce.py | http_basic_digest_bruteforce | 1 | 0 | 1 | 0 | 0 | 0 | 0 | - | - |
| http_basic_digest_default.py | http_basic_digest_default | 1 | 0 | 1 | 0 | 0 | 0 | 0 | - | - |
| http_multi_auth_default.py | http_multi_auth_default | 1 | 0 | 1 | 0 | 0 | 0 | 0 | - | - |
| http_web_form_bruteforce.py | http_web_form_bruteforce | 1 | 0 | 1 | 0 | 0 | 0 | 0 | - | - |
| imperva | securesphere_sqli_cve_2013_xxxx | 1 | 1 | 0 | 0 | 0 | 0 | 0 | - | - |
| ipfire | ftp_default_creds | 1 | 0 | 1 | 0 | 0 | 0 | 0 | - | - |
| ipfire | ssh_default_creds | 1 | 0 | 1 | 0 | 0 | 0 | 0 | - | - |
| ipfire | telnet_default_creds | 1 | 0 | 1 | 0 | 0 | 0 | 0 | - | - |
| ivanti | connect_secure_auth_rce_cve_2023_46805 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | CVE-2023-46805, CVE-2024-21887 | rce |
| ivanti | ics_buffer_overflow_rce_cve_2025_0282 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | CVE-2025-0282 | rce |
| juniper | ftp_default_creds | 1 | 0 | 1 | 0 | 0 | 0 | 0 | - | - |
| juniper | jweb_oob_write_rce_cve_2024_21591 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | CVE-2024-21591 | rce |
| juniper | jweb_php_rce_cve_2023_36845 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | CVE-2023-36845 | rce |
| juniper | ssh_default_creds | 1 | 0 | 1 | 0 | 0 | 0 | 0 | - | - |
| juniper | telnet_default_creds | 1 | 0 | 1 | 0 | 0 | 0 | 0 | - | - |
| mipsbe | bind_tcp | 1 | 0 | 0 | 0 | 0 | 1 | 0 | - | - |
| mipsbe | reverse_tcp | 1 | 0 | 0 | 0 | 0 | 1 | 0 | - | - |
| mipsle | bind_tcp | 1 | 0 | 0 | 0 | 0 | 1 | 0 | - | - |
| mipsle | reverse_tcp | 1 | 0 | 0 | 0 | 0 | 1 | 0 | - | - |
| moxa | edr_cmd_injection_cve_2024_9138 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | CVE-2024-9138 | rce |
| moxa | edr_g_jwt_hardcoded_cve_2024_9137 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | CVE-2024-9137 | - |
| paloalto | globalprotect_auth_bypass_cve_2026_0257 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | CVE-2026-0257 | auth_bypass |
| paloalto | globalprotect_cmd_injection_cve_2024_3400 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | CVE-2024-3400 | rce |
| paloalto | panos_auth_bypass_cve_2025_0108 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | CVE-2025-0108 | auth_bypass |
| paloalto | panos_mgmt_auth_bypass_cve_2024_0012 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | CVE-2024-0012, CVE-2024-9474 | auth_bypass |
| paloalto | panos_privesc_cve_2024_9474 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | CVE-2024-0012, CVE-2024-9474 | rce |
| paloalto | panos_saml_auth_bypass_cve_2020_2021 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | CVE-2020-2021 | auth_bypass |
| perl | base64 | 1 | 0 | 0 | 0 | 0 | 0 | 1 | - | - |
| perl | bind_tcp | 1 | 0 | 0 | 0 | 0 | 1 | 0 | - | - |
| perl | hex | 1 | 0 | 0 | 0 | 0 | 0 | 1 | - | - |
| perl | reverse_tcp | 1 | 0 | 0 | 0 | 0 | 1 | 0 | - | - |
| perl | rot13 | 1 | 0 | 0 | 0 | 0 | 0 | 1 | - | - |
| perl | url | 1 | 0 | 0 | 0 | 0 | 0 | 1 | - | - |
| pfsense | antibruteforce_bypass_cve_2023_27100 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | CVE-2023-27100 | - |
| pfsense | interfaces_cmd_injection_cve_2023_42326 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | CVE-2023-42326 | rce |
| pfsense | pfblockerng_rce_cve_2022_31814 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | CVE-2022-31814 | rce |
| pfsense | ssh_default_creds | 1 | 0 | 1 | 0 | 0 | 0 | 0 | - | - |
| pfsense | webinterface_http_form_default_creds | 1 | 0 | 1 | 0 | 0 | 0 | 0 | - | - |
| phoenix | mguard_cmd_injection_cve_2024_43386 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | CVE-2024-43386 | rce |
| php | base64 | 1 | 0 | 0 | 0 | 0 | 0 | 1 | - | - |
| php | bind_tcp | 1 | 0 | 0 | 0 | 0 | 1 | 0 | - | - |
| php | hex | 1 | 0 | 0 | 0 | 0 | 0 | 1 | - | - |
| php | reverse_tcp | 1 | 0 | 0 | 0 | 0 | 1 | 0 | - | - |
| php | rot13 | 1 | 0 | 0 | 0 | 0 | 0 | 1 | - | - |
| php | url | 1 | 0 | 0 | 0 | 0 | 0 | 1 | - | - |
| pulsesecure | sslvpn_arbitrary_file_read_cve_2019_11510 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | CVE-2019-11510 | - |
| python | base32 | 1 | 0 | 0 | 0 | 0 | 0 | 1 | - | - |
| python | base64 | 1 | 0 | 0 | 0 | 0 | 0 | 1 | - | - |
| python | bind_tcp | 1 | 0 | 0 | 0 | 0 | 1 | 0 | - | - |
| python | bind_udp | 1 | 0 | 0 | 0 | 0 | 1 | 0 | - | - |
| python | hex | 1 | 0 | 0 | 0 | 0 | 0 | 1 | - | - |
| python | reverse_tcp | 1 | 0 | 0 | 0 | 0 | 1 | 0 | - | - |
| python | reverse_udp | 1 | 0 | 0 | 0 | 0 | 1 | 0 | - | - |
| python | rot13 | 1 | 0 | 0 | 0 | 0 | 0 | 1 | - | - |
| python | url | 1 | 0 | 0 | 0 | 0 | 0 | 1 | - | - |
| scanners | autopwn | 1 | 0 | 0 | 1 | 0 | 0 | 0 | - | - |
| schneider | connexium_ssh_hardcoded_cve_2017_6026 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | CVE-2017-6026 | - |
| secomea | gatemanager_rce_cve_2020_14500 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | CVE-2020-14500 | rce |
| sftp_bruteforce.py | sftp_bruteforce | 1 | 0 | 1 | 0 | 0 | 0 | 0 | - | - |
| sftp_default.py | sftp_default | 1 | 0 | 1 | 0 | 0 | 0 | 0 | - | - |
| siemens | ruggedcom_web_rce_cve_2023_24845 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | CVE-2023-24845 | rce |
| siemens | scalance_cmd_injection_cve_2023_44373 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | CVE-2023-44373 | rce |
| siemens | sinema_rc_path_traversal_cve_2022_32257 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | CVE-2022-32257 | path_traversal |
| snmp | snmp_trap_listener | 1 | 0 | 0 | 0 | 1 | 0 | 0 | - | - |
| snmp_bruteforce.py | snmp_bruteforce | 1 | 0 | 1 | 0 | 0 | 0 | 0 | - | - |
| snmpv3_default.py | snmpv3_default | 1 | 0 | 1 | 0 | 0 | 0 | 0 | - | - |
| sonicwall | sma100_sqli_cve_2021_20016 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | CVE-2021-20016 | - |
| sonicwall | sma_password_reset_cve_2021_20034 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | CVE-2021-20034 | password_reset_or_change |
| sonicwall | sonicos_sslvpn_access_cve_2024_40766 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | CVE-2024-40766 | - |
| sonicwall | sonicos_sslvpn_auth_bypass_cve_2024_53704 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | CVE-2024-53704 | auth_bypass |
| sonicwall | sonicos_vpn_buffer_overflow_cve_2020_5135 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | CVE-2020-5135 | - |
| sonicwall | sslvpn_shellshock_rce_visualdoor | 1 | 1 | 0 | 0 | 0 | 0 | 0 | CVE-2014-6271 | rce |
| sophos | firewall_code_injection_cve_2022_3236 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | CVE-2022-3236 | - |
| sophos | xg_auth_bypass_cve_2022_1040 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | CVE-2022-1040 | auth_bypass |
| sophos | xg_sqli_asnarok_cve_2020_12271 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | CVE-2020-12271 | - |
| ssh_bruteforce.py | ssh_bruteforce | 1 | 0 | 1 | 0 | 0 | 0 | 0 | - | - |
| ssh_default.py | ssh_default | 1 | 0 | 1 | 0 | 0 | 0 | 0 | - | - |
| telnet_bruteforce.py | telnet_bruteforce | 1 | 0 | 1 | 0 | 0 | 0 | 0 | - | - |
| telnet_default.py | telnet_default | 1 | 0 | 1 | 0 | 0 | 0 | 0 | - | - |
| upnp | ssdp_msearch | 1 | 0 | 0 | 0 | 1 | 0 | 0 | - | - |
| vpn | fortigate_sslvpn_scan | 1 | 0 | 0 | 1 | 0 | 0 | 0 | CVE-2018-13379, CVE-2022-40684, CVE-2023-27997, CVE-2024-21762, CVE-2025-59718 | - |
| watchguard | firebox_cyclops_blink_cve_2022_23176 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | CVE-2022-23176 | - |
| watchguard | xcs_9_rce | 1 | 1 | 0 | 0 | 0 | 0 | 0 | - | rce |
| wordlist | wordlist_generator | 1 | 0 | 0 | 0 | 1 | 0 | 0 | - | - |
| x64 | bind_tcp | 1 | 0 | 0 | 0 | 0 | 1 | 0 | - | - |
| x64 | reverse_tcp | 1 | 0 | 0 | 0 | 0 | 1 | 0 | - | - |
| x86 | bind_tcp | 1 | 0 | 0 | 0 | 0 | 1 | 0 | - | - |
| x86 | reverse_tcp | 1 | 0 | 0 | 0 | 0 | 1 | 0 | - | - |
| zyxel | buffer_overflow_cve_2023_33009 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | CVE-2023-33009 | - |
| zyxel | ike_cmd_injection_cve_2023_28771 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | CVE-2023-28771 | rce |
| zyxel | usg_flex_cmd_injection_cve_2022_30525 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | CVE-2022-30525 | rce |

## Modules By Vendor/Product

### a10 / softax_path_traversal

- Totals: modules=1, exploits=1, creds=0, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: none
- Attack classes: path_traversal
- Module paths:
  - `modules/exploits/lb/a10/softax_path_traversal.py`

### armle / bind_tcp

- Totals: modules=1, exploits=0, creds=0, scanners=0, generic=0, payloads=1, encoders=0
- CVEs: none
- Attack classes: none
- Module paths:
  - `modules/payloads/armle/bind_tcp.py`

### armle / reverse_tcp

- Totals: modules=1, exploits=0, creds=0, scanners=0, generic=0, payloads=1, encoders=0
- CVEs: none
- Attack classes: none
- Module paths:
  - `modules/payloads/armle/reverse_tcp.py`

### aruba / clearpass_unauth_rce_cve_2023_25594

- Totals: modules=1, exploits=1, creds=0, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: CVE-2023-25594
- Attack classes: rce
- Module paths:
  - `modules/exploits/nac/aruba/clearpass_unauth_rce_cve_2023_25594.py`

### aruba / clearpass_xss_stored

- Totals: modules=1, exploits=1, creds=0, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: none
- Attack classes: none
- Module paths:
  - `modules/exploits/nac/aruba/clearpass_xss_stored.py`

### barracuda / esg_cmd_injection_cve_2023_2868

- Totals: modules=1, exploits=1, creds=0, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: CVE-2023-2868
- Attack classes: rce
- Module paths:
  - `modules/exploits/waf/barracuda/esg_cmd_injection_cve_2023_2868.py`

### barracuda / esg_spreadsheet_rce_cve_2023_7102

- Totals: modules=1, exploits=1, creds=0, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: CVE-2023-7102
- Attack classes: rce
- Module paths:
  - `modules/exploits/waf/barracuda/esg_spreadsheet_rce_cve_2023_7102.py`

### checkpoint / gateway_info_disclosure_cve_2024_24919

- Totals: modules=1, exploits=1, creds=0, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: CVE-2024-24919
- Attack classes: info_disclosure
- Module paths:
  - `modules/exploits/perimeter/checkpoint/gateway_info_disclosure_cve_2024_24919.py`

### cisco / asa_ftd_path_traversal_cve_2020_3452

- Totals: modules=1, exploits=1, creds=0, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: CVE-2020-3452
- Attack classes: path_traversal
- Module paths:
  - `modules/exploits/perimeter/cisco/asa_ftd_path_traversal_cve_2020_3452.py`

### cisco / asa_vpn_bruteforce_cve_2023_20269

- Totals: modules=1, exploits=1, creds=0, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: CVE-2023-20269
- Attack classes: none
- Module paths:
  - `modules/exploits/perimeter/cisco/asa_vpn_bruteforce_cve_2023_20269.py`

### cisco / cisco_asa_ftd_firestarter_chain_cve_2025_20362_20333

- Totals: modules=1, exploits=1, creds=0, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: CVE-2025-20333, CVE-2025-20362
- Attack classes: backdoor
- Module paths:
  - `modules/exploits/perimeter/cisco/cisco_asa_ftd_firestarter_chain_cve_2025_20362_20333.py`

### cisco / firepower_management60_path_traversal

- Totals: modules=1, exploits=1, creds=0, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: CVE-2016-6435
- Attack classes: path_traversal
- Module paths:
  - `modules/exploits/perimeter/cisco/firepower_management60_path_traversal.py`

### cisco / firepower_management60_rce

- Totals: modules=1, exploits=1, creds=0, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: CVE-2016-6433
- Attack classes: backdoor, rce
- Module paths:
  - `modules/exploits/perimeter/cisco/firepower_management60_rce.py`

### cisco / ftp_default_creds

- Totals: modules=1, exploits=0, creds=1, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: none
- Attack classes: none
- Module paths:
  - `modules/creds/perimeter/cisco/ftp_default_creds.py`

### cisco / ios_xe_webui_privesc_cve_2023_20198

- Totals: modules=1, exploits=1, creds=0, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: CVE-2023-20198
- Attack classes: none
- Module paths:
  - `modules/exploits/perimeter/cisco/ios_xe_webui_privesc_cve_2023_20198.py`

### cisco / isa3000_asa_rce_cve_2018_0101

- Totals: modules=1, exploits=1, creds=0, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: CVE-2018-0101
- Attack classes: rce
- Module paths:
  - `modules/exploits/perimeter/cisco/isa3000_asa_rce_cve_2018_0101.py`

### cisco / secure_acs_bypass

- Totals: modules=1, exploits=1, creds=0, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: none
- Attack classes: auth_bypass
- Module paths:
  - `modules/exploits/nac/cisco/secure_acs_bypass.py`

### cisco / ssh_default_creds

- Totals: modules=1, exploits=0, creds=1, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: none
- Attack classes: none
- Module paths:
  - `modules/creds/perimeter/cisco/ssh_default_creds.py`

### cisco / telnet_default_creds

- Totals: modules=1, exploits=0, creds=1, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: none
- Attack classes: none
- Module paths:
  - `modules/creds/perimeter/cisco/telnet_default_creds.py`

### cisco / ucm_info_disclosure

- Totals: modules=1, exploits=1, creds=0, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: CVE-2013-7030
- Attack classes: info_disclosure
- Module paths:
  - `modules/exploits/perimeter/cisco/ucm_info_disclosure.py`

### cisco / ucs_manager_rce

- Totals: modules=1, exploits=1, creds=0, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: none
- Attack classes: rce
- Module paths:
  - `modules/exploits/perimeter/cisco/ucs_manager_rce.py`

### cisco / unified_multi_path_traversal

- Totals: modules=1, exploits=1, creds=0, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: CVE-2011-3315
- Attack classes: path_traversal
- Module paths:
  - `modules/exploits/perimeter/cisco/unified_multi_path_traversal.py`

### citrix / adc_rce_cve_2019_19781

- Totals: modules=1, exploits=1, creds=0, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: CVE-2019-19781
- Attack classes: path_traversal, rce
- Module paths:
  - `modules/exploits/vpn/citrix/adc_rce_cve_2019_19781.py`

### citrix / netscaler_citrixbleed_cve_2023_4966

- Totals: modules=1, exploits=1, creds=0, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: CVE-2023-4966
- Attack classes: info_disclosure
- Module paths:
  - `modules/exploits/vpn/citrix/netscaler_citrixbleed_cve_2023_4966.py`

### citrix / netscaler_rce_cve_2023_3519

- Totals: modules=1, exploits=1, creds=0, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: CVE-2023-3519
- Attack classes: rce
- Module paths:
  - `modules/exploits/vpn/citrix/netscaler_rce_cve_2023_3519.py`

### cmd / awk_bind_tcp

- Totals: modules=1, exploits=0, creds=0, scanners=0, generic=0, payloads=1, encoders=0
- CVEs: none
- Attack classes: none
- Module paths:
  - `modules/payloads/cmd/awk_bind_tcp.py`

### cmd / awk_bind_udp

- Totals: modules=1, exploits=0, creds=0, scanners=0, generic=0, payloads=1, encoders=0
- CVEs: none
- Attack classes: none
- Module paths:
  - `modules/payloads/cmd/awk_bind_udp.py`

### cmd / awk_reverse_tcp

- Totals: modules=1, exploits=0, creds=0, scanners=0, generic=0, payloads=1, encoders=0
- CVEs: none
- Attack classes: none
- Module paths:
  - `modules/payloads/cmd/awk_reverse_tcp.py`

### cmd / bash_reverse_tcp

- Totals: modules=1, exploits=0, creds=0, scanners=0, generic=0, payloads=1, encoders=0
- CVEs: none
- Attack classes: none
- Module paths:
  - `modules/payloads/cmd/bash_reverse_tcp.py`

### cmd / netcat_bind_tcp

- Totals: modules=1, exploits=0, creds=0, scanners=0, generic=0, payloads=1, encoders=0
- CVEs: none
- Attack classes: none
- Module paths:
  - `modules/payloads/cmd/netcat_bind_tcp.py`

### cmd / netcat_reverse_tcp

- Totals: modules=1, exploits=0, creds=0, scanners=0, generic=0, payloads=1, encoders=0
- CVEs: none
- Attack classes: none
- Module paths:
  - `modules/payloads/cmd/netcat_reverse_tcp.py`

### cmd / perl_bind_tcp

- Totals: modules=1, exploits=0, creds=0, scanners=0, generic=0, payloads=1, encoders=0
- CVEs: none
- Attack classes: none
- Module paths:
  - `modules/payloads/cmd/perl_bind_tcp.py`

### cmd / perl_reverse_tcp

- Totals: modules=1, exploits=0, creds=0, scanners=0, generic=0, payloads=1, encoders=0
- CVEs: none
- Attack classes: none
- Module paths:
  - `modules/payloads/cmd/perl_reverse_tcp.py`

### cmd / php_bind_tcp

- Totals: modules=1, exploits=0, creds=0, scanners=0, generic=0, payloads=1, encoders=0
- CVEs: none
- Attack classes: none
- Module paths:
  - `modules/payloads/cmd/php_bind_tcp.py`

### cmd / php_reverse_tcp

- Totals: modules=1, exploits=0, creds=0, scanners=0, generic=0, payloads=1, encoders=0
- CVEs: none
- Attack classes: none
- Module paths:
  - `modules/payloads/cmd/php_reverse_tcp.py`

### cmd / python_bind_tcp

- Totals: modules=1, exploits=0, creds=0, scanners=0, generic=0, payloads=1, encoders=0
- CVEs: none
- Attack classes: none
- Module paths:
  - `modules/payloads/cmd/python_bind_tcp.py`

### cmd / python_bind_udp

- Totals: modules=1, exploits=0, creds=0, scanners=0, generic=0, payloads=1, encoders=0
- CVEs: none
- Attack classes: none
- Module paths:
  - `modules/payloads/cmd/python_bind_udp.py`

### cmd / python_reverse_tcp

- Totals: modules=1, exploits=0, creds=0, scanners=0, generic=0, payloads=1, encoders=0
- CVEs: none
- Attack classes: none
- Module paths:
  - `modules/payloads/cmd/python_reverse_tcp.py`

### cmd / python_reverse_udp

- Totals: modules=1, exploits=0, creds=0, scanners=0, generic=0, payloads=1, encoders=0
- CVEs: none
- Attack classes: none
- Module paths:
  - `modules/payloads/cmd/python_reverse_udp.py`

### cve / cve_lookup

- Totals: modules=1, exploits=0, creds=0, scanners=0, generic=1, payloads=0, encoders=0
- CVEs: none
- Attack classes: none
- Module paths:
  - `modules/generic/cve/cve_lookup.py`

### ewon / cosy_unauth_rce_cve_2026_25823

- Totals: modules=1, exploits=1, creds=0, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: CVE-2026-25823
- Attack classes: rce
- Module paths:
  - `modules/exploits/vpn/ewon/cosy_unauth_rce_cve_2026_25823.py`

### external / metasploit_console_bridge

- Totals: modules=1, exploits=0, creds=0, scanners=0, generic=1, payloads=0, encoders=0
- CVEs: none
- Attack classes: none
- Module paths:
  - `modules/generic/external/metasploit_console_bridge.py`

### external / metasploit_rb_inspect

- Totals: modules=1, exploits=0, creds=0, scanners=0, generic=1, payloads=0, encoders=0
- CVEs: none
- Attack classes: none
- Module paths:
  - `modules/generic/external/metasploit_rb_inspect.py`

### external / mikrotikapi_bf_bridge

- Totals: modules=1, exploits=0, creds=0, scanners=0, generic=1, payloads=0, encoders=0
- CVEs: none
- Attack classes: none
- Module paths:
  - `modules/generic/external/mikrotikapi_bf_bridge.py`

### f5 / bigip_apm_buffer_overflow_cve_2025_53521

- Totals: modules=1, exploits=1, creds=0, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: CVE-2025-53521
- Attack classes: none
- Module paths:
  - `modules/exploits/lb/f5/bigip_apm_buffer_overflow_cve_2025_53521.py`

### f5 / bigip_config_rce_cve_2023_46747

- Totals: modules=1, exploits=1, creds=0, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: CVE-2023-46747
- Attack classes: rce
- Module paths:
  - `modules/exploits/lb/f5/bigip_config_rce_cve_2023_46747.py`

### f5 / bigip_icontrol_auth_bypass_cve_2022_1388

- Totals: modules=1, exploits=1, creds=0, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: CVE-2022-1388
- Attack classes: auth_bypass
- Module paths:
  - `modules/exploits/lb/f5/bigip_icontrol_auth_bypass_cve_2022_1388.py`

### f5 / bigip_icontrol_rest_rce_cve_2021_22986

- Totals: modules=1, exploits=1, creds=0, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: CVE-2021-22986
- Attack classes: rce
- Module paths:
  - `modules/exploits/lb/f5/bigip_icontrol_rest_rce_cve_2021_22986.py`

### f5 / bigip_tmui_lfi_cve_2020_5902

- Totals: modules=1, exploits=1, creds=0, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: CVE-2020-5902
- Attack classes: none
- Module paths:
  - `modules/exploits/lb/f5/bigip_tmui_lfi_cve_2020_5902.py`

### fortinet / forticlient_ems_preauth_api_bypass_cve_2026_35616

- Totals: modules=1, exploits=1, creds=0, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: CVE-2026-35616
- Attack classes: auth_bypass, backdoor
- Module paths:
  - `modules/exploits/perimeter/fortinet/forticlient_ems_preauth_api_bypass_cve_2026_35616.py`

### fortinet / forticlientems_sqli_rce_cve_2023_48788

- Totals: modules=1, exploits=1, creds=0, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: CVE-2023-48788
- Attack classes: rce
- Module paths:
  - `modules/exploits/perimeter/fortinet/forticlientems_sqli_rce_cve_2023_48788.py`

### fortinet / forticloud_sso_auth_bypass_cve_2026_24858

- Totals: modules=1, exploits=1, creds=0, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: CVE-2026-24858
- Attack classes: auth_bypass
- Module paths:
  - `modules/exploits/perimeter/fortinet/forticloud_sso_auth_bypass_cve_2026_24858.py`

### fortinet / fortigate_os_backdoor

- Totals: modules=1, exploits=1, creds=0, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: CVE-2014-3413
- Attack classes: backdoor
- Module paths:
  - `modules/exploits/perimeter/fortinet/fortigate_os_backdoor.py`

### fortinet / fortimanager_fortijump_cve_2024_47575

- Totals: modules=1, exploits=1, creds=0, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: CVE-2024-47575
- Attack classes: none
- Module paths:
  - `modules/exploits/perimeter/fortinet/fortimanager_fortijump_cve_2024_47575.py`

### fortinet / fortios_auth_bypass_cve_2022_40684

- Totals: modules=1, exploits=1, creds=0, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: CVE-2022-40684
- Attack classes: auth_bypass
- Module paths:
  - `modules/exploits/perimeter/fortinet/fortios_auth_bypass_cve_2022_40684.py`

### fortinet / fortios_sslvpn_heap_rce_cve_2022_42475

- Totals: modules=1, exploits=1, creds=0, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: CVE-2022-42475
- Attack classes: rce
- Module paths:
  - `modules/exploits/perimeter/fortinet/fortios_sslvpn_heap_rce_cve_2022_42475.py`

### fortinet / fortios_sslvpn_path_traversal_cve_2018_13379

- Totals: modules=1, exploits=1, creds=0, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: CVE-2018-13379
- Attack classes: info_disclosure, path_traversal
- Module paths:
  - `modules/exploits/perimeter/fortinet/fortios_sslvpn_path_traversal_cve_2018_13379.py`

### fortinet / fortios_sslvpn_preauth_rce_cve_2023_27997

- Totals: modules=1, exploits=1, creds=0, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: CVE-2023-27997
- Attack classes: rce
- Module paths:
  - `modules/exploits/perimeter/fortinet/fortios_sslvpn_preauth_rce_cve_2023_27997.py`

### fortinet / fortios_sslvpn_rce_cve_2024_21762

- Totals: modules=1, exploits=1, creds=0, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: CVE-2024-21762
- Attack classes: rce
- Module paths:
  - `modules/exploits/perimeter/fortinet/fortios_sslvpn_rce_cve_2024_21762.py`

### fortinet / fortios_sslvpn_session_reuse_cve_2024_50562

- Totals: modules=1, exploits=1, creds=0, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: CVE-2024-50562
- Attack classes: none
- Module paths:
  - `modules/exploits/perimeter/fortinet/fortios_sslvpn_session_reuse_cve_2024_50562.py`

### fortinet / fortios_websocket_auth_bypass_cve_2024_55591

- Totals: modules=1, exploits=1, creds=0, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: CVE-2024-55591
- Attack classes: auth_bypass
- Module paths:
  - `modules/exploits/perimeter/fortinet/fortios_websocket_auth_bypass_cve_2024_55591.py`

### fortinet / fortiweb_admin_rce_cve_2025_64446

- Totals: modules=1, exploits=1, creds=0, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: CVE-2025-64446
- Attack classes: rce
- Module paths:
  - `modules/exploits/perimeter/fortinet/fortiweb/fortiweb_admin_rce_cve_2025_64446.py`

### fortinet / fortiweb_auth_bypass_rce_cve_2025_25257

- Totals: modules=1, exploits=1, creds=0, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: CVE-2025-25257
- Attack classes: auth_bypass, rce
- Module paths:
  - `modules/exploits/perimeter/fortinet/fortiweb/fortiweb_auth_bypass_rce_cve_2025_25257.py`

### fortinet / ftp_default_creds

- Totals: modules=1, exploits=0, creds=1, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: none
- Attack classes: none
- Module paths:
  - `modules/creds/perimeter/fortinet/ftp_default_creds.py`

### fortinet / ssh_default_creds

- Totals: modules=1, exploits=0, creds=1, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: none
- Attack classes: none
- Module paths:
  - `modules/creds/perimeter/fortinet/ssh_default_creds.py`

### fortinet / telnet_default_creds

- Totals: modules=1, exploits=0, creds=1, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: none
- Attack classes: none
- Module paths:
  - `modules/creds/perimeter/fortinet/telnet_default_creds.py`

### ftp_bruteforce.py / ftp_bruteforce

- Totals: modules=1, exploits=0, creds=1, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: none
- Attack classes: none
- Module paths:
  - `modules/creds/generic/ftp_bruteforce.py`

### ftp_default.py / ftp_default

- Totals: modules=1, exploits=0, creds=1, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: none
- Attack classes: none
- Module paths:
  - `modules/creds/generic/ftp_default.py`

### generic / dnp3_firewall_evasion

- Totals: modules=1, exploits=1, creds=0, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: none
- Attack classes: none
- Module paths:
  - `modules/exploits/perimeter/generic/dnp3_firewall_evasion.py`

### generic / ethernetip_cip_bypass

- Totals: modules=1, exploits=1, creds=0, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: none
- Attack classes: none
- Module paths:
  - `modules/exploits/perimeter/generic/ethernetip_cip_bypass.py`

### generic / heartbleed

- Totals: modules=1, exploits=1, creds=0, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: none
- Attack classes: info_disclosure
- Module paths:
  - `modules/exploits/perimeter/generic/heartbleed.py`

### generic / http_form_char_by_char_oracle

- Totals: modules=1, exploits=1, creds=0, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: none
- Attack classes: info_disclosure
- Module paths:
  - `modules/exploits/perimeter/generic/http_form_char_by_char_oracle.py`

### generic / http_smuggling_checker

- Totals: modules=1, exploits=1, creds=0, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: none
- Attack classes: none
- Module paths:
  - `modules/exploits/perimeter/generic/http_smuggling_checker.py`

### generic / iec104_manipulation

- Totals: modules=1, exploits=1, creds=0, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: none
- Attack classes: none
- Module paths:
  - `modules/exploits/perimeter/generic/iec104_manipulation.py`

### generic / misc_scan

- Totals: modules=1, exploits=0, creds=0, scanners=1, generic=0, payloads=0, encoders=0
- CVEs: none
- Attack classes: none
- Module paths:
  - `modules/scanners/generic/misc_scan.py`

### generic / modbus_dpi_bypass

- Totals: modules=1, exploits=1, creds=0, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: none
- Attack classes: none
- Module paths:
  - `modules/exploits/perimeter/generic/modbus_dpi_bypass.py`

### generic / opcua_firewall_bypass

- Totals: modules=1, exploits=1, creds=0, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: none
- Attack classes: none
- Module paths:
  - `modules/exploits/perimeter/generic/opcua_firewall_bypass.py`

### generic / shellshock

- Totals: modules=1, exploits=1, creds=0, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: CVE-2014-6271, CVE-2014-6278, CVE-2014-7169
- Attack classes: rce
- Module paths:
  - `modules/exploits/perimeter/generic/shellshock.py`

### generic / ssh_auth_keys

- Totals: modules=1, exploits=1, creds=0, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: none
- Attack classes: none
- Module paths:
  - `modules/exploits/perimeter/generic/ssh_auth_keys.py`

### generic / vlan_hopping_checker

- Totals: modules=1, exploits=1, creds=0, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: none
- Attack classes: none
- Module paths:
  - `modules/exploits/nac/generic/vlan_hopping_checker.py`

### hirschmann / eagle_auth_bypass_cve_2020_6994

- Totals: modules=1, exploits=1, creds=0, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: CVE-2020-6994
- Attack classes: auth_bypass
- Module paths:
  - `modules/exploits/perimeter/hirschmann/eagle_auth_bypass_cve_2020_6994.py`

### http_basic_digest_bruteforce.py / http_basic_digest_bruteforce

- Totals: modules=1, exploits=0, creds=1, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: none
- Attack classes: none
- Module paths:
  - `modules/creds/generic/http_basic_digest_bruteforce.py`

### http_basic_digest_default.py / http_basic_digest_default

- Totals: modules=1, exploits=0, creds=1, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: none
- Attack classes: none
- Module paths:
  - `modules/creds/generic/http_basic_digest_default.py`

### http_multi_auth_default.py / http_multi_auth_default

- Totals: modules=1, exploits=0, creds=1, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: none
- Attack classes: none
- Module paths:
  - `modules/creds/generic/http_multi_auth_default.py`

### http_web_form_bruteforce.py / http_web_form_bruteforce

- Totals: modules=1, exploits=0, creds=1, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: none
- Attack classes: none
- Module paths:
  - `modules/creds/generic/http_web_form_bruteforce.py`

### imperva / securesphere_sqli_cve_2013_xxxx

- Totals: modules=1, exploits=1, creds=0, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: none
- Attack classes: none
- Module paths:
  - `modules/exploits/waf/imperva/securesphere_sqli_cve_2013_xxxx.py`

### ipfire / ftp_default_creds

- Totals: modules=1, exploits=0, creds=1, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: none
- Attack classes: none
- Module paths:
  - `modules/creds/perimeter/ipfire/ftp_default_creds.py`

### ipfire / ssh_default_creds

- Totals: modules=1, exploits=0, creds=1, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: none
- Attack classes: none
- Module paths:
  - `modules/creds/perimeter/ipfire/ssh_default_creds.py`

### ipfire / telnet_default_creds

- Totals: modules=1, exploits=0, creds=1, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: none
- Attack classes: none
- Module paths:
  - `modules/creds/perimeter/ipfire/telnet_default_creds.py`

### ivanti / connect_secure_auth_rce_cve_2023_46805

- Totals: modules=1, exploits=1, creds=0, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: CVE-2023-46805, CVE-2024-21887
- Attack classes: rce
- Module paths:
  - `modules/exploits/vpn/ivanti/connect_secure_auth_rce_cve_2023_46805.py`

### ivanti / ics_buffer_overflow_rce_cve_2025_0282

- Totals: modules=1, exploits=1, creds=0, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: CVE-2025-0282
- Attack classes: rce
- Module paths:
  - `modules/exploits/vpn/ivanti/ics_buffer_overflow_rce_cve_2025_0282.py`

### juniper / ftp_default_creds

- Totals: modules=1, exploits=0, creds=1, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: none
- Attack classes: none
- Module paths:
  - `modules/creds/perimeter/juniper/ftp_default_creds.py`

### juniper / jweb_oob_write_rce_cve_2024_21591

- Totals: modules=1, exploits=1, creds=0, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: CVE-2024-21591
- Attack classes: rce
- Module paths:
  - `modules/exploits/perimeter/juniper/jweb_oob_write_rce_cve_2024_21591.py`

### juniper / jweb_php_rce_cve_2023_36845

- Totals: modules=1, exploits=1, creds=0, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: CVE-2023-36845
- Attack classes: rce
- Module paths:
  - `modules/exploits/perimeter/juniper/jweb_php_rce_cve_2023_36845.py`

### juniper / ssh_default_creds

- Totals: modules=1, exploits=0, creds=1, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: none
- Attack classes: none
- Module paths:
  - `modules/creds/perimeter/juniper/ssh_default_creds.py`

### juniper / telnet_default_creds

- Totals: modules=1, exploits=0, creds=1, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: none
- Attack classes: none
- Module paths:
  - `modules/creds/perimeter/juniper/telnet_default_creds.py`

### mipsbe / bind_tcp

- Totals: modules=1, exploits=0, creds=0, scanners=0, generic=0, payloads=1, encoders=0
- CVEs: none
- Attack classes: none
- Module paths:
  - `modules/payloads/mipsbe/bind_tcp.py`

### mipsbe / reverse_tcp

- Totals: modules=1, exploits=0, creds=0, scanners=0, generic=0, payloads=1, encoders=0
- CVEs: none
- Attack classes: none
- Module paths:
  - `modules/payloads/mipsbe/reverse_tcp.py`

### mipsle / bind_tcp

- Totals: modules=1, exploits=0, creds=0, scanners=0, generic=0, payloads=1, encoders=0
- CVEs: none
- Attack classes: none
- Module paths:
  - `modules/payloads/mipsle/bind_tcp.py`

### mipsle / reverse_tcp

- Totals: modules=1, exploits=0, creds=0, scanners=0, generic=0, payloads=1, encoders=0
- CVEs: none
- Attack classes: none
- Module paths:
  - `modules/payloads/mipsle/reverse_tcp.py`

### moxa / edr_cmd_injection_cve_2024_9138

- Totals: modules=1, exploits=1, creds=0, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: CVE-2024-9138
- Attack classes: rce
- Module paths:
  - `modules/exploits/perimeter/moxa/edr_cmd_injection_cve_2024_9138.py`

### moxa / edr_g_jwt_hardcoded_cve_2024_9137

- Totals: modules=1, exploits=1, creds=0, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: CVE-2024-9137
- Attack classes: none
- Module paths:
  - `modules/exploits/perimeter/moxa/edr_g_jwt_hardcoded_cve_2024_9137.py`

### paloalto / globalprotect_auth_bypass_cve_2026_0257

- Totals: modules=1, exploits=1, creds=0, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: CVE-2026-0257
- Attack classes: auth_bypass
- Module paths:
  - `modules/exploits/perimeter/paloalto/globalprotect_auth_bypass_cve_2026_0257.py`

### paloalto / globalprotect_cmd_injection_cve_2024_3400

- Totals: modules=1, exploits=1, creds=0, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: CVE-2024-3400
- Attack classes: rce
- Module paths:
  - `modules/exploits/perimeter/paloalto/globalprotect_cmd_injection_cve_2024_3400.py`

### paloalto / panos_auth_bypass_cve_2025_0108

- Totals: modules=1, exploits=1, creds=0, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: CVE-2025-0108
- Attack classes: auth_bypass
- Module paths:
  - `modules/exploits/perimeter/paloalto/panos_auth_bypass_cve_2025_0108.py`

### paloalto / panos_mgmt_auth_bypass_cve_2024_0012

- Totals: modules=1, exploits=1, creds=0, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: CVE-2024-0012, CVE-2024-9474
- Attack classes: auth_bypass
- Module paths:
  - `modules/exploits/perimeter/paloalto/panos_mgmt_auth_bypass_cve_2024_0012.py`

### paloalto / panos_privesc_cve_2024_9474

- Totals: modules=1, exploits=1, creds=0, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: CVE-2024-0012, CVE-2024-9474
- Attack classes: rce
- Module paths:
  - `modules/exploits/perimeter/paloalto/panos_privesc_cve_2024_9474.py`

### paloalto / panos_saml_auth_bypass_cve_2020_2021

- Totals: modules=1, exploits=1, creds=0, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: CVE-2020-2021
- Attack classes: auth_bypass
- Module paths:
  - `modules/exploits/perimeter/paloalto/panos_saml_auth_bypass_cve_2020_2021.py`

### perl / base64

- Totals: modules=1, exploits=0, creds=0, scanners=0, generic=0, payloads=0, encoders=1
- CVEs: none
- Attack classes: none
- Module paths:
  - `modules/encoders/perl/base64.py`

### perl / bind_tcp

- Totals: modules=1, exploits=0, creds=0, scanners=0, generic=0, payloads=1, encoders=0
- CVEs: none
- Attack classes: none
- Module paths:
  - `modules/payloads/perl/bind_tcp.py`

### perl / hex

- Totals: modules=1, exploits=0, creds=0, scanners=0, generic=0, payloads=0, encoders=1
- CVEs: none
- Attack classes: none
- Module paths:
  - `modules/encoders/perl/hex.py`

### perl / reverse_tcp

- Totals: modules=1, exploits=0, creds=0, scanners=0, generic=0, payloads=1, encoders=0
- CVEs: none
- Attack classes: none
- Module paths:
  - `modules/payloads/perl/reverse_tcp.py`

### perl / rot13

- Totals: modules=1, exploits=0, creds=0, scanners=0, generic=0, payloads=0, encoders=1
- CVEs: none
- Attack classes: none
- Module paths:
  - `modules/encoders/perl/rot13.py`

### perl / url

- Totals: modules=1, exploits=0, creds=0, scanners=0, generic=0, payloads=0, encoders=1
- CVEs: none
- Attack classes: none
- Module paths:
  - `modules/encoders/perl/url.py`

### pfsense / antibruteforce_bypass_cve_2023_27100

- Totals: modules=1, exploits=1, creds=0, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: CVE-2023-27100
- Attack classes: none
- Module paths:
  - `modules/exploits/perimeter/pfsense/antibruteforce_bypass_cve_2023_27100.py`

### pfsense / interfaces_cmd_injection_cve_2023_42326

- Totals: modules=1, exploits=1, creds=0, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: CVE-2023-42326
- Attack classes: rce
- Module paths:
  - `modules/exploits/perimeter/pfsense/interfaces_cmd_injection_cve_2023_42326.py`

### pfsense / pfblockerng_rce_cve_2022_31814

- Totals: modules=1, exploits=1, creds=0, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: CVE-2022-31814
- Attack classes: rce
- Module paths:
  - `modules/exploits/perimeter/pfsense/pfblockerng_rce_cve_2022_31814.py`

### pfsense / ssh_default_creds

- Totals: modules=1, exploits=0, creds=1, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: none
- Attack classes: none
- Module paths:
  - `modules/creds/perimeter/pfsense/ssh_default_creds.py`

### pfsense / webinterface_http_form_default_creds

- Totals: modules=1, exploits=0, creds=1, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: none
- Attack classes: none
- Module paths:
  - `modules/creds/perimeter/pfsense/webinterface_http_form_default_creds.py`

### phoenix / mguard_cmd_injection_cve_2024_43386

- Totals: modules=1, exploits=1, creds=0, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: CVE-2024-43386
- Attack classes: rce
- Module paths:
  - `modules/exploits/perimeter/phoenix/mguard_cmd_injection_cve_2024_43386.py`

### php / base64

- Totals: modules=1, exploits=0, creds=0, scanners=0, generic=0, payloads=0, encoders=1
- CVEs: none
- Attack classes: none
- Module paths:
  - `modules/encoders/php/base64.py`

### php / bind_tcp

- Totals: modules=1, exploits=0, creds=0, scanners=0, generic=0, payloads=1, encoders=0
- CVEs: none
- Attack classes: none
- Module paths:
  - `modules/payloads/php/bind_tcp.py`

### php / hex

- Totals: modules=1, exploits=0, creds=0, scanners=0, generic=0, payloads=0, encoders=1
- CVEs: none
- Attack classes: none
- Module paths:
  - `modules/encoders/php/hex.py`

### php / reverse_tcp

- Totals: modules=1, exploits=0, creds=0, scanners=0, generic=0, payloads=1, encoders=0
- CVEs: none
- Attack classes: none
- Module paths:
  - `modules/payloads/php/reverse_tcp.py`

### php / rot13

- Totals: modules=1, exploits=0, creds=0, scanners=0, generic=0, payloads=0, encoders=1
- CVEs: none
- Attack classes: none
- Module paths:
  - `modules/encoders/php/rot13.py`

### php / url

- Totals: modules=1, exploits=0, creds=0, scanners=0, generic=0, payloads=0, encoders=1
- CVEs: none
- Attack classes: none
- Module paths:
  - `modules/encoders/php/url.py`

### pulsesecure / sslvpn_arbitrary_file_read_cve_2019_11510

- Totals: modules=1, exploits=1, creds=0, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: CVE-2019-11510
- Attack classes: none
- Module paths:
  - `modules/exploits/vpn/pulsesecure/sslvpn_arbitrary_file_read_cve_2019_11510.py`

### python / base32

- Totals: modules=1, exploits=0, creds=0, scanners=0, generic=0, payloads=0, encoders=1
- CVEs: none
- Attack classes: none
- Module paths:
  - `modules/encoders/python/base32.py`

### python / base64

- Totals: modules=1, exploits=0, creds=0, scanners=0, generic=0, payloads=0, encoders=1
- CVEs: none
- Attack classes: none
- Module paths:
  - `modules/encoders/python/base64.py`

### python / bind_tcp

- Totals: modules=1, exploits=0, creds=0, scanners=0, generic=0, payloads=1, encoders=0
- CVEs: none
- Attack classes: none
- Module paths:
  - `modules/payloads/python/bind_tcp.py`

### python / bind_udp

- Totals: modules=1, exploits=0, creds=0, scanners=0, generic=0, payloads=1, encoders=0
- CVEs: none
- Attack classes: none
- Module paths:
  - `modules/payloads/python/bind_udp.py`

### python / hex

- Totals: modules=1, exploits=0, creds=0, scanners=0, generic=0, payloads=0, encoders=1
- CVEs: none
- Attack classes: none
- Module paths:
  - `modules/encoders/python/hex.py`

### python / reverse_tcp

- Totals: modules=1, exploits=0, creds=0, scanners=0, generic=0, payloads=1, encoders=0
- CVEs: none
- Attack classes: none
- Module paths:
  - `modules/payloads/python/reverse_tcp.py`

### python / reverse_udp

- Totals: modules=1, exploits=0, creds=0, scanners=0, generic=0, payloads=1, encoders=0
- CVEs: none
- Attack classes: none
- Module paths:
  - `modules/payloads/python/reverse_udp.py`

### python / rot13

- Totals: modules=1, exploits=0, creds=0, scanners=0, generic=0, payloads=0, encoders=1
- CVEs: none
- Attack classes: none
- Module paths:
  - `modules/encoders/python/rot13.py`

### python / url

- Totals: modules=1, exploits=0, creds=0, scanners=0, generic=0, payloads=0, encoders=1
- CVEs: none
- Attack classes: none
- Module paths:
  - `modules/encoders/python/url.py`

### scanners / autopwn

- Totals: modules=1, exploits=0, creds=0, scanners=1, generic=0, payloads=0, encoders=0
- CVEs: none
- Attack classes: none
- Module paths:
  - `modules/scanners/autopwn.py`

### schneider / connexium_ssh_hardcoded_cve_2017_6026

- Totals: modules=1, exploits=1, creds=0, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: CVE-2017-6026
- Attack classes: none
- Module paths:
  - `modules/exploits/perimeter/schneider/connexium_ssh_hardcoded_cve_2017_6026.py`

### secomea / gatemanager_rce_cve_2020_14500

- Totals: modules=1, exploits=1, creds=0, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: CVE-2020-14500
- Attack classes: rce
- Module paths:
  - `modules/exploits/vpn/secomea/gatemanager_rce_cve_2020_14500.py`

### sftp_bruteforce.py / sftp_bruteforce

- Totals: modules=1, exploits=0, creds=1, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: none
- Attack classes: none
- Module paths:
  - `modules/creds/generic/sftp_bruteforce.py`

### sftp_default.py / sftp_default

- Totals: modules=1, exploits=0, creds=1, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: none
- Attack classes: none
- Module paths:
  - `modules/creds/generic/sftp_default.py`

### siemens / ruggedcom_web_rce_cve_2023_24845

- Totals: modules=1, exploits=1, creds=0, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: CVE-2023-24845
- Attack classes: rce
- Module paths:
  - `modules/exploits/perimeter/siemens/ruggedcom_web_rce_cve_2023_24845.py`

### siemens / scalance_cmd_injection_cve_2023_44373

- Totals: modules=1, exploits=1, creds=0, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: CVE-2023-44373
- Attack classes: rce
- Module paths:
  - `modules/exploits/perimeter/siemens/scalance_cmd_injection_cve_2023_44373.py`

### siemens / sinema_rc_path_traversal_cve_2022_32257

- Totals: modules=1, exploits=1, creds=0, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: CVE-2022-32257
- Attack classes: path_traversal
- Module paths:
  - `modules/exploits/perimeter/siemens/sinema_rc_path_traversal_cve_2022_32257.py`

### snmp / snmp_trap_listener

- Totals: modules=1, exploits=0, creds=0, scanners=0, generic=1, payloads=0, encoders=0
- CVEs: none
- Attack classes: none
- Module paths:
  - `modules/generic/snmp/snmp_trap_listener.py`

### snmp_bruteforce.py / snmp_bruteforce

- Totals: modules=1, exploits=0, creds=1, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: none
- Attack classes: none
- Module paths:
  - `modules/creds/generic/snmp_bruteforce.py`

### snmpv3_default.py / snmpv3_default

- Totals: modules=1, exploits=0, creds=1, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: none
- Attack classes: none
- Module paths:
  - `modules/creds/generic/snmpv3_default.py`

### sonicwall / sma100_sqli_cve_2021_20016

- Totals: modules=1, exploits=1, creds=0, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: CVE-2021-20016
- Attack classes: none
- Module paths:
  - `modules/exploits/perimeter/sonicwall/sma100_sqli_cve_2021_20016.py`

### sonicwall / sma_password_reset_cve_2021_20034

- Totals: modules=1, exploits=1, creds=0, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: CVE-2021-20034
- Attack classes: password_reset_or_change
- Module paths:
  - `modules/exploits/perimeter/sonicwall/sma_password_reset_cve_2021_20034.py`

### sonicwall / sonicos_sslvpn_access_cve_2024_40766

- Totals: modules=1, exploits=1, creds=0, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: CVE-2024-40766
- Attack classes: none
- Module paths:
  - `modules/exploits/perimeter/sonicwall/sonicos_sslvpn_access_cve_2024_40766.py`

### sonicwall / sonicos_sslvpn_auth_bypass_cve_2024_53704

- Totals: modules=1, exploits=1, creds=0, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: CVE-2024-53704
- Attack classes: auth_bypass
- Module paths:
  - `modules/exploits/perimeter/sonicwall/sonicos_sslvpn_auth_bypass_cve_2024_53704.py`

### sonicwall / sonicos_vpn_buffer_overflow_cve_2020_5135

- Totals: modules=1, exploits=1, creds=0, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: CVE-2020-5135
- Attack classes: none
- Module paths:
  - `modules/exploits/perimeter/sonicwall/sonicos_vpn_buffer_overflow_cve_2020_5135.py`

### sonicwall / sslvpn_shellshock_rce_visualdoor

- Totals: modules=1, exploits=1, creds=0, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: CVE-2014-6271
- Attack classes: rce
- Module paths:
  - `modules/exploits/perimeter/sonicwall/sslvpn_shellshock_rce_visualdoor.py`

### sophos / firewall_code_injection_cve_2022_3236

- Totals: modules=1, exploits=1, creds=0, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: CVE-2022-3236
- Attack classes: none
- Module paths:
  - `modules/exploits/perimeter/sophos/firewall_code_injection_cve_2022_3236.py`

### sophos / xg_auth_bypass_cve_2022_1040

- Totals: modules=1, exploits=1, creds=0, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: CVE-2022-1040
- Attack classes: auth_bypass
- Module paths:
  - `modules/exploits/perimeter/sophos/xg_auth_bypass_cve_2022_1040.py`

### sophos / xg_sqli_asnarok_cve_2020_12271

- Totals: modules=1, exploits=1, creds=0, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: CVE-2020-12271
- Attack classes: none
- Module paths:
  - `modules/exploits/perimeter/sophos/xg_sqli_asnarok_cve_2020_12271.py`

### ssh_bruteforce.py / ssh_bruteforce

- Totals: modules=1, exploits=0, creds=1, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: none
- Attack classes: none
- Module paths:
  - `modules/creds/generic/ssh_bruteforce.py`

### ssh_default.py / ssh_default

- Totals: modules=1, exploits=0, creds=1, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: none
- Attack classes: none
- Module paths:
  - `modules/creds/generic/ssh_default.py`

### telnet_bruteforce.py / telnet_bruteforce

- Totals: modules=1, exploits=0, creds=1, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: none
- Attack classes: none
- Module paths:
  - `modules/creds/generic/telnet_bruteforce.py`

### telnet_default.py / telnet_default

- Totals: modules=1, exploits=0, creds=1, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: none
- Attack classes: none
- Module paths:
  - `modules/creds/generic/telnet_default.py`

### upnp / ssdp_msearch

- Totals: modules=1, exploits=0, creds=0, scanners=0, generic=1, payloads=0, encoders=0
- CVEs: none
- Attack classes: none
- Module paths:
  - `modules/generic/upnp/ssdp_msearch.py`

### vpn / fortigate_sslvpn_scan

- Totals: modules=1, exploits=0, creds=0, scanners=1, generic=0, payloads=0, encoders=0
- CVEs: CVE-2018-13379, CVE-2022-40684, CVE-2023-27997, CVE-2024-21762, CVE-2025-59718
- Attack classes: none
- Module paths:
  - `modules/scanners/vpn/fortinet/fortigate_sslvpn_scan.py`

### watchguard / firebox_cyclops_blink_cve_2022_23176

- Totals: modules=1, exploits=1, creds=0, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: CVE-2022-23176
- Attack classes: none
- Module paths:
  - `modules/exploits/perimeter/watchguard/firebox_cyclops_blink_cve_2022_23176.py`

### watchguard / xcs_9_rce

- Totals: modules=1, exploits=1, creds=0, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: none
- Attack classes: rce
- Module paths:
  - `modules/exploits/perimeter/watchguard/xcs_9_rce.py`

### wordlist / wordlist_generator

- Totals: modules=1, exploits=0, creds=0, scanners=0, generic=1, payloads=0, encoders=0
- CVEs: none
- Attack classes: none
- Module paths:
  - `modules/generic/wordlist/wordlist_generator.py`

### x64 / bind_tcp

- Totals: modules=1, exploits=0, creds=0, scanners=0, generic=0, payloads=1, encoders=0
- CVEs: none
- Attack classes: none
- Module paths:
  - `modules/payloads/x64/bind_tcp.py`

### x64 / reverse_tcp

- Totals: modules=1, exploits=0, creds=0, scanners=0, generic=0, payloads=1, encoders=0
- CVEs: none
- Attack classes: none
- Module paths:
  - `modules/payloads/x64/reverse_tcp.py`

### x86 / bind_tcp

- Totals: modules=1, exploits=0, creds=0, scanners=0, generic=0, payloads=1, encoders=0
- CVEs: none
- Attack classes: none
- Module paths:
  - `modules/payloads/x86/bind_tcp.py`

### x86 / reverse_tcp

- Totals: modules=1, exploits=0, creds=0, scanners=0, generic=0, payloads=1, encoders=0
- CVEs: none
- Attack classes: none
- Module paths:
  - `modules/payloads/x86/reverse_tcp.py`

### zyxel / buffer_overflow_cve_2023_33009

- Totals: modules=1, exploits=1, creds=0, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: CVE-2023-33009
- Attack classes: none
- Module paths:
  - `modules/exploits/perimeter/zyxel/buffer_overflow_cve_2023_33009.py`

### zyxel / ike_cmd_injection_cve_2023_28771

- Totals: modules=1, exploits=1, creds=0, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: CVE-2023-28771
- Attack classes: rce
- Module paths:
  - `modules/exploits/perimeter/zyxel/ike_cmd_injection_cve_2023_28771.py`

### zyxel / usg_flex_cmd_injection_cve_2022_30525

- Totals: modules=1, exploits=1, creds=0, scanners=0, generic=0, payloads=0, encoders=0
- CVEs: CVE-2022-30525
- Attack classes: rce
- Module paths:
  - `modules/exploits/perimeter/zyxel/usg_flex_cmd_injection_cve_2022_30525.py`
