# Módulos `generic`

**Idioma:** Português (pt-BR). **English:** [../en-US/08-generic-modules.md](../en-US/08-generic-modules.md)

Módulos genéricos cobrem capacidades multifabricante: lookup de CVE, análise de PCAP, traps SNMP, descoberta UPnP/SSDP, geração de wordlist e varredura Bluetooth LE.

---

## Lookup de CVE — `generic/cve/cve_lookup`

Consulta o banco de dados CVE offline embutido para dispositivos de rede/perímetro.

```text
fxf > use generic/cve/cve_lookup
fxf (CVE Lookup) > set vendor paloalto
fxf (CVE Lookup) > run
```

**Opções:**

| Opção | Tipo | Padrão | Descrição |
|-------|------|--------|-----------|
| `vendor` | `OptString` | `""` | Nome do vendor (busca fuzzy; ex.: `paloalto`, `fortinet`, `cisco`) |
| `product` | `OptString` | `""` | Nome ou modelo do produto |
| `version` | `OptString` | `""` | String de versão do firmware/software |
| `banner` | `OptString` | `""` | Texto de banner bruto (tokens extraídos automaticamente) |
| `remote_only` | `OptBool` | `true` | Mostrar apenas CVEs exploráveis remotamente |
| `show_physical` | `OptBool` | `false` | Incluir CVEs que requerem acesso físico |

**Saída de exemplo — CVE-2026-0257:**
```
fxf > use generic/cve/cve_lookup
fxf (CVE Lookup) > set vendor paloalto
fxf (CVE Lookup) > set product pan-os
fxf (CVE Lookup) > run

[+] CVE-2026-0257 | CVSS: 7.8 | paloalto / pan-os | REMOTE
    GlobalProtect auth override cookie bypass. Exploração ativa confirmada.
    EXPLOITABLE (rxf module available)
    Módulo: exploits/perimeter/paloalto/globalprotect_auth_bypass_cve_2026_0257
    Refs: https://security.paloaltonetworks.com/CVE-2026-0257

[+] CVE-2024-3400 | CVSS: 10.0 | paloalto / pan-os | REMOTE
    Command injection no GlobalProtect levando a RCE
    EXPLOITABLE (rxf module available)
    Módulo: exploits/perimeter/paloalto/globalprotect_cmd_injection_cve_2024_3400
```

---

## Exploit-DB offline — `generic/external/exploitdb_embedded_lookup`

Pesquisa o `files_exploits.csv` do espelho Exploit-DB embutido. Sem necessidade de `searchsploit` ou CLI externo.

Localização: `firewallxpl/resources/arsenal/pocs/integrated_modules/`

---

## PCAP / Wi-Fi offline — `generic/pcap/*`

Requer **Scapy**. Apenas para uso em laboratório autorizado ou análise forense.

| Módulo | Função |
|--------|--------|
| `pcap_ap_station_mapper` | Mapear APs e estações a partir de uma captura |
| `pcap_handshake_extractor` | Extrair handshakes WPA |
| `pcap_offline_wpa_crack` | Fluxo de quebra offline de WPA |
| `pcap_wep_crack` | Ataques estatísticos WEP |
| `pcap_pmkid_attack` | Extração PMKID e fluxo de ataque offline |
| `pcap_credential_sniffer` | Extrair padrões de credenciais da captura |

---

## Gerador de wordlist — `generic/wordlist_generator`

Geração parametrizada de wordlists para alimentar módulos de bruteforce.

---

## Listener SNMP — `generic/snmp_trap_listener`

Escuta traps SNMP em ambientes de laboratório.

| Opção | Tipo | Padrão | Descrição |
|-------|------|--------|-----------|
| `bind_address` | `OptString` | `0.0.0.0` | Endereço de bind |
| `port` | `OptPort` | `162` | Porta UDP de traps |
| `community` | `OptString` | `public` | Community string SNMP |

---

## UPnP / SSDP — `generic/ssdp_msearch`

Descobre dispositivos UPnP na LAN via SSDP M-SEARCH.

---

## Bluetooth LE — `generic/bluetooth/*`

Apenas Linux com `bluepy` opcional. Requer adaptador Bluetooth e permissões adequadas.

---

[Hub da wiki](../README.md)
